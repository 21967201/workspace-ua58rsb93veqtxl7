"""
Phase 5: 全局Token预算协议 - 预算控制器
版本: v6.0.0
功能: 硬预算约束 + 任务分级 + 超限触发骨架提取
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time


class TaskLevel(Enum):
    """任务等级定义"""
    MINIMAL = "minimal"      # 极简问答 300T
    SIMPLE = "simple"        # 简单问答 500T
    EXTRACT = "extract"      # 分类提取 1000T
    ANALYZE = "analyze"      # 分析对比 2000T
    REPORT = "report"        # 报告生成 4000T
    CODING = "coding"        # 代码开发 8000T
    COMPLEX = "complex"      # 复杂系统 15000T


@dataclass
class TokenBudget:
    """Token预算配置"""
    level: TaskLevel
    budget: int
    trigger_scenarios: list[str]
    
    def to_dict(self):
        return {
            "level": self.level.value,
            "budget": self.budget,
            "triggers": self.trigger_scenarios
        }


class Phase5BudgetController:
    """
    Phase 5 预算控制器
    
    核心功能:
    1. 任务分级识别
    2. 硬预算约束
    3. 超限触发骨架模式
    """
    
    # 7级Token预算表
    BUDGET_TABLE = {
        TaskLevel.MINIMAL: TokenBudget(
            level=TaskLevel.MINIMAL,
            budget=300,
            trigger_scenarios=["是/否/哪个", "确认", "好的"]
        ),
        TaskLevel.SIMPLE: TokenBudget(
            level=TaskLevel.SIMPLE,
            budget=500,
            trigger_scenarios=["怎么做", "什么是", "怎么用"]
        ),
        TaskLevel.EXTRACT: TokenBudget(
            level=TaskLevel.EXTRACT,
            budget=1000,
            trigger_scenarios=["列举", "分类", "列出", "提取"]
        ),
        TaskLevel.ANALYZE: TokenBudget(
            level=TaskLevel.ANALYZE,
            budget=2000,
            trigger_scenarios=["对比", "分析", "评估", "比较"]
        ),
        TaskLevel.REPORT: TokenBudget(
            level=TaskLevel.REPORT,
            budget=4000,
            trigger_scenarios=["报告", "详细", "研究", "方案"]
        ),
        TaskLevel.CODING: TokenBudget(
            level=TaskLevel.CODING,
            budget=8000,
            trigger_scenarios=["代码", "实现", "开发", "架构"]
        ),
        TaskLevel.COMPLEX: TokenBudget(
            level=TaskLevel.COMPLEX,
            budget=15000,
            trigger_scenarios=["设计全系统", "多模块", "复杂集成"]
        ),
    }
    
    def __init__(self, initial_bank: int = 4000):
        """
        初始化预算控制器
        
        Args:
            initial_bank: Token银行初始额度 (默认4000)
        """
        self.initial_bank = initial_bank
        self.token_bank = initial_bank
        self.bank_interest_rate = 0.05  # 5%复利
        self.overdraft_limit = 0.5  # 可透支50%
        
        # 会话统计
        self.session_usage = []
        self.total_saved = 0
        
    def classify_task(self, user_query: str) -> TaskLevel:
        """
        识别任务等级
        
        Args:
            user_query: 用户查询字符串
            
        Returns:
            TaskLevel: 任务等级
        """
        query_lower = user_query.lower().strip()
        
        # 极简问答 (≤8字纯确认)
        if len(query_lower) <= 8 and any(word in query_lower for word in ["好", "可以", "行", "完成", "知道"]):
            return TaskLevel.MINIMAL
        
        # 复杂系统
        if any(word in query_lower for word in ["设计全系统", "多模块集成", "复杂架构"]):
            return TaskLevel.COMPLEX
        
        # 代码开发
        if any(word in query_lower for word in ["代码", "实现", "开发", "编程", "函数", "类"]):
            return TaskLevel.CODING
        
        # 报告生成
        if any(word in query_lower for word in ["报告", "详细分析", "研究报告", "完整方案"]):
            return TaskLevel.REPORT
        
        # 分析对比
        if any(word in query_lower for word in ["对比", "分析", "评估", "比较", "区别"]):
            return TaskLevel.ANALYZE
        
        # 分类提取
        if any(word in query_lower for word in ["列举", "分类", "列出", "提取", "总结"]):
            return TaskLevel.EXTRACT
        
        # 默认: 简单问答
        return TaskLevel.SIMPLE
    
    def get_budget(self, task_level: TaskLevel) -> int:
        """
        获取任务预算
        
        Args:
            task_level: 任务等级
            
        Returns:
            int: Token预算
        """
        return self.BUDGET_TABLE[task_level].budget
    
    def check_budget(self, task_level: TaskLevel, estimated_tokens: int) -> tuple[bool, int]:
        """
        检查预算是否超限
        
        Args:
            task_level: 任务等级
            estimated_tokens: 预估Token消耗
            
        Returns:
            tuple: (是否超限, 预算余额)
        """
        budget = self.get_budget(task_level)
        remaining = budget - estimated_tokens
        return remaining < 0, remaining
    
    def trigger_skeleton_mode(self, conclusion: str, key_data: list[str], next_step: str) -> str:
        """
        触发骨架提取模式 (超预算时强制启用)
        
        提取三要素:
        1. 结论(≤50字)
        2. 关键数据(≤3条)
        3. 下一步(≤30字)
        
        Args:
            conclusion: 结论
            key_data: 关键数据列表
            next_step: 下一步行动
            
        Returns:
            str: 骨架化输出
        """
        # 压缩结论至50字
        conclusion_short = conclusion[:50] if len(conclusion) > 50 else conclusion
        
        # 保留≤3条关键数据
        data_short = key_data[:3]
        data_text = "|".join(data_short)
        
        # 压缩下一步至30字
        next_short = next_step[:30] if len(next_step) > 30 else next_step
        
        # 组装骨架输出
        skeleton = f"结论:{conclusion_short} | 数据:{data_text} | 下一步:{next_short}"
        
        return skeleton
    
    def save_to_bank(self, saved_tokens: int):
        """
        节省的Token存入银行 (产生5%复利)
        
        Args:
            saved_tokens: 节省的Token数
        """
        # 存入本金
        self.token_bank += saved_tokens
        self.total_saved += saved_tokens
        
        # 计算利息 (每轮对话结算5%)
        interest = int(self.token_bank * self.bank_interest_rate)
        self.token_bank += interest
        
        # 记录
        self.session_usage.append({
            "saved": saved_tokens,
            "interest": interest,
            "balance": self.token_bank,
            "timestamp": time.time()
        })
    
    def can_overdraft(self, required_tokens: int) -> bool:
        """
        检查是否可以透支
        
        Args:
            required_tokens: 需要的Token数
            
        Returns:
            bool: 是否可以透支
        """
        overdraft_available = int(self.token_bank * self.overdraft_limit)
        return required_tokens <= overdraft_available
    
    def generate_report(self) -> Dict[str, Any]:
        """
        生成预算使用报告
        
        Returns:
            Dict: 报告数据
        """
        return {
            "initial_bank": self.initial_bank,
            "current_balance": self.token_bank,
            "total_saved": self.total_saved,
            "interest_earned": self.token_bank - self.initial_bank - self.total_saved,
            "session_count": len(self.session_usage),
            "usage_history": self.session_usage[-10:]  # 最近10次
        }


# 测试代码
if __name__ == "__main__":
    controller = Phase5BudgetController(initial_bank=4000)
    
    # 测试任务分类
    test_queries = [
        "好的",
        "1688怎么做",
        "列举5个方法",
        "对比A和B",
        "详细运营报告",
        "写自动化脚本",
        "设计全系统"
    ]
    
    print("=== Phase 5 预算控制器测试 ===\n")
    for query in test_queries:
        level = controller.classify_task(query)
        budget = controller.get_budget(level)
        print(f"查询: {query}")
        print(f"  等级: {level.value}")
        print(f"  预算: {budget}T\n")
    
    # 测试骨架提取
    print("=== 骨架提取测试 ===")
    skeleton = controller.trigger_skeleton_mode(
        conclusion="关键词不足导致搜索降权,需要优化标题",
        key_data=["转化率下降30%", "竞品均价低20%", "流量提升50%"],
        next_step="建议在低竞争时段加价"
    )
    print(f"骨架输出: {skeleton}\n")
    
    # 测试Token银行
    print("=== Token银行测试 ===")
    controller.save_to_bank(500)
    controller.save_to_bank(300)
    report = controller.generate_report()
    print(f"总节省: {report['total_saved']}T")
    print(f"当前余额: {report['current_balance']}T")
    print(f"利息收入: {report['interest_earned']}T")
