"""
OpenClaw Token Optimizer 集成层
将Phase 5+6优化器集成到OpenClaw架构

集成点:
1. 响应生成前 → Phase 6 零Token检查
2. 工具调用前 → Phase 5 预算检查
3. 响应生成后 → Phase 6 Delta/三元组压缩
4. 会话结束 → Token银行结算
"""

from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass, field
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phase5_token_budget_controller import Phase5BudgetController, TaskLevel
from phase6_ultimate_saver import Phase6UltimateSaver


@dataclass
class OptimizationContext:
    """优化上下文"""
    user_query: str
    session_id: str
    conversation_history: list[str] = field(default_factory=list)
    estimated_tokens: int = 0
    actual_tokens: int = 0
    
    # 优化元数据
    mechanism_used: Optional[str] = None
    tokens_saved: int = 0
    compression_ratio: float = 0.0


class OpenClawTokenOptimizer:
    """
    OpenClaw Token优化器主类
    
    工作流程:
    1. 接收用户查询
    2. Phase 6 零Token检查 (最小信号/缓存命中)
    3. 若未命中 → Phase 5 任务分级 + 预算检查
    4. 执行工具调用 (如有)
    5. 生成响应
    6. Phase 6 压缩优化 (Delta/三元组)
    7. 更新缓存 + Token银行结算
    """
    
    def __init__(self, initial_bank: int = 4000):
        """
        初始化优化器
        
        Args:
            initial_bank: Token银行初始额度
        """
        self.phase5 = Phase5BudgetController(initial_bank=initial_bank)
        self.phase6 = Phase6UltimateSaver(cache_size=2000)
        
        self.enabled = True
        self.stats = {
            "total_queries": 0,
            "zero_token_hits": 0,
            "budget_overruns": 0,
            "skeleton_triggers": 0,
            "total_tokens_saved": 0
        }
    
    def pre_process(self, user_query: str, conversation_history: list[str]) -> Dict[str, Any]:
        """
        预处理钩子 (在响应生成前调用)
        
        优先级:
        1. 最小信号匹配 → 1 Token响应
        2. 缓存直出 → 0 Token响应
        3. 通过 → 继续执行
        
        Args:
            user_query: 用户查询
            conversation_history: 会话历史
            
        Returns:
            Dict: {
                "should_skip_generation": bool,  # 是否跳过生成
                "optimized_response": str,        # 优化后的响应 (若跳过)
                "metadata": dict                  # 元数据
            }
        """
        if not self.enabled:
            return {"should_skip_generation": False, "optimized_response": None, "metadata": {}}
        
        self.stats["total_queries"] += 1
        
        # 1. 检查最小信号 (≤8字确认 → 1 Token)
        signal = self.phase6.check_minimal_signal(user_query)
        if signal:
            self.stats["zero_token_hits"] += 1
            return {
                "should_skip_generation": True,
                "optimized_response": signal,
                "metadata": {
                    "mechanism": "minimal_signal",
                    "tokens_saved": 100,  # 假设原响应100Token
                    "compression_ratio": 0.99
                }
            }
        
        # 2. 检查缓存命中 (相似度>85% → 0 Token)
        cached = self.phase6.check_cache_hit(user_query, threshold=0.85)
        if cached:
            self.stats["zero_token_hits"] += 1
            return {
                "should_skip_generation": True,
                "optimized_response": cached,
                "metadata": {
                    "mechanism": "cache_hit",
                    "tokens_saved": 100,
                    "compression_ratio": 1.0
                }
            }
        
        # 3. 未命中,需要正常生成
        return {"should_skip_generation": False, "optimized_response": None, "metadata": {}}
    
    def check_budget(self, user_query: str, estimated_tokens: int) -> Dict[str, Any]:
        """
        预算检查钩子 (在工具调用前调用)
        
        Args:
            user_query: 用户查询
            estimated_tokens: 预估Token消耗
            
        Returns:
            Dict: {
                "budget_ok": bool,           # 预算是否充足
                "task_level": TaskLevel,     # 任务等级
                "budget": int,              # 预算额度
                "remaining": int,           # 剩余预算
                "should_use_skeleton": bool  # 是否触发骨架模式
            }
        """
        if not self.enabled:
            return {"budget_ok": True, "task_level": None, "budget": 0, "remaining": 0, "should_use_skeleton": False}
        
        # 任务分级
        task_level = self.phase5.classify_task(user_query)
        budget = self.phase5.get_budget(task_level)
        
        # 预算检查
        is_overrun, remaining = self.phase5.check_budget(task_level, estimated_tokens)
        
        result = {
            "budget_ok": not is_overrun,
            "task_level": task_level,
            "budget": budget,
            "remaining": remaining,
            "should_use_skeleton": is_overrun
        }
        
        if is_overrun:
            self.stats["budget_overruns"] += 1
            self.stats["skeleton_triggers"] += 1
        
        return result
    
    def post_process(self, user_query: str, original_response: str, 
                     conversation_history: list[str]) -> Dict[str, Any]:
        """
        后处理钩子 (在响应生成后调用)
        
        优化策略:
        1. 尝试Delta压缩 (若上一轮有相似查询)
        2. 兜底: 三元组压缩
        3. 更新缓存
        
        Args:
            user_query: 用户查询
            original_response: 原始响应
            conversation_history: 会话历史
            
        Returns:
            Dict: {
                "optimized_response": str,  # 优化后的响应
                "metadata": dict            # 优化元数据
            }
        """
        if not self.enabled:
            return {"optimized_response": original_response, "metadata": {}}
        
        # 调用Phase 6优化
        optimized, metadata = self.phase6.optimize_response(user_query, original_response)
        
        # 更新统计
        self.stats["total_tokens_saved"] += metadata["tokens_saved"]
        
        # 若未缓存,添加当前query-response对
        if metadata["mechanism"] == "triple_compression":
            self.phase6.add_to_cache(user_query, optimized)
        
        return {
            "optimized_response": optimized,
            "metadata": metadata
        }
    
    def settlement(self, actual_tokens_used: int):
        """
        结算钩子 (在会话结束或回合结束时调用)
        
        功能:
        1. 计算本轮节省的Token
        2. 存入Token银行 (产生5%复利)
        3. 更新统计
        
        Args:
            actual_tokens_used: 实际使用的Token数
        """
        if not self.enabled:
            return
        
        # 获取本轮预算
        # (简化: 假设预算为2000)
        budget = 2000
        
        # 计算节省
        saved = max(0, budget - actual_tokens_used)
        
        # 存入银行
        if saved > 0:
            self.phase5.save_to_bank(saved)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            Dict: 统计报告
        """
        cache_stats = self.phase6.get_cache_stats()
        bank_report = self.phase5.generate_report()
        
        return {
            "optimizer_stats": self.stats,
            "cache_stats": cache_stats,
            "token_bank": bank_report,
            "overall_savings_rate": (
                self.stats["total_tokens_saved"] / (self.stats["total_queries"] * 1000) * 100
                if self.stats["total_queries"] > 0 else 0
            )
        }
    
    def enable(self):
        """启用优化器"""
        self.enabled = True
    
    def disable(self):
        """禁用优化器"""
        self.enabled = False


# ==================== OpenClaw集成示例 ====================

def integrate_with_openclaw():
    """
    OpenClaw集成示例
    
    在OpenClaw的agent.py中添加以下代码:
    """
    
    example_code = '''
# ===== OpenClaw Token Optimizer 集成代码 =====
# 在 agent.py 的顶部添加:

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "optimization-state"))
from openclaw_integration import OpenClawTokenOptimizer, OptimizationContext

# 初始化全局优化器
token_optimizer = OpenClawTokenOptimizer(initial_bank=4000)

# ===== 钩子1: 预处理 (在响应生成前) =====
def pre_response_hook(user_query: str, conversation_history: list) -> dict:
    """
    在生成响应前调用,检查是否可以零Token响应
    """
    result = token_optimizer.pre_process(user_query, conversation_history)
    
    if result["should_skip_generation"]:
        # 直接返回优化后的响应,跳过生成
        return {
            "skip_generation": True,
            "response": result["optimized_response"],
            "metadata": result["metadata"]
        }
    
    return {"skip_generation": False}

# ===== 钩子2: 预算检查 (在工具调用前) =====
def pre_tool_call_hook(user_query: str, estimated_tokens: int) -> dict:
    """
    在执行工具调用前检查预算
    """
    return token_optimizer.check_budget(user_query, estimated_tokens)

# ===== 钩子3: 后处理 (在响应生成后) =====
def post_response_hook(user_query: str, original_response: str, 
                      conversation_history: list) -> dict:
    """
    在生成响应后调用,进行压缩优化
    """
    return token_optimizer.post_process(user_query, original_response, conversation_history)

# ===== 钩子4: 结算 (在回合结束) =====
def settlement_hook(actual_tokens_used: int):
    """
    在每轮对话结束时调用,结算Token银行
    """
    token_optimizer.settlement(actual_tokens_used)

# ===== 在OpenClaw的主循环中集成 =====
# 伪代码示例:

def handle_user_message(user_query: str, history: list):
    """处理用户消息的主函数"""
    
    # 钩子1: 预处理
    pre_result = pre_response_hook(user_query, history)
    if pre_result.get("skip_generation"):
        return pre_result["response"]
    
    # 预算检查
    budget_result = pre_tool_call_hook(user_query, estimated_tokens=500)
    if not budget_result["budget_ok"]:
        # 超预算,触发骨架模式
        return generate_skeleton_response(user_query)
    
    # 正常执行工具调用 + 生成响应
    response = generate_response(user_query, history)
    
    # 钩子3: 后处理
    post_result = post_response_hook(user_query, response, history)
    optimized_response = post_result["optimized_response"]
    
    # 钩子4: 结算
    actual_tokens = count_tokens(optimized_response)
    settlement_hook(actual_tokens)
    
    return optimized_response

# ===== 获取统计信息 =====
def get_token_optimization_stats():
    """获取Token优化统计"""
    return token_optimizer.get_stats()
'''
    
    return example_code


# 测试代码
if __name__ == "__main__":
    print("=== OpenClaw Token Optimizer 集成测试 ===\n")
    
    # 初始化优化器
    optimizer = OpenClawTokenOptimizer(initial_bank=4000)
    
    # 模拟会话
    test_conversation = [
        "1688怎么做",
        "好的",
        "列举5个方法",
        "好的",
        "1688怎么做",  # 重复查询
        "详细运营报告",
        "好的"
    ]
    
    history = []
    
    for i, query in enumerate(test_conversation, 1):
        print(f"【轮次 {i}】")
        print(f"查询: {query}")
        
        # 预处理
        pre_result = optimizer.pre_process(query, history)
        
        if pre_result["should_skip_generation"]:
            print(f"✓ 零Token响应: {pre_result['optimized_response']}")
            print(f"  机制: {pre_result['metadata']['mechanism']}")
            print(f"  节省: {pre_result['metadata']['tokens_saved']}T")
        else:
            # 模拟生成响应
            mock_response = f"这是关于'{query}'的详细回答..." * 10
            
            # 后处理
            post_result = optimizer.post_process(query, mock_response, history)
            print(f"  优化后: {post_result['optimized_response'][:50]}...")
            print(f"  机制: {post_result['metadata']['mechanism']}")
            print(f"  节省: {post_result['metadata']['tokens_saved']}T")
        
        # 结算
        optimizer.settlement(actual_tokens_used=500)
        
        history.append(query)
        print()
    
    # 输出统计
    print("=== 统计报告 ===")
    stats = optimizer.get_stats()
    print(f"总查询数: {stats['optimizer_stats']['total_queries']}")
    print(f"零Token命中: {stats['optimizer_stats']['zero_token_hits']}")
    print(f"总节省Token: {stats['optimizer_stats']['total_tokens_saved']}T")
    print(f"缓存命中率: {stats['cache_stats']['hit_rate']:.1f}%")
    print(f"Token银行余额: {stats['token_bank']['current_balance']}T")
    print(f"整体节省率: {stats['overall_savings_rate']:.1f}%")
    
    # 生成集成代码示例
    print("\n=== 集成代码示例 ===")
    print(integrate_with_openclaw())
