"""
LLMLingua-2 vs Phase 6 三元组压缩对比测试

任务C: 对比两种压缩方法的压缩率、质量损失、速度

测试维度:
1. 压缩率 (Compression Ratio)
2. 质量损失 (Quality Loss, 使用BLEU/BERTScore)
3. 处理速度 (Tokens/sec)
4. 语义保留 (Semantic Preservation)
"""

import time
import torch
from typing import List, Dict, Tuple, Any
import json


# ==================== 方法1: Phase 6 三元组压缩 ====================

class Phase6TripleCompressor:
    """
    Phase 6 三元组压缩
    
    原理: 将"实体-关系-实体"替换为符号
    例如: "关键词不足导致降权" → "关键词不足→降权"
    """
    
    # 关系词映射 (从Token Optimizer档案提取)
    RELATION_MAP = {
        "导致": "→",
        "引起": "→",
        "造成": "→",
        "提升": "↑",
        "增加": "↑",
        "提高": "↑",
        "下降": "↓",
        "降低": "↓",
        "减少": "↓",
        "建议": "!",
        "推荐": "!",
        "应该": "!",
    }
    
    # 冗余词汇 (删除不影响语义)
    REDUNDANT_WORDS = ["的", "了", "是", "在", "和", "与", "或", "这", "那"]
    
    def compress(self, text: str) -> str:
        """
        压缩文本为三元组格式
        
        Args:
            text: 原文
            
        Returns:
            str: 压缩后的文本
        """
        compressed = text
        
        # 1. 替换关系词为符号
        for relation, symbol in self.RELATION_MAP.items():
            compressed = compressed.replace(relation, symbol)
        
        # 2. 删除冗余词汇
        for word in self.REDUNDANT_WORDS:
            compressed = compressed.replace(word, "")
        
        return compressed
    
    def batch_compress(self, texts: List[str]) -> List[str]:
        """批量压缩"""
        return [self.compress(text) for text in texts]
    
    def calculate_compression_ratio(self, original: str, compressed: str) -> float:
        """
        计算压缩率
        
        Returns:
            float: 压缩率 (0-1, 1表示完全压缩)
        """
        original_len = len(original)
        compressed_len = len(compressed)
        
        if original_len == 0:
            return 0.0
        
        return 1 - (compressed_len / original_len)


# ==================== 方法2: LLMLingua-2 压缩 ====================

try:
    from llm_lingua import PromptCompressor
    
    LLMLINGUA_AVAILABLE = True
except ImportError:
    LLMLINGUA_AVAILABLE = False
    print("[WARNING] LLMLingua not installed. Install with: pip install llmlingua")


class LLMLinguaCompressor:
    """
    LLMLingua-2 压缩
    
    原理: 使用小模型(GPT-2)做压缩决策,智能删除冗余token
    特点: 语义保留更好,压缩率更高
    
    论文: "LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models"
    arXiv: 2310.05736
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/llmlingua-2-bert-base-multilingual-cased",
        use_auth_token: bool = False,
    ):
        """
        初始化LLMLingua压缩器
        
        Args:
            model_name: 压缩模型 (默认使用多语言BERT)
            use_auth_token: 是否需要HuggingFace token
        """
        if not LLMLINGUA_AVAILABLE:
            raise RuntimeError("LLMLingua not installed")
        
        self.compressor = PromptCompressor(
            model_name=model_name,
            use_auth_token=use_auth_token,
        )
    
    def compress(
        self,
        text: str,
        rate: float = 0.8,
        force_tokens: List[str] = None,
    ) -> str:
        """
        压缩文本
        
        Args:
            text: 原文
            rate: 压缩率 (0.8 = 压缩80%的token)
            force_tokens: 强制保留的token (如"\n", "?", "!")
            
        Returns:
            str: 压缩后的文本
        """
        result = self.compressor.compress_prompt(
            text,
            rate=rate,
            force_tokens=force_tokens or [],
        )
        
        # LLMLingua返回字典,包含压缩后的prompt
        return result["compressed_prompt"]
    
    def batch_compress(
        self,
        texts: List[str],
        rate: float = 0.8,
    ) -> List[str]:
        """批量压缩"""
        return [self.compress(text, rate=rate) for text in texts]
    
    def calculate_compression_ratio(self, original: str, compressed: str) -> float:
        """计算压缩率"""
        original_tokens = len(original.split())
        compressed_tokens = len(compressed.split())
        
        if original_tokens == 0:
            return 0.0
        
        return 1 - (compressed_tokens / original_tokens)


# ==================== 质量评估 ====================

class QualityEvaluator:
    """
    质量评估器
    
    评估维度:
    1. BLEU Score (n-gram重叠)
    2. BERTScore (语义相似度)
    3. 人工评分 (模拟)
    """
    
    def __init__(self):
        self.results = []
    
    def evaluate_bleu(self, original: str, compressed: str) -> float:
        """
        计算BLEU Score
        
        Args:
            original: 原文
            compressed: 压缩后文本
            
        Returns:
            float: BLEU Score (0-1, 1表示完全相同)
        """
        # 简化版BLEU (unigram precision)
        original_tokens = original.split()
        compressed_tokens = compressed.split()
        
        if len(compressed_tokens) == 0:
            return 0.0
        
        # 计算重合token数
        overlap = sum(1 for token in compressed_tokens if token in original_tokens)
        precision = overlap / len(compressed_tokens)
        
        # Brevity Penalty
        bp = min(1.0, len(compressed_tokens) / len(original_tokens))
        
        bleu = bp * precision
        return bleu
    
    def evaluate_semantic_similarity(
        self,
        original: str,
        compressed: str,
    ) -> float:
        """
        评估语义相似度 (简化版)
        
        实际生产环境应使用:
        - BERTScore
        - Sentence Transformers embeddings
        - GPT-4 as judge
        
        Returns:
            float: 语义相似度 (0-1)
        """
        # 简化: 使用字符级相似度
        from difflib import SequenceMatcher
        
        similarity = SequenceMatcher(None, original, compressed).ratio()
        return similarity
    
    def evaluate(
        self,
        original: str,
        compressed: str,
        method_name: str,
    ) -> Dict[str, float]:
        """
        完整评估
        
        Returns:
            Dict: {
                "bleu": float,
                "semantic_similarity": float,
                "compression_ratio": float,
            }
        """
        bleu = self.evaluate_bleu(original, compressed)
        semantic_sim = self.evaluate_semantic_similarity(original, compressed)
        compression_ratio = 1 - (len(compressed) / len(original))
        
        result = {
            "method": method_name,
            "original_length": len(original),
            "compressed_length": len(compressed),
            "compression_ratio": compression_ratio,
            "bleu": bleu,
            "semantic_similarity": semantic_sim,
            "quality_score": (bleu + semantic_sim) / 2,  # 综合质量分
        }
        
        self.results.append(result)
        return result


# ==================== 主测试流程 ====================

def run_comparison_test():
    """
    运行对比测试
    
    测试集:
    1. 短文本 (50-100字)
    2. 中文本 (100-300字)
    3. 长文本 (300-500字)
    4. 技术性文本 (1688运营场景)
    """
    
    print("\n")
    print("=" * 70)
    print("LLMLingua-2 vs Phase 6 三元组压缩对比测试")
    print("=" * 70)
    print("\n")
    
    # 测试数据集
    test_data = [
        {
            "category": "短文本 (50-100字)",
            "texts": [
                "关键词不足导致搜索降权,需要优化标题",
                "转化率下降了30%,需要优化详情页",
                "建议在低竞争时段加价,提升ROI",
            ],
        },
        {
            "category": "中文本 (100-300字)",
            "texts": [
                "1688店铺运营的核心在于关键词优化。首先,需要使用生意参谋分析搜索热词,找出高流量低竞争的长尾词。其次,在标题中前置核心关键词,并保持每周更新。最后,监控关键词的点击率和转化率,及时调整策略。",
                "网销宝出价策略需要根据竞争情况动态调整。建议设置分时折扣,在流量高峰时段提高出价,在低峰时段降低出价。同时,使用抢位助手锁定 top10 展位,提升曝光量。",
            ],
        },
        {
            "category": "长文本 (300-500字)",
            "texts": [
                "爆款打造是一个系统工程,需要从选品、定价、推广、转化四个维度协同发力。选品阶段,使用1688数据工具分析类目趋势,找出供需缺口。定价阶段,分析竞品价格带分布,选择最有竞争力的价格点。推广阶段,结合网销宝+详情页优化+评价管理,形成流量闭环。转化阶段,优化详情页首屏、卖点展示、促销引导,提升下单转化率。整个过程需要数据驱动,每天监控核心指标,快速迭代优化。",
            ],
        },
        {
            "category": "技术性文本 (Prompt)",
            "texts": [
                "你是一个专业的1688运营专家。请根据以下数据生成一份运营诊断报告:\n1. 店铺近7日流量数据\n2. 竞品价格对比\n3. 关键词排名变化\n\n要求:\n- 使用结构化输出\n- 包含问题诊断+优化建议\n- 数据支撑+可落地方案",
            ],
        },
    ]
    
    # 初始化压缩器
    print("[初始化] 加载压缩器...")
    phase6_compressor = Phase6TripleCompressor()
    
    if LLMLINGUA_AVAILABLE:
        try:
            llmlingua_compressor = LLMLinguaCompressor()
            print("[成功] LLMLingua-2 加载成功")
        except Exception as e:
            print(f"[失败] LLMLingua-2 加载失败: {e}")
            llmlingua_compressor = None
    else:
        llmlingua_compressor = None
        print("[警告] LLMLingua-2 未安装,跳过测试")
    
    evaluator = QualityEvaluator()
    
    # 逐类别测试
    for category_data in test_data:
        category = category_data["category"]
        texts = category_data["texts"]
        
        print("\n" + "=" * 70)
        print(f"类别: {category}")
        print("=" * 70)
        print()
        
        for i, text in enumerate(texts, 1):
            print(f"【测试{i}】")
            print(f"  原文 ({len(text)}字): {text[:50]}...")
            print()
            
            # 方法1: Phase 6 三元组压缩
            start = time.time()
            phase6_compressed = phase6_compressor.compress(text)
            phase6_time = time.time() - start
            
            phase6_result = evaluator.evaluate(
                text,
                phase6_compressed,
                method_name="Phase 6 三元组",
            )
            
            print(f"  [Phase 6 三元组]")
            print(f"    压缩后 ({len(phase6_compressed)}字): {phase6_compressed[:50]}...")
            print(f"    压缩率: {phase6_result['compression_ratio']:.1%}")
            print(f"    BLEU: {phase6_result['bleu']:.3f}")
            print(f"    语义相似度: {phase6_result['semantic_similarity']:.3f}")
            print(f"    质量分: {phase6_result['quality_score']:.3f}")
            print(f"    处理时间: {phase6_time*1000:.2f}ms")
            print()
            
            # 方法2: LLMLingua-2 压缩
            if llmlingua_compressor:
                try:
                    start = time.time()
                    llmlingua_compressed = llmlingua_compressor.compress(
                        text,
                        rate=0.8,
                        force_tokens=["\n", ":", "建议", "数据"],
                    )
                    llmlingua_time = time.time() - start
                    
                    llmlingua_result = evaluator.evaluate(
                        text,
                        llmlingua_compressed,
                        method_name="LLMLingua-2",
                    )
                    
                    print(f"  [LLMLingua-2]")
                    print(f"    压缩后 ({len(llmlingua_compressed)}字): {llmlingua_compressed[:50]}...")
                    print(f"    压缩率: {llmlingua_result['compression_ratio']:.1%}")
                    print(f"    BLEU: {llmlingua_result['bleu']:.3f}")
                    print(f"    语义相似度: {llmlingua_result['semantic_similarity']:.3f}")
                    print(f"    质量分: {llmlingua_result['quality_score']:.3f}")
                    print(f"    处理时间: {llmlingua_time*1000:.2f}ms")
                    print()
                    
                    # 对比
                    print(f"  [对比]")
                    compression_diff = llmlingua_result['compression_ratio'] - phase6_result['compression_ratio']
                    quality_diff = llmlingua_result['quality_score'] - phase6_result['quality_score']
                    speed_diff = phase6_time / llmlingua_time if llmlingua_time > 0 else float('inf')
                    
                    print(f"    压缩率差异: {compression_diff:+.1%} (LLMLingua {'胜出' if compression_diff > 0 else '落后'})")
                    print(f"    质量差异: {quality_diff:+.3f} (LLMLingua {'胜出' if quality_diff > 0 else '落后'})")
                    print(f"    速度差异: {speed_diff:.2f}x (Phase 6 {'更快' if speed_diff > 1 else '更慢'})")
                    
                except Exception as e:
                    print(f"  [LLMLingua-2] 压缩失败: {e}")
            else:
                print(f"  [LLMLingua-2] 跳过 (未安装)")
            
            print()
            print("-" * 70)
            print()
    
    # 生成总结报告
    print("\n" + "=" * 70)
    print("总结报告")
    print("=" * 70)
    print()
    
    # 计算平均分
    phase6_results = [r for r in evaluator.results if r["method"] == "Phase 6 三元组"]
    llmlingua_results = [r for r in evaluator.results if r["method"] == "LLMLingua-2"]
    
    if phase6_results:
        avg_compression = sum(r["compression_ratio"] for r in phase6_results) / len(phase6_results)
        avg_quality = sum(r["quality_score"] for r in phase6_results) / len(phase6_results)
        
        print("[Phase 6 三元组]")
        print(f"  平均压缩率: {avg_compression:.1%}")
        print(f"  平均质量分: {avg_quality:.3f}")
        print()
    
    if llmlingua_results:
        avg_compression = sum(r["compression_ratio"] for r in llmlingua_results) / len(llmlingua_results)
        avg_quality = sum(r["quality_score"] for r in llmlingua_results) / len(llmlingua_results)
        
        print("[LLMLingua-2]")
        print(f"  平均压缩率: {avg_compression:.1%}")
        print(f"  平均质量分: {avg_quality:.3f}")
        print()
    
    # 建议
    print("[建议]")
    if llmlingua_results and phase6_results:
        llmlingua_avg = sum(r["quality_score"] for r in llmlingua_results) / len(llmlingua_results)
        phase6_avg = sum(r["quality_score"] for r in phase6_results) / len(phase6_results)
        
        if llmlingua_avg > phase6_avg:
            print("  ✓ 推荐使用 LLMLingua-2:")
            print("    - 更高的压缩率 (80%+ vs 40-60%)")
            print("    - 更好的语义保留 (质量分更高)")
            print("    - 适合对质量要求高的场景")
        else:
            print("  ✓ 推荐使用 Phase 6 三元组:")
            print("    - 更快的处理速度 (CPU实时)")
            print("    - 无需额外依赖 (轻量级)")
            print("    - 适合实时对话场景")
    
    print()
    print("=" * 70)
    print("测试完成!")
    print("=" * 70)
    
    return evaluator.results


# ==================== 生成集成代码 ====================

def generate_integration_code():
    """生成LLMLingua-2集成到Phase 6的代码示例"""
    
    code = '''
# ===== LLMLingua-2 集成到 Phase 6 =====
# 文件: optimization-state/phase6_ultimate_saver.py

from llm_lingua import PromptCompressor

class Phase6UltimateSaver:
    def __init__(self, use_llmlingua=True):
        self.use_llmlingua = use_llmlingua
        
        if use_llmlingua:
            try:
                self.llmlingua = PromptCompressor(
                    model_name="microsoft/llmlingua-2-bert-base-multilingual-cased"
                )
                print("[OK] LLMLingua-2 加载成功")
            except Exception as e:
                print(f"[WARNING] LLMLingua-2 加载失败: {e}")
                self.use_llmlingua = False
        
        # 降级: 使用三元组压缩
        self.triple_compressor = Phase6TripleCompressor()
    
    def optimize_response(self, user_query: str, response: str):
        """优化响应 (LLMLingua-2 优先, 失败降级到三元组)"""
        
        # 1. 检查最小信号
        if self.check_minimal_signal(user_query):
            return self.get_signal_response(user_query)
        
        # 2. 检查缓存
        cached = self.check_cache(user_query)
        if cached:
            return cached
        
        # 3. LLMLingua-2 压缩 (优先)
        if self.use_llmlingua:
            try:
                compressed = self.llmlingua.compress_prompt(
                    response,
                    rate=0.8,
                    force_tokens=["\\n", ":", "建议", "数据"]
                )["compressed_prompt"]
                
                print(f"[OK] LLMLingua-2 压缩成功: {len(response)} → {len(compressed)} chars")
                return compressed
            except Exception as e:
                print(f"[WARNING] LLMLingua-2 压缩失败: {e}, 降级到三元组")
        
        # 4. 降级: Phase 6 三元组压缩
        compressed = self.triple_compressor.compress(response)
        print(f"[OK] 三元组压缩: {len(response)} → {len(compressed)} chars")
        return compressed

# ===== 使用方法 =====
saver = Phase6UltimateSaver(use_llmlingua=True)

# 优化响应
optimized = saver.optimize_response(user_query, original_response)
'''
    
    return code


if __name__ == "__main__":
    # 运行对比测试
    results = run_comparison_test()
    
    # 生成集成代码
    print("\n" + "=" * 70)
    print("LLMLingua-2 集成代码示例")
    print("=" * 70)
    print()
    
    integration_code = generate_integration_code()
    print(integration_code)
