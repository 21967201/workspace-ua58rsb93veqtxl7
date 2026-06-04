"""
ECC压缩器优化流程 - 集成Rejected Buffer
自动优化压缩参数，避免重复错误
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 导入ECC压缩器
sys.path.insert(0, str(Path(__file__).parent))
from ecc_compressor import ECCCompressor, CompressorType, ContentRouter


class ECCOptimizerWithRejectedBuffer:
    """ECC压缩器优化器（集成Rejected Buffer）"""
    
    def __init__(self, initial_params=None):
        """
        初始化优化器
        
        Args:
            initial_params: 初始参数配置
        """
        self.compressor = ECCCompressor()
        self.current_params = initial_params or {
            "compression_level": 5,
            "chunk_size": 200,
            "overlap_ratio": 0.1
        }
        self.current_best_ratio = 45.0  # 当前最优压缩比（来自MEMORY.md）
        self.rejected_buffer_dir = Path("rejected-buffer")
        self.rejected_buffer_dir.mkdir(exist_ok=True)
        self.rejected_count = 0
        
    def optimize(self, test_data, max_iterations=20):
        """
        优化压缩参数
        
        Args:
            test_data: 测试数据（长文本列表）
            max_iterations: 最大迭代次数
            
        Returns:
            optimized_params: 优化后的参数
            best_ratio: 最佳压缩比
        """
        print("=" * 60)
        print("ECC压缩器优化 - 集成Rejected Buffer")
        print("=" * 60)
        
        best_params = self.current_params.copy()
        best_ratio = self.current_best_ratio
        
        for i in range(max_iterations):
            print(f"\n[迭代 {i+1}/{max_iterations}]")
            print(f"  当前参数: {self.current_params}")
            print(f"  当前最优压缩比: {best_ratio:.2f}%")
            
            # 1. 生成参数调整提案
            proposal = self._generate_proposal(i)
            print(f"  调整提案: {proposal}")
            
            # 2. 检查Rejected Buffer（避免重复错误）
            if self._is_in_rejected_buffer(proposal):
                print(f"  ⚠️ 该提案曾在Rejected Buffer中，跳过")
                continue
            
            # 3. 测试提案
            test_result = self._test_proposal(proposal, test_data)
            print(f"  测试结果: 压缩比 {test_result['compression_ratio']:.2f}%")
            
            # 4. 判断是否接受
            accepted = False
            if test_result['compression_ratio'] > best_ratio:
                # 严格提升 → 接受
                accepted = True
                best_ratio = test_result['compression_ratio']
                best_params = proposal.copy()
                print(f"  [ACCEPT] 提案已接受: 压缩比提升 {best_ratio:.2f}%")
                
            elif test_result['compression_ratio'] == best_ratio:
                # 持平 → 接受但标记neutral
                accepted = True
                print(f"  [NEUTRAL] 提案已接受 (neutral): 压缩比持平")
                
            else:
                # 下降 → 拒绝，写入Rejected Buffer
                print(f"  [REJECT] 提案已拒绝: 压缩比下降 {best_ratio:.2f}% → {test_result['compression_ratio']:.2f}%")
                self._write_to_rejected_buffer(proposal, test_result, best_ratio)
                
            # 5. 如果接受，更新当前参数
            if accepted:
                self.current_params = proposal.copy()
                
            # 6. 检查是否达到目标（60-80%）
            if best_ratio >= 60.0:
                print(f"\n🎉 已达到目标压缩比: {best_ratio:.2f}%")
                break
                
        print("\n" + "=" * 60)
        print("优化完成")
        print(f"  最优参数: {best_params}")
        print(f"  最佳压缩比: {best_ratio:.2f}%")
        print("=" * 60)
        
        return best_params, best_ratio
    
    def _generate_proposal(self, iteration):
        """生成参数调整提案（文本学习率约束：每次最多调整2个参数）"""
        import random
        
        proposal = self.current_params.copy()
        
        # 文本学习率约束：每次最多调整2个参数（lr=2）
        params_to_adjust = random.sample(list(proposal.keys()), min(2, len(proposal)))
        
        for param in params_to_adjust:
            if param == "compression_level":
                # compression_level: 1-10
                proposal[param] = max(1, min(10, proposal[param] + random.choice([-2, -1, 1, 2])))
            elif param == "chunk_size":
                # chunk_size: 100-2000
                proposal[param] = max(100, min(2000, proposal[param] + random.choice([-200, -100, 100, 200])))
            elif param == "overlap_ratio":
                # overlap_ratio: 0.0-0.5
                proposal[param] = round(max(0.0, min(0.5, proposal[param] + random.choice([-0.1, -0.05, 0.05, 0.1]))), 2)
                
        return proposal
    
    def _is_in_rejected_buffer(self, proposal):
        """检查提案是否在Rejected Buffer中（避免重复错误）"""
        for filename in os.listdir(self.rejected_buffer_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.rejected_buffer_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    rejected_proposal_str = data.get('edit_proposal', '{}')
                    
                    # 安全解析JSON字符串
                    try:
                        rejected_proposal = json.loads(rejected_proposal_str)
                    except json.JSONDecodeError:
                        # 如果不是JSON，跳过
                        continue
                    
                    # 比较关键参数
                    if isinstance(rejected_proposal, dict) and isinstance(proposal, dict):
                        if rejected_proposal.get('compression_level') == proposal.get('compression_level') and \
                           rejected_proposal.get('chunk_size') == proposal.get('chunk_size'):
                            return True
                        
        return False
    
    def _test_proposal(self, proposal, test_data):
        """测试提案（在训练集上）"""
        # 模拟：compression_level越高，压缩比越高，但可能损失准确性
        compression_level = proposal.get('compression_level', 5)
        chunk_size = proposal.get('chunk_size', 200)
        overlap_ratio = proposal.get('overlap_ratio', 0.1)
        
        # 改进模拟：基于参数计算更真实的压缩比
        # compression_level: 1-10, 每增加1级提升约3-5%压缩比
        # chunk_size: 越大压缩比越高（但可能损失信息）
        # overlap_ratio: 越小压缩比越高（但可能丢失上下文）
        base_ratio = 30.0
        level_boost = compression_level * 4.0  # 每级+4%
        chunk_boost = min(30.0, (chunk_size / 200.0) * 15.0)  # 最多+30%
        overlap_penalty = overlap_ratio * 20.0  # overlap越高，压缩比越低
        
        simulated_ratio = base_ratio + level_boost + chunk_boost - overlap_penalty
        simulated_ratio = min(95.0, max(5.0, simulated_ratio))  # 限制在5-95%范围内
        
        # 模拟准确性损失：compression_level越高，准确性越低
        accuracy = max(0.0, 100.0 - compression_level * 3.0 + (overlap_ratio * 50.0))  # overlap可以提升准确性
        
        return {
            "compression_ratio": simulated_ratio,
            "accuracy_score": accuracy,
            "compressor_used": "ECCOptimizer",
            "compressed_content": f"Compressed with level={compression_level}, chunk={chunk_size}, overlap={overlap_ratio}",
            "metadata": {"proposal": proposal}
        }
    
    def _write_to_rejected_buffer(self, proposal, test_result, current_best):
        """写入Rejected Buffer"""
        self.rejected_count += 1
        
        rejected = {
            "id": f"rej_ecc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.rejected_count:03d}",
            "timestamp": datetime.now().isoformat(),
            "skill": "ecc-compressor",
            "step": self.rejected_count,
            "epoch": 1,
            "rejected_reason": f"Compression ratio dropped from {current_best:.2f}% to {test_result['compression_ratio']:.2f}%",
            "edit_proposal": json.dumps(proposal, ensure_ascii=False),
            "target_dimension": "compression_ratio",
            "failure_pattern": "over-aggressive_compression" if proposal.get('compression_level', 5) > 7 else "suboptimal_params",
            "test_case": "ecc_optimization",
            "expected_ratio": "60-80%",
            "actual_ratio": f"{test_result['compression_ratio']:.2f}%"
        }
        
        filename = self.rejected_buffer_dir / f"{rejected['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rejected, f, ensure_ascii=False, indent=2)
        
        print(f"  [INFO] 已写入Rejected Buffer: {filename}")


def main():
    """主函数"""
    # 准备测试数据（长文本）
    test_data = [
        "这是一个长文本测试数据..." * 1000,  # 约30KB
        "Another long text for testing..." * 800,   # 约24KB
        "ECC压缩器优化测试..." * 1200,            # 约36KB
    ]
    
    # 创建优化器
    optimizer = ECCOptimizerWithRejectedBuffer(initial_params={
        "compression_level": 5,
        "chunk_size": 200,
        "overlap_ratio": 0.1
    })
    
    # 执行优化
    best_params, best_ratio = optimizer.optimize(test_data, max_iterations=20)
    
    print(f"\n✅ 优化完成！")
    print(f"  最优参数: {best_params}")
    print(f"  最佳压缩比: {best_ratio:.2f}%")


if __name__ == "__main__":
    main()
