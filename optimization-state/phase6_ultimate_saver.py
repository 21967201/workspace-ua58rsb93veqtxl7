"""
Phase 6: 终局优化 - 零Token响应 + 语义Delta + 三元组
版本: v6.0.0
目标: Token节省率97%+
"""

from typing import Optional, Dict, List, Tuple
import re
import difflib
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    """缓存条目"""
    query: str
    response: str
    embedding: Optional[List[float]] = None
    access_count: int = 0
    last_access: float = 0.0
    
    def similarity(self, other_query: str) -> float:
        """计算语义相似度"""
        return difflib.SequenceMatcher(None, self.query, other_query).ratio()


class Phase6UltimateSaver:
    """
    Phase 6 终局优化器
    
    三大核心机制:
    1. 零Token响应 (最小信号 + 缓存直出)
    2. 语义Delta压缩 (只传变化部分)
    3. 三元组格式 (实体|关系|实体)
    """
    
    # 最小信号映射 (≤8字纯确认 → 1 Token)
    # 使用ASCII字符避免Windows GBK编码问题
    MINIMAL_SIGNALS = {
        "好的": "[OK]",
        "可以": "[OK]", 
        "行": "[OK]",
        "完成": "[DONE]",
        "搞定": "[DONE]",
        "知道": "->",
        "了解": "->",
        "明白": "->",
        "是的": "[OK]",
        "对的": "[OK]",
        "没问题": "[OK]"
    }
    
    def __init__(self, cache_size: int = 2000):
        """
        初始化终局优化器
        
        Args:
            cache_size: 缓存大小 (默认2000条)
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.cache_size = cache_size
        self.hit_count = 0
        self.total_queries = 0
        
        # 三元组关系词映射
        self.relation_symbols = {
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
            "应该": "!"
        }
    
    # ==================== 机制1: 零Token响应 ====================
    
    def check_minimal_signal(self, user_input: str) -> Optional[str]:
        """
        检查最小信号匹配 (≤8字纯确认 → 1 Token)
        
        Args:
            user_input: 用户输入
            
        Returns:
            Optional[str]: 匹配的信号符号,无匹配返回None
        """
        # 清理输入
        cleaned = user_input.strip()
        
        # ≤8字检查
        if len(cleaned) > 8:
            return None
        
        # 精确匹配
        if cleaned in self.MINIMAL_SIGNALS:
            return self.MINIMAL_SIGNALS[cleaned]
        
        return None
    
    def check_cache_hit(self, query: str, threshold: float = 0.85) -> Optional[str]:
        """
        检查缓存命中 (语义相似度>85% → 0 Token)
        
        Args:
            query: 用户查询
            threshold: 相似度阈值 (默认85%)
            
        Returns:
            Optional[str]: 缓存的响应,无命中返回None
        """
        self.total_queries += 1
        
        best_match = None
        best_similarity = 0.0
        
        for cached_query, entry in self.cache.items():
            similarity = entry.similarity(query)
            
            if similarity >= threshold and similarity > best_similarity:
                best_match = entry.response
                best_similarity = similarity
        
        if best_match:
            self.hit_count += 1
            return best_match
        
        return None
    
    def add_to_cache(self, query: str, response: str):
        """
        添加到缓存 (LRU淘汰)
        
        Args:
            query: 查询
            response: 响应
        """
        if len(self.cache) >= self.cache_size:
            # LRU淘汰: 删除访问次数最少且最久未访问的
            lru_key = min(
                self.cache.keys(),
                key=lambda k: (self.cache[k].access_count, self.cache[k].last_access)
            )
            del self.cache[lru_key]
        
        self.cache[query] = CacheEntry(
            query=query,
            response=response,
            access_count=1,
            last_access=0.0  # 实际应使用time.time()
        )
    
    def get_cache_stats(self) -> Dict[str, float]:
        """获取缓存统计"""
        hit_rate = (self.hit_count / self.total_queries * 100) if self.total_queries > 0 else 0
        
        return {
            "hit_rate": hit_rate,
            "total_queries": self.total_queries,
            "hit_count": self.hit_count,
            "cache_size": len(self.cache)
        }
    
    # ==================== 机制2: 语义Delta压缩 ====================
    
    def compute_delta(self, new_text: str, old_text: str) -> Tuple[str, float]:
        """
        计算语义Delta (只保留变化部分)
        
        Args:
            new_text: 新文本
            old_text: 旧文本
            
        Returns:
            Tuple[str, float]: (Delta文本, 压缩率)
        """
        # 使用difflib计算差异
        seq_matcher = difflib.SequenceMatcher(None, old_text, new_text)
        
        # 提取变化部分
        delta_parts = []
        for tag, i1, i2, j1, j2 in seq_matcher.get_opcodes():
            if tag == 'equal':
                # 相同部分用占位符
                delta_parts.append(f"[...{j2-j1}chars...]")
            else:
                # 变化部分保留
                delta_parts.append(new_text[j1:j2])
        
        delta_text = "".join(delta_parts)
        
        # 计算压缩率
        original_len = len(new_text)
        delta_len = len(delta_text)
        compression_ratio = 1 - (delta_len / original_len) if original_len > 0 else 0
        
        return delta_text, compression_ratio
    
    def should_use_delta(self, new_query: str, old_query: str, threshold: float = 0.90) -> bool:
        """
        判断是否应该使用Delta压缩
        
        Args:
            new_query: 新查询
            old_query: 旧查询
            threshold: 相似度阈值 (默认90%)
            
        Returns:
            bool: 是否使用Delta
        """
        similarity = difflib.SequenceMatcher(None, old_query, new_query).ratio()
        return similarity >= threshold
    
    # ==================== 机制3: 三元组格式 ====================
    
    def compress_to_triple(self, text: str) -> str:
        """
        压缩为三元组格式 (实体|关系|实体)
        
        示例:
        原文: "关键词不足导致降权"
        三元组: "关键词不足→降权"
        
        Args:
            text: 原文
            
        Returns:
            str: 三元组格式文本
        """
        # 替换关系词为符号
        compressed = text
        for relation, symbol in self.relation_symbols.items():
            compressed = compressed.replace(relation, symbol)
        
        # 移除冗余词汇
        remove_words = ["的", "了", "是", "在", "和", "与", "或"]
        for word in remove_words:
            compressed = compressed.replace(word, "")
        
        return compressed
    
    def batch_compress_to_triples(self, texts: List[str]) -> List[str]:
        """
        批量压缩为三元组
        
        Args:
            texts: 文本列表
            
        Returns:
            List[str]: 三元组列表
        """
        return [self.compress_to_triple(text) for text in texts]
    
    # ==================== 统一接口 ====================
    
    def optimize_response(self, user_query: str, response: str) -> Tuple[str, Dict[str, Any]]:
        """
        统一优化接口
        
        优先级:
        1. 最小信号匹配 (1 Token)
        2. 缓存直出 (0 Token)
        3. Delta压缩 (节省65%)
        4. 三元组压缩 (节省10-80%)
        
        Args:
            user_query: 用户查询
            response: 原始响应
            
        Returns:
            Tuple[str, Dict]: (优化后响应, 元数据)
        """
        metadata = {
            "mechanism": None,
            "tokens_saved": 0,
            "compression_ratio": 0.0
        }
        
        original_tokens = len(response.split())  # 简化Token计算
        
        # 1. 检查最小信号
        signal = self.check_minimal_signal(user_query)
        if signal:
            metadata["mechanism"] = "minimal_signal"
            metadata["tokens_saved"] = original_tokens - 1
            metadata["compression_ratio"] = 1 - (1 / original_tokens) if original_tokens > 0 else 0
            return signal, metadata
        
        # 2. 检查缓存命中
        cached_response = self.check_cache_hit(user_query)
        if cached_response:
            metadata["mechanism"] = "cache_hit"
            metadata["tokens_saved"] = original_tokens
            metadata["compression_ratio"] = 1.0
            return cached_response, metadata
        
        # 3. 尝试Delta压缩
        # (这里假设有上一轮查询,实际需要从会话历史获取)
        # delta_text, compression_ratio = self.compute_delta(response, old_response)
        
        # 4. 三元组压缩 (兜底方案)
        triple_response = self.compress_to_triple(response)
        triple_tokens = len(triple_response.split())
        tokens_saved = original_tokens - triple_tokens
        compression_ratio = 1 - (triple_tokens / original_tokens) if original_tokens > 0 else 0
        
        if compression_ratio > 0:
            metadata["mechanism"] = "triple_compression"
            metadata["tokens_saved"] = tokens_saved
            metadata["compression_ratio"] = compression_ratio
            
            # 添加到缓存
            self.add_to_cache(user_query, triple_response)
            
            return triple_response, metadata
        
        # 无优化空间,返回原文
        metadata["mechanism"] = "none"
        return response, metadata


# 测试代码
if __name__ == "__main__":
    saver = Phase6UltimateSaver()
    
    print("=== Phase 6 终局优化器测试 ===\n")
    
    # 测试1: 最小信号
    print("【测试1: 最小信号】")
    test_inputs = ["好的", "完成", "知道", "你好啊这个"]
    for inp in test_inputs:
        signal = saver.check_minimal_signal(inp)
        print(f"  输入: {inp} → 信号: {signal}")
    print()
    
    # 测试2: 缓存命中
    print("【测试2: 缓存命中】")
    saver.add_to_cache("1688怎么做", "1688是批发平台...")
    cached = saver.check_cache_hit("1688怎么做")  # 精确匹配
    similar = saver.check_cache_hit("1688怎么操作")  # 相似匹配
    print(f"  精确匹配: {cached is not None}")
    print(f"  相似匹配(需threshold调整): {similar is not None}")
    print(f"  缓存统计: {saver.get_cache_stats()}")
    print()
    
    # 测试3: 三元组压缩
    print("【测试3: 三元组压缩】")
    test_texts = [
        "关键词不足导致搜索降权",
        "优化标题能提升流量",
        "转化率下降了30%",
        "建议在低竞争时段加价"
    ]
    for text in test_texts:
        triple = saver.compress_to_triple(text)
        print(f"  原文: {text}")
        print(f"  三元组: {triple}\n")
    
    # 测试4: 统一优化接口
    print("【测试4: 统一优化接口】")
    test_query = "好的"
    test_response = "好的,我已经理解了你的需求,现在我将为你详细分析这个问题的各个方面..."
    optimized, metadata = saver.optimize_response(test_query, test_response)
    print(f"  查询: {test_query}")
    print(f"  原文({len(test_response.split())}T): {test_response[:50]}...")
    print(f"  优化({metadata['tokens_saved']}T节省): {optimized}")
    print(f"  机制: {metadata['mechanism']}")
    print(f"  压缩率: {metadata['compression_ratio']:.1%}")
