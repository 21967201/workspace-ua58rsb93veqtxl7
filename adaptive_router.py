"""
自适应路由引擎 (Adaptive Router) v1.0
=====================================
基于任务复杂度评估的智能路由系统。
参考: DECS(ICLR 2026 Oral) + AbstractCoT(IBM) + CoD(Zoom)

Token预算策略:
  - 简单(0-0.3): 直答, 0额外token
  - 中等(0.3-0.7): CoD草稿链, ≤7.6%原始CoT
  - 复杂(0.7-1.0): CoT+TokenSkip, ≤15%原始CoT
  - 决策(关键): 多视角验证, ≤15%原始CoT
"""

import json
import sys
from dataclasses import dataclass, field
from typing import Optional


# ─── 数据模型 ───────────────────────────────────────────────

@dataclass
class TaskProfile:
    """任务画像"""
    query: str
    estimated_complexity: float = 0.0
    token_budget: str = "0"
    strategy: str = "direct_answer"
    model_tier: str = "cheapest"
    requires_verification: bool = False
    confidence_label: str = ""

    def to_dict(self):
        return {
            "query": self.query[:80],
            "complexity": self.estimated_complexity,
            "token_budget": self.token_budget,
            "strategy": self.strategy,
            "model_tier": self.model_tier,
            "verification": self.requires_verification
        }


# ─── 复杂度评估器 ───────────────────────────────────────────

class ComplexityEstimator:
    """评估任务复杂度 (0-1)"""

    KEYWORD_WEIGHTS = {
        "high_complexity": [
            ("分析", 0.3), ("推理", 0.3), ("生成", 0.25),
            ("比较", 0.25), ("预测", 0.3), ("评估", 0.25),
            ("设计", 0.3), ("研究", 0.25), ("构建", 0.25),
            ("优化", 0.2), ("调试", 0.2), ("实现", 0.25),
            ("架构", 0.3), ("分布式", 0.3), ("系统", 0.2),
            ("策略", 0.2), ("框架", 0.2),
        ],
        "medium_complexity": [
            ("解释", 0.15), ("说明", 0.12), ("总结", 0.1),
            ("描述", 0.1), ("建议", 0.12), ("方案", 0.15),
            ("方法", 0.1), ("步骤", 0.08), ("流程", 0.1),
        ],
        "low_complexity": [
            ("什么是", -0.2), ("是谁", -0.2), ("在哪里", -0.15),
            ("现在几点", -0.3), ("天气", -0.2),
            ("你好", -0.4), ("谢谢", -0.3), ("再见", -0.4),
        ],
        "verification_signals": [
            "资金", "预算", "投资",
            "权限", "敏感", "保密",
            "对外", "公开", "api", "密码", "token",
        ],
        "code_signals": [
            "```", "def ", "class ", "import ",
            "function", "const ", "let ", "var ",
            ".py", ".js", ".ts", ".json",
        ]
    }

    def estimate(self, query: str) -> TaskProfile:
        """评估单个查询的复杂度"""
        profile = TaskProfile(query=query)
        score = 0.0

        # 1. 长度评估
        word_count = len(query.split())
        if word_count > 50:
            score += 0.3
        elif word_count > 20:
            score += 0.1

        # 2. 关键词匹配 (contains / in)
        query_lower = query.lower()
        for kw, weight in self.KEYWORD_WEIGHTS["high_complexity"]:
            if kw in query or kw in query_lower:
                score += weight

        for kw, weight in self.KEYWORD_WEIGHTS["medium_complexity"]:
            if kw in query or kw in query_lower:
                score += weight

        for kw, weight in self.KEYWORD_WEIGHTS["low_complexity"]:
            if kw in query:
                score += weight

        # 3. 验证信号检测
        for signal in self.KEYWORD_WEIGHTS["verification_signals"]:
            if signal in query or signal in query_lower:
                profile.requires_verification = True
                score += 0.1
                break

        # 4. 代码信号
        for signal in self.KEYWORD_WEIGHTS["code_signals"]:
            if signal in query:
                score += 0.15
                break

        # 规范化到0-1范围
        score = max(0.0, min(1.0, score))
        profile.estimated_complexity = round(score, 2)

        # 分配策略
        profile = self.assign_strategy(profile)
        return profile

    def assign_strategy(self, profile: TaskProfile) -> TaskProfile:
        """根据复杂度分配推理策略"""
        c = profile.estimated_complexity

        if c <= 0.3:
            profile.strategy = "direct_answer"
            profile.token_budget = "0"
            profile.model_tier = "cheapest"
            profile.confidence_label = "LOW" if c < 0.1 else "MEDIUM"
        elif c <= 0.7:
            profile.strategy = "cod_reasoning"
            profile.token_budget = "7.6% of original"
            profile.model_tier = "balanced"
            profile.confidence_label = "MEDIUM"
        else:
            profile.strategy = "cot_skip"
            profile.token_budget = "15% of original"
            profile.model_tier = "most_capable"
            profile.confidence_label = "HIGH"

        if profile.requires_verification and c > 0.5:
            profile.strategy += "+multi_view"
            profile.confidence_label += "+verification"

        return profile


# ─── 批次路由 ───────────────────────────────────────────────

class BatchRouter:
    """批量处理路由决策"""

    def __init__(self):
        self.estimator = ComplexityEstimator()
        self.routes: list[TaskProfile] = []

    def route(self, query: str) -> dict:
        """路由单条查询"""
        profile = self.estimator.estimate(query)
        self.routes.append(profile)
        return profile.to_dict()

    def route_batch(self, queries: list[str]) -> list[dict]:
        """路由批量查询"""
        results = []
        for q in queries:
            profile = self.estimator.estimate(q)
            self.routes.append(profile)
            results.append(profile.to_dict())
        return results

    def get_stats(self) -> dict:
        """获取路由统计"""
        if not self.routes:
            return {"total": 0}

        strategies = {}
        for r in self.routes:
            s = r.strategy.split("+")[0]
            strategies[s] = strategies.get(s, 0) + 1

        avg_complexity = sum(r.estimated_complexity for r in self.routes) / len(self.routes)

        return {
            "total": len(self.routes),
            "strategies": strategies,
            "avg_complexity": round(avg_complexity, 2),
            "tier_distribution": {
                "direct_answer": sum(1 for r in self.routes if r.strategy.startswith("direct")),
                "cod": sum(1 for r in self.routes if "cod" in r.strategy),
                "cot": sum(1 for r in self.routes if "cot" in r.strategy),
                "needs_verification": sum(1 for r in self.routes if r.requires_verification),
            }
        }


# ─── 演示 ────────────────────────────────────────────────────

def demo():
    """自适应路由引擎演示"""
    sys.stdout.reconfigure(encoding='utf-8')

    router = BatchRouter()

    test_queries = [
        "什么是自适应路由引擎？",                    # simple
        "帮我生成一段Python代码",                     # simple
        "分析最近一周的Token消耗趋势",                # medium
        "比较Headroom和LCM两种压缩方案的优劣",         # medium
        "设计一个分布式Agent编排系统架构",             # complex
        "这个投资方案需要预算100万美金给新项目",        # complex+decision
        "你好",                                      # very simple
        "调试这个RAG系统的内存泄漏问题，并给出优化方案", # complex
        "今天天气怎么样？",                           # very simple
    ]

    print("=" * 60)
    print("  Adaptive Router v1.0 - Routing Decision Demo")
    print("=" * 60)

    results = router.route_batch(test_queries)

    for i, r in enumerate(results):
        print(f"\n  [{i+1}] Q: \"{r['query']}\"")
        print(f"      Complexity: {r['complexity']} | Strategy: {r['strategy']}")
        print(f"      Token Budget: {r['token_budget']} | Model: {r['model_tier']}")

    print("\n" + "=" * 60)
    stats = router.get_stats()
    print(f"  Stats:")
    print(f"      Total queries: {stats['total']}")
    print(f"      Avg complexity: {stats['avg_complexity']}")
    print(f"      Strategy distribution: {json.dumps(stats['strategies'], ensure_ascii=False)}")
    print(f"      Needs verification: {stats['tier_distribution']['needs_verification']}")
    print("=" * 60)

    # 保存路由日志
    log = {
        "timestamp": "2026-06-09",
        "total_queries": stats['total'],
        "avg_complexity": stats['avg_complexity'],
        "strategy_distribution": stats['strategies'],
        "routes": results
    }
    with open("router_demo_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"\n  [OK] Router log saved to router_demo_log.json")
    print(f"  [NEXT] Integrate this into QClaw main reasoning pipeline")
    print("=" * 60)


if __name__ == "__main__":
    demo()
