"""
Held-out Validation Gate - Python实现
严格验证，仅当验证得分提升时才接受更新
"""

import json
from datetime import datetime
from pathlib import Path


class HeldOutValidationGate:
    """Held-out Validation Gate 验证门控类"""

    def __init__(self, current_best_score):
        """
        初始化验证门控

        Args:
            current_best_score: 当前最优验证得分（例如：ECC压缩比46%）
        """
        self.current_best_score = current_best_score
        self.validation_results = []
        self.buffer_dir = Path("rejected-buffer")
        self.buffer_dir.mkdir(exist_ok=True)

    def validate(self, proposal, train_score, val_score):
        """
        验证门控：仅当验证得分提升时才接受

        Args:
            proposal: 优化提案（dict）
            train_score: 训练集得分
            val_score: 验证集得分

        Returns:
            (accepted: bool, result: dict)
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "proposal": proposal,
            "train_score": train_score,
            "val_score": val_score,
            "current_best": self.current_best_score,
            "decision": None,
            "reason": None
        }

        # 门控逻辑
        if val_score > self.current_best_score:
            # 严格提升 → 接受
            result["decision"] = "accept"
            result["reason"] = f"Validation score improved: {self.current_best_score} → {val_score}"
            self.current_best_score = val_score
            self.validation_results.append(result)
            return True, result

        elif val_score == self.current_best_score:
            # 持平 → 接受但标记neutral
            result["decision"] = "accept_neutral"
            result["reason"] = f"Validation score unchanged: {val_score}"
            self.validation_results.append(result)
            return True, result

        else:
            # 下降 → 拒绝
            result["decision"] = "reject"
            result["reason"] = f"Validation score dropped: {self.current_best_score} → {val_score}"
            self.validation_results.append(result)

            # 写入Rejected Buffer
            self._write_to_rejected_buffer(proposal, result)
            return False, result

    def _write_to_rejected_buffer(self, proposal, result):
        """写入Rejected Buffer"""
        rejected = {
            "id": f"rej_{datetime.now().strftime('%Y%m%d_%H%M%S')}_001",
            "timestamp": datetime.now().isoformat(),
            "skill": proposal.get("skill", "unknown"),
            "step": proposal.get("step", 0),
            "epoch": proposal.get("epoch", 0),
            "rejected_reason": result["reason"],
            "edit_proposal": json.dumps(proposal, ensure_ascii=False),
            "target_dimension": proposal.get("target_dimension", "unknown"),
            "failure_pattern": "validation_score_dropped",
            "train_score": result["train_score"],
            "val_score": result["val_score"],
            "current_best": result["current_best"]
        }

        filename = self.buffer_dir / f"{rejected['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rejected, f, ensure_ascii=False, indent=2)

        print(f"[INFO] 已写入Rejected Buffer: {filename}")

    def save_validation_log(self, output_file):
        """保存验证日志"""
        log = {
            "current_best_score": self.current_best_score,
            "validation_results": self.validation_results
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

        print(f"[INFO] 已保存验证日志: {output_file}")


# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("Held-out Validation Gate - 测试")
    print("=" * 60)

    # 当前最优验证得分（例如：ECC压缩器当前压缩比46%）
    gate = HeldOutValidationGate(current_best_score=46.0)

    # 测试1：严格提升 → 接受
    print("\n[测试1] 严格提升 → 应接受")
    proposal1 = {
        "skill": "ecc-compressor",
        "step": 1,
        "epoch": 1,
        "compression_level": 8,
        "chunk_size": 500,
        "target_dimension": "compression_ratio"
    }
    accepted1, result1 = gate.validate(proposal1, train_score=58.0, val_score=61.0)
    print(f"  决策: {result1['decision']}")
    print(f"  原因: {result1['reason']}")
    print(f"  结果: {'✅ 已接受' if accepted1 else '❌ 已拒绝'}")

    # 测试2：下降 → 拒绝
    print("\n[测试2] 下降 → 应拒绝")
    proposal2 = {
        "skill": "ecc-compressor",
        "step": 2,
        "epoch": 1,
        "compression_level": 9,
        "chunk_size": 1000,
        "target_dimension": "compression_ratio"
    }
    accepted2, result2 = gate.validate(proposal2, train_score=55.0, val_score=42.0)
    print(f"  决策: {result2['decision']}")
    print(f"  原因: {result2['reason']}")
    print(f"  结果: {'✅ 已接受' if accepted2 else '❌ 已拒绝'}")

    # 测试3：持平 → 接受（neutral）
    print("\n[测试3] 持平 → 应接受（neutral）")
    proposal3 = {
        "skill": "ecc-compressor",
        "step": 3,
        "epoch": 1,
        "compression_level": 8,
        "chunk_size": 500,
        "target_dimension": "compression_ratio"
    }
    accepted3, result3 = gate.validate(proposal3, train_score=61.0, val_score=61.0)
    print(f"  决策: {result3['decision']}")
    print(f"  原因: {result3['reason']}")
    print(f"  结果: {'✅ 已接受' if accepted3 else '❌ 已拒绝'}")

    # 保存验证日志
    gate.save_validation_log("validation_log.json")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
