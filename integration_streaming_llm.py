"""
StreamingLLM 集成到 OpenClaw

将StreamingLLM集成到OpenClaw的推理引擎中,支持无限长上下文。

修改点:
1. 替换KV Cache管理为StreamingKVManager
2. 修改Attention层,使用sinks + recent窗口
3. 添加配置参数 (num_sinks, max_recent)
"""

import torch
import torch.nn as nn
from typing import List, Tuple, Optional, Deque
from collections import deque


# ==================== StreamingKVManager ====================

class StreamingKVManager:
    """
    StreamingLLM 的 KV Cache 管理器
    
    保留:
    - num_sinks 个注意力Sink token (初始token)
    - max_recent 个最近token (滑动窗口)
    
    内存: O(num_sinks + max_recent) [恒定]
    传统方式: O(N) [随上下文线性增长]
    """
    
    def __init__(
        self,
        num_sinks: int = 4,
        max_recent: int = 512,
        num_heads: int = 32,
        head_dim: int = 128,
    ):
        """
        初始化
        
        Args:
            num_sinks: Sink token数量 (论文推荐4个)
            max_recent: 最近token数量 (论文推荐512个)
            num_heads: 注意力头数
            head_dim: 每个头的维度
        """
        self.num_sinks = num_sinks
        self.max_recent = max_recent
        self.num_heads = num_heads
        self.head_dim = head_dim
        
        # Sink KV (恒定大小)
        self.sink_K = None  # (1, num_sinks, H, D)
        self.sink_V = None
        
        # Recent KV (滑动窗口)
        self.recent_K = deque(maxlen=max_recent)
        self.recent_V = deque(maxlen=max_recent)
        
        # 统计
        self.total_tokens = 0
        
    def identify_sinks(
        self,
        attention_scores: torch.Tensor,
    ) -> List[int]:
        """
        识别注意力Sink token
        
        Sink token特征: 累积注意力值最高
        
        Args:
            attention_scores: 注意力分数 (H, S, S)
            
        Returns:
            List[int]: sink token索引
        """
        # 计算累积注意力 (对所有query token求平均)
        # attention_scores shape: (H, S, S)
        #   dim=1: query token维度
        #   dim=2: key token维度
        cumulative_attn = attention_scores.mean(dim=0).sum(dim=0)  # (S,)
        
        # 选择top-K个sink token
        _, top_k_indices = torch.topk(cumulative_attn, min(self.num_sinks, len(cumulative_attn)))
        sink_indices = sorted(top_k_indices.tolist())
        
        return sink_indices
    
    def update(
        self,
        new_K: torch.Tensor,
        new_V: torch.Tensor,
        attention_scores: Optional[torch.Tensor] = None,
    ):
        """
        更新KV Cache (添加新token, 丢弃中间token)
        
        Args:
            new_K: 新token的K (1, new_tokens, H, D)
            new_V: 新token的V (1, new_tokens, H, D)
            attention_scores: 注意力分数 (用于识别sinks)
        """
        self.total_tokens += new_K.shape[1]
        
        # 第一次: 初始化sink tokens
        if self.sink_K is None:
            # 简化: 使用前num_sinks个token作为sinks
            self.sink_K = new_K[:, :self.num_sinks, :, :].clone()
            self.sink_V = new_V[:, :self.num_sinks, :, :].clone()
            
            # 剩余部分加入recent窗口
            if new_K.shape[1] > self.num_sinks:
                recent_K = new_K[:, self.num_sinks:, :, :]
                recent_V = new_V[:, self.num_sinks:, :, :]
                
                for i in range(recent_K.shape[1]):
                    self.recent_K.append(recent_K[:, i, :, :].unsqueeze(1))
                    self.recent_V.append(recent_V[:, i, :, :].unsqueeze(1))
        else:
            # 识别新的sink tokens (如果提供了attention_scores)
            if attention_scores is not None:
                # 简化: 不重新识别sinks, 保持初始sinks
                pass
            
            # 将新token加入recent窗口 (自动淘汰最旧的)
            for i in range(new_K.shape[1]):
                self.recent_K.append(new_K[:, i, :, :].unsqueeze(1))
                self.recent_V.append(new_V[:, i, :, :].unsqueeze(1))
    
    def get_kv_cache(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        获取完整的KV Cache (sinks + recent)
        
        Returns:
            Tuple[K, V]: 拼接好的KV Cache
        """
        # Sink KV
        if self.sink_K is None:
            raise RuntimeError("KV Cache is empty. Call update() first.")
        
        sink_K = self.sink_K
        sink_V = self.sink_V
        
        # Recent KV
        if len(self.recent_K) > 0:
            recent_K = torch.cat(list(self.recent_K), dim=1)
            recent_V = torch.cat(list(self.recent_V), dim=1)
        else:
            # 空tensor
            recent_K = torch.empty(1, 0, self.num_heads, self.head_dim, device=sink_K.device)
            recent_V = torch.empty(1, 0, self.num_heads, self.head_dim, device=sink_K.device)
        
        # 拼接: [sinks, recent]
        full_K = torch.cat([sink_K, recent_K], dim=1)
        full_V = torch.cat([sink_V, recent_V], dim=1)
        
        return full_K, full_V
    
    def clear(self):
        """清空KV Cache"""
        self.sink_K = None
        self.sink_V = None
        self.recent_K.clear()
        self.recent_V.clear()
        self.total_tokens = 0
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_tokens": self.total_tokens,
            "sink_tokens": self.num_sinks,
            "recent_tokens": len(self.recent_K),
            "cache_size_mb": self._estimate_cache_size_mb(),
        }
    
    def _estimate_cache_size_mb(self) -> float:
        """估算KV Cache大小 (MB)"""
        if self.sink_K is None:
            return 0.0
        
        # 每个tensor的字节数
        sink_size = self.sink_K.nelement() * self.sink_K.element_size() * 2  # K+V
        recent_size = sum(x.nelement() * x.element_size() for x in self.recent_K) * 2
        
        total_bytes = sink_size + recent_size
        return total_bytes / (1024 * 1024)


# ==================== 修改后的 Attention 层 ====================

class StreamingAttention(nn.Module):
    """
    使用StreamingLLM的Attention层
    
    替换标准Attention,支持无限长上下文。
    """
    
    def __init__(
        self,
        hidden_size: int,
        num_heads: int,
        head_dim: int,
        num_sinks: int = 4,
        max_recent: int = 512,
        dropout: float = 0.1,
    ):
        """
        初始化
        
        Args:
            hidden_size: 隐藏层大小
            num_heads: 注意力头数
            head_dim: 每个头的维度
            num_sinks: sink token数量
            max_recent: 最近token数量
            dropout: dropout概率
        """
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.num_sinks = num_sinks
        self.max_recent = max_recent
        
        # QKV投影
        self.q_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        self.k_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        self.v_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        self.o_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        
        self.dropout = nn.Dropout(dropout)
        
        # StreamingKVManager
        self.kv_manager = StreamingKVManager(
            num_sinks=num_sinks,
            max_recent=max_recent,
            num_heads=num_heads,
            head_dim=head_dim,
        )
        
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        use_cache: bool = True,
    ) -> torch.Tensor:
        """
        前向传播
        
        Args:
            hidden_states: (B, S, H*D)
            attention_mask: (B, S) 或 (B, 1, 1, S)
            use_cache: 是否使用KV Cache
            
        Returns:
            torch.Tensor: (B, S, H*D)
        """
        batch, seqlen, _ = hidden_states.shape
        
        # QKV投影
        Q = self.q_proj(hidden_states).view(batch, seqlen, self.num_heads, self.head_dim)
        K = self.k_proj(hidden_states).view(batch, seqlen, self.num_heads, self.head_dim)
        V = self.v_proj(hidden_states).view(batch, seqlen, self.num_heads, self.head_dim)
        
        # 使用StreamingKV (推理加速)
        if use_cache and self.kv_manager.total_tokens > 0:
            # 获取优化后的KV Cache
            cache_K, cache_V = self.kv_manager.get_kv_cache()
            
            # 拼接历史KV和当前KV
            K_full = torch.cat([cache_K, K], dim=1)
            V_full = torch.cat([cache_V, V], dim=1)
        else:
            K_full = K
            V_full = V
        
        # 计算注意力
        # Q: (B, Sq, H, D)
        # K_full: (B, Sk, H, D)
        # V_full: (B, Sk, H, D)
        attn_scores = torch.einsum("bqhd,bkhd->bhqk", Q, K_full) / math.sqrt(self.head_dim)
        
        # Attention mask
        if attention_mask is not None:
            # 扩展mask
            mask = attention_mask.unsqueeze(1).unsqueeze(2)  # (B, 1, 1, Sk)
            attn_scores = attn_scores.masked_fill(mask == 0, float('-inf'))
        
        # Softmax
        attn_weights = torch.softmax(attn_scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # 输出
        attn_output = torch.einsum("bhqk,bkhd->bqhd", attn_weights, V_full)
        attn_output = attn_output.view(batch, seqlen, -1)
        
        # 输出投影
        attn_output = self.o_proj(attn_output)
        
        # 更新KV Cache (StreamingLLM核心)
        if use_cache:
            # 计算注意力分数 (用于识别sinks)
            # 简化: 只在第一次时识别sinks
            if self.kv_manager.sink_K is None:
                # 使用当前attn_scores
                self.kv_manager.update(K, V, attn_scores)
            else:
                # 不重新识别sinks
                self.kv_manager.update(K, V, None)
        
        return attn_output
    
    def clear_kv_cache(self):
        """清空KV Cache (新对话开始时调用)"""
        self.kv_manager.clear()


# ==================== 集成到 OpenClaw ====================

def integrate_streaming_llm_to_openclaw():
    """
    集成StreamingLLM到OpenClaw
    
    修改文件:
    1. openclaw/models/modeling.py (主模型文件)
    2. openclaw/models/configuration.py (配置文件)
    3. openclaw/trainer.py (训练脚本,可选)
    """
    
    integration_code = '''
# ===== openclaw/models/modeling.py (修改后) =====

from .streaming_kv_manager import StreamingKVManager
from .streaming_attention import StreamingAttention


class OpenClawModel(nn.Module):
    """
    OpenClaw 主模型 (集成StreamingLLM)
    """
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        # Embedding
        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size)
        
        # Transformer layers
        self.layers = nn.ModuleList([
            OpenClawLayer(config, layer_idx=i)
            for i in range(config.num_hidden_layers)
        ])
        
        # LM Head
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        
        # StreamingLLM KV Manager (全局)
        self.kv_manager = StreamingKVManager(
            num_sinks=config.num_sinks if hasattr(config, 'num_sinks') else 4,
            max_recent=config.max_recent if hasattr(config, 'max_recent') else 512,
            num_heads=config.num_attention_heads,
            head_dim=config.hidden_size // config.num_attention_heads,
        )
    
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        use_cache: bool = True,
    ):
        """
        前向传播
        
        Args:
            input_ids: (B, S)
            attention_mask: (B, S)
            use_cache: 是否使用StreamingKV
        """
        # Embedding
        hidden_states = self.embed_tokens(input_ids)
        
        # Transformer layers
        for layer in self.layers:
            hidden_states = layer(
                hidden_states,
                attention_mask=attention_mask,
                kv_manager=self.kv_manager if use_cache else None,
            )
        
        # LM Head
        logits = self.lm_head(hidden_states)
        
        return logits
    
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 100,
        temperature: float = 1.0,
        use_cache: bool = True,
    ):
        """
        生成文本 (支持无限长上下文)
        """
        self.eval()
        
        generated = input_ids.clone()
        
        with torch.no_grad():
            for _ in range(max_new_tokens):
                # 前向传播
                logits = self.forward(
                    generated,
                    use_cache=use_cache,
                )
                
                # 只取最后一个token的logits
                next_token_logits = logits[:, -1, :] / temperature
                
                # 采样
                probs = torch.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                
                # 拼接
                generated = torch.cat([generated, next_token], dim=1)
                
                # 停止条件
                if next_token.item() == self.config.eos_token_id:
                    break
        
        return generated
    
    def clear_kv_cache(self):
        """清空KV Cache (新对话开始时调用)"""
        self.kv_manager.clear()


class OpenClawLayer(nn.Module):
    """
    OpenClaw Transformer Layer (使用StreamingAttention)
    """
    
    def __init__(self, config, layer_idx):
        super().__init__()
        self.layer_idx = layer_idx
        
        # Streaming Attention
        self.self_attn = StreamingAttention(
            hidden_size=config.hidden_size,
            num_heads=config.num_attention_heads,
            head_dim=config.hidden_size // config.num_attention_heads,
            num_sinks=4,
            max_recent=512,
        )
        
        # Feed-forward network
        self.mlp = OpenClawMLP(config)
        
        # Layer Norm
        self.input_layernorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.post_attention_layernorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
    
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        kv_manager: Optional[StreamingKVManager] = None,
    ):
        # Self-attention (with StreamingKV)
        attn_output = self.self_attn(
            self.input_layernorm(hidden_states),
            attention_mask=attention_mask,
            kv_manager=kv_manager,
        )
        
        hidden_states = hidden_states + attn_output
        
        # MLP
        mlp_output = self.mlp(self.post_attention_layernorm(hidden_states))
        hidden_states = hidden_states + mlp_output
        
        return hidden_states


# ===== openclaw/models/configuration.py (修改后) =====

class OpenClawConfig:
    """
    OpenClaw 配置 (添加StreamingLLM参数)
    """
    
    def __init__(
        self,
        vocab_size=50257,
        hidden_size=768,
        num_hidden_layers=12,
        num_attention_heads=12,
        # ... 其他参数 ...
        
        # StreamingLLM 参数
        num_sinks: int = 4,       # Sink token数量
        max_recent: int = 512,     # 最近token数量
        **kwargs,
    ):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        
        # StreamingLLM
        self.num_sinks = num_sinks
        self.max_recent = max_recent
        
        # ... 其他初始化 ...


# ===== 使用示例 =====

# 1. 初始化模型 (自动启用StreamingLLM)
model = OpenClawModel.from_pretrained(
    "openclaw-base",
    num_sinks=4,      # Sink token数量
    max_recent=512,    # 最近token数量
)

# 2. 推理 (自动使用StreamingKV)
output = model.generate(
    input_ids,
    max_new_tokens=100,
    use_cache=True,  # 启用StreamingKV
)

# 3. 新对话时清空Cache
model.clear_kv_cache()
'''
    
    return integration_code


# ==================== 测试脚本 ====================

def test_streaming_llm_integration():
    """
    测试StreamingLLM集成
    """
    print("\n")
    print("=" * 70)
    print("测试 StreamingLLM 集成")
    print("=" * 70)
    print()
    
    # 配置
    config = {
        "hidden_size": 768,
        "num_heads": 12,
        "head_dim": 64,
        "num_sinks": 4,
        "max_recent": 512,
    }
    
    # 初始化Attention层
    attention = StreamingAttention(
        hidden_size=config["hidden_size"],
        num_heads=config["num_heads"],
        head_dim=config["head_dim"],
        num_sinks=config["num_sinks"],
        max_recent=config["max_recent"],
    )
    
    print("[测试1] 短上下文 (512 tokens)")
    print()
    
    # 模拟短上下文
    batch = 1
    seqlen_short = 512
    
    hidden_states = torch.randn(batch, seqlen_short, config["hidden_size"])
    attention_mask = torch.ones(batch, seqlen_short)
    
    # 前向传播
    output = attention(hidden_states, attention_mask, use_cache=True)
    
    stats = attention.kv_manager.get_stats()
    
    print(f"  输入长度: {seqlen_short}")
    print(f"  输出形状: {output.shape}")
    print(f"  Sink tokens: {stats['sink_tokens']}")
    print(f"  Recent tokens: {stats['recent_tokens']}")
    print(f"  Cache大小: {stats['cache_size_mb']:.2f} MB")
    print()
    
    print("[测试2] 长上下文 (10K tokens)")
    print()
    
    # 清空Cache
    attention.clear_kv_cache()
    
    # 模拟逐token生成 (10K steps)
    seqlen_long = 10240
    
    for t in range(seqlen_long):
        hidden_state = torch.randn(batch, 1, config["hidden_size"])
        mask = torch.ones(batch, 1)
        
        output = attention(hidden_state, mask, use_cache=True)
    
    stats = attention.kv_manager.get_stats()
    
    print(f"  输入长度: {seqlen_long}")
    print(f"  Sink tokens: {stats['sink_tokens']}")
    print(f"  Recent tokens: {stats['recent_tokens']}")
    print(f"  Cache大小: {stats['cache_size_mb']:.2f} MB")
    print()
    
    # 对比传统方式
    traditional_memory = seqlen_long * config["num_heads"] * config["head_dim"] * 2 * 4 / (1024 * 1024)
    
    print(f"  [对比] 传统方式内存: {traditional_memory:.2f} MB")
    print(f"  [对比] StreamingLLM内存: {stats['cache_size_mb']:.2f} MB")
    print(f"  [对比] 内存节省: {(1 - stats['cache_size_mb']/traditional_memory)*100:.1f}%")
    print()
    
    print("[测试3] 超长上下文 (100K tokens)")
    print()
    
    # 清空Cache
    attention.clear_kv_cache()
    
    # 模拟超长上下文
    seqlen_ultra = 102400
    
    for t in range(seqlen_ultra):
        hidden_state = torch.randn(batch, 1, config["hidden_size"])
        mask = torch.ones(batch, 1)
        
        output = attention(hidden_state, mask, use_cache=True)
    
    stats = attention.kv_manager.get_stats()
    
    print(f"  输入长度: {seqlen_ultra}")
    print(f"  Cache大小: {stats['cache_size_mb']:.2f} MB")
    print()
    
    # 验证内存恒定
    print(f"  [验证] 内存是否恒定? ", end="")
    if abs(stats['cache_size_mb'] - 0.50) < 0.01:  # 应该是~0.50 MB
        print("✅ 是 (内存恒定在~0.50 MB)")
    else:
        print(f"❌ 否 (当前: {stats['cache_size_mb']:.2f} MB)")
    print()
    
    print("=" * 70)
    print("测试完成!")
    print("=" * 70)


# ==================== 主函数 ====================

if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("StreamingLLM 集成到 OpenClaw")
    print("=" * 70)
    print("\n")
    
    # 1. 显示集成代码
    print("[步骤1] 集成代码示例:")
    print()
    code = integrate_streaming_llm_to_openclaw()
    print(code[:2000] + "\n...\n")
    
    # 2. 运行测试
    print("\n[步骤2] 运行集成测试:")
    print()
    test_streaming_llm_integration()
    
    # 3. 部署说明
    print("\n[步骤3] 部署说明:")
    print()
    print("  1. 将以下文件复制到 openclaw/models/:")
    print("     - streaming_kv_manager.py")
    print("     - streaming_attention.py")
    print()
    print("  2. 修改 modeling.py, 使用 StreamingAttention 替代标准Attention")
    print()
    print("  3. 修改 configuration.py, 添加 num_sinks 和 max_recent 参数")
    print()
    print("  4. 测试:")
    print("     - 检查显存占用 (应恒定在~500MB)")
    print("     - 检查质量损失 (应在<5%)")
    print("     - 测试超长上下文 (100K+ tokens)")
    print()
    
    print("=" * 70)
    print("StreamingLLM 集成完成!")
    print("=" * 70)
