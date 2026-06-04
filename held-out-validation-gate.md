# Held-out Validation Gate - 验证门控机制

**版本**: v1.0  
**创建时间**: 2026-06-03 14:23  
**用途**: 严格验证，仅当验证得分提升时才接受更新

---

## 核心思想

借鉴SkillOpt的Held-out Validation Gate：
- **训练集**: 70% 数据用于优化
- **验证集**: 30% held-out 数据用于严格验证
- **门控规则**: 仅当验证得分 ≥ 当前最优验证得分时才接受更新

---

## 验证流程

### 1. 数据拆分
```
总数据集: 100个测试用例
├─ 训练集 (70%): 用于优化/调参
└─ 验证集 (30%): held-out，用于严格验证
```

### 2. 验证步骤
1. 在**训练集**上优化参数/集成方案
2. 在**验证集**上测试优化后的版本
3. 比较验证集得分：
   - ✅ **严格提升** (score_new > score_current) → 接受，更新当前最优
   - ⚠️ **持平** (score_new == score_current) → 接受但标记"neutral"
   - ❌ **下降** (score_new < score_current) → 拒绝，写入Rejected Buffer

### 3. 门控行为
| 验证结果 | 行为 | 后续操作 |
|----------|------|------------|
| 严格提升 | 接受 | 更新当前技能/配置为最优版本 |
| 持平 | 接受（标记neutral） | 无退化即为安全，但需警惕过拟合 |
| 下降 | 拒绝 | 写入Rejected Buffer，回滚到上一版本 |

---

## 应用场景

### 场景1: ECC压缩器优化

**目标**: 压缩比从45%提升到60-80%

**验证流程**:
1. 准备测试数据：
   - 训练集 (70%): 10个长文本文件（用于调参）
   - 验证集 (30%): 5个held-out长文本（严格验证）

2. 提出压缩参数调整提案：
   ```python
   # 示例：调整 compression_level 参数
   proposal = {
       "compression_level": 8,  # 原值: 5
       "chunk_size": 500         # 原值: 200
   }
   ```

3. 在训练集上测试：
   ```bash
   python test_ecc_compressor.py --train-set train_70percent.json --params compression_level=8,chunk_size=500
   ```
   结果：压缩比 58%（达到预期）

4. **在验证集上严格验证**：
   ```bash
   python test_ecc_compressor.py --val-set val_30percent.json --params compression_level=8,chunk_size=500
   ```
   结果：压缩比 61%（≥ 当前最优 46%）→ ✅ **接受**

5. 如果验证集压缩比 < 46% → ❌ **拒绝**，写入Rejected Buffer

---

### 场景2: headroom集成

**目标**: 集成headroom Token压缩工具

**验证流程**:
1. 准备测试环境：
   - 训练集 (70%): 在测试会话中验证基础功能
   - 验证集 (30%): 在held-out测试集上验证兼容性

2. 提出集成方案：
   ```python
   proposal = {
       "headroom_version": "v1.0",
       "integration_mode": "api",  # vs "cli"
       "fallback": True
   }
   ```

3. 在训练集（测试会话）中验证：
   ```bash
   python test_headroom_integration.py --mode api --fallback True
   ```
   结果：Token压缩比 65%（达到预期）

4. **在验证集（held-out测试集）上严格验证**：
   ```bash
   python test_headroom_compatibility.py --held-out val_30percent.json
   ```
   结果：兼容性 100%（无退化）→ ✅ **接受**

5. 如果验证集兼容性 < 100% → ❌ **拒绝**，写入Rejected Buffer

---

### 场景3: 技术突破集成

**目标**: 集成P0级技术突破（headroom, ECC）

**验证流程**:
1. 对P0级突破，先验证可行性：
   - 训练集 (70%): 在测试环境验证核心功能
   - 验证集 (30%): 在held-out环境验证稳定性和兼容性

2. 验证通过 → 标记为"待集成"
3. 验证失败 → 写入Rejected Buffer，标记为"验证失败"

---

## 实现代码

### Python实现（示例）

```python
import json
from datetime import datetime

class HeldOutValidationGate:
    def __init__(self, current_best_score):
        self.current_best_score = current_best_score
        self.validation_results = []

    def validate(self, proposal, train_score, val_score):
        """验证门控：仅当验证得分提升时才接受"""

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
        import os

        buffer_dir = "rejected-buffer"
        os.makedirs(buffer_dir, exist_ok=True)

        rejected = {
            "id": f"rej_{datetime.now().strftime('%Y%m%d_%H%M%S')}_001",
            "timestamp": datetime.now().isoformat(),
            "proposal": proposal,
            "val_score": result["val_score"],
            "current_best": result["current_best"],
            "rejected_reason": result["reason"],
            "failure_pattern": "validation_score_dropped"
        }

        filename = f"{buffer_dir}/{rejected['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rejected, f, ensure_ascii=False, indent=2)

        print(f"[INFO] 已写入Rejected Buffer: {filename}")

    def save_validation_log(self, output_file):
        """保存验证日志"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "current_best_score": self.current_best_score,
                "validation_results": self.validation_results
            }, f, ensure_ascii=False, indent=2)
        print(f"[INFO] 已保存验证日志: {output_file}")


# 使用示例
if __name__ == "__main__":
    # 当前最优验证得分（例如：ECC压缩器当前压缩比46%）
    gate = HeldOutValidationGate(current_best_score=46.0)

    # 提出优化提案
    proposal = {
        "compression_level": 8,
        "chunk_size": 500
    }

    # 在训练集上测试（压缩比58%）
    train_score = 58.0

    # 在验证集上严格验证（压缩比61%）
    val_score = 61.0

    # 门控验证
    accepted, result = gate.validate(proposal, train_score, val_score)

    if accepted:
        print(f"✅ 提案已接受: {result['reason']}")
    else:
        print(f"❌ 提案已拒绝: {result['reason']}")

    # 保存验证日志
    gate.save_validation_log("validation_log.json")
```

---

## 与优化流程集成

### ECC压缩器优化流程（增强版）

```
1. 提出压缩参数调整提案
   ↓
2. 检查 Rejected Buffer（避免重复错误）
   ↓
3. 在训练集（70%）上测试
   ↓
4. 【关键】在验证集（30% held-out）上严格验证
   ↓
5. Held-out Validation Gate 门控
   ├─ 严格提升 → 接受，更新当前最优
   ├─ 持平 → 接受（标记neutral）
   └─ 下降 → 拒绝，写入Rejected Buffer
   ↓
6. 如果接受 → 继续优化
   如果拒绝 → 回滚到上一版本，调整提案
```

### headroom集成流程（增强版）

```
1. 提出集成方案
   ↓
2. 检查 Rejected Buffer（避免兼容性问题）
   ↓
3. 在训练环境（70%）中验证基础功能
   ↓
4. 【关键】在held-out验证环境（30%）中验证兼容性
   ↓
5. Held-out Validation Gate 门控
   ├─ 兼容性100% → 接受，标记为"待集成"
   ├─ 兼容性≥95% → 接受（标记neutral，需进一步测试）
   └─ 兼容性<95% → 拒绝，写入Rejected Buffer
   ↓
6. 如果接受 → 集成到主会话
   如果拒绝 → 修复兼容性问题，重新提出方案
```

---

## 预期收益

| 机制 | 收益 | 证据 |
|------|------|------|
| Held-out Validation Gate | 确保每次更新质量不退化 | SkillOpt论文：每次更新都有验证保障 |
| 与Rejected Buffer联动 | 加速收敛，避免重复无效编辑 | 失败案例不重复出现 |
| 严格门控 | 防止过拟合，提升泛化能力 | 仅在held-out集上验证通过才接受 |

**综合预估**：
- ECC压缩器优化成功率：从 ~70% 提升至 ~90%
- headroom集成成功率：从 ~60% 提升至 ~85%
- 技术突破集成质量：显著提升，避免"看似有效但实际退化"

---

## 文件清单

1. `held-out-validation-gate.md` - 本文档（说明+使用指南）
2. `held-out-validation-gate.py` - Python实现（可集成到优化流程）
3. `validation_log.json` - 验证日志（每次验证的记录）
4. 与 `rejected-buffer/` 联动（拒绝时自动写入）

---

**创建者**: OpenClaw Agent (全自动)  
**版本**: v1.0  
**状态**: ✅ 已启用，可立即集成到ECC优化和headroom集成流程中
