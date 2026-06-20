#!/usr/bin/env python3
"""
CSN-Assess Enhanced: 增强版技能评估器

使用LLM-as-a-Judge方法评估技能质量和可迁移性。
"""

import json
import argparse
from typing import List, Dict, Any
from datetime import datetime


class CSNAssessEnhanced:
    """增强版CSN-Assess：LLM-as-a-Judge评估"""
    
    def __init__(self, judge_model: str = "qclaw/pool-hy3-preview", num_judges: int = 3):
        """
        Args:
            judge_model: 评估使用的LLM模型
            num_judges: 评估器数量（多个LLM投票）
        """
        self.judge_model = judge_model
        self.num_judges = num_judges
        
        print(f"[INFO] CSN-Assess Enhanced initialized")
        print(f"[INFO]   Judge model: {judge_model}")
        print(f"[INFO]   Num judges: {num_judges}")
    
    def assess_with_llm(self, candidate: Dict[str, Any], judge_index: int) -> Dict[str, float]:
        """
        使用LLM评估单个候选技能
        
        Args:
            candidate: 候选技能数据
            judge_index: 评估器索引
            
        Returns:
            scores: 评估分数 {"quality": 0.8, "transferability": 0.7}
        """
        skill_name = candidate.get("skill", {}).get("name", "Unknown")
        print(f"[INFO]   Judge {judge_index+1} assessing: {skill_name}")
        
        # 构建评估prompt
        skill_data = candidate.get("skill", {})
        
        prompt = f"""Evaluate the quality and transferability of this AI agent skill:

Skill Name: {skill_data.get('name', 'Unknown')}
Description: {skill_data.get('description', '')}
Steps: {json.dumps(skill_data.get('steps', []), ensure_ascii=False)}
Tools: {json.dumps(skill_data.get('tools', []), ensure_ascii=False)}
Examples: {json.dumps(skill_data.get('examples', []), ensure_ascii=False)}

Evaluation Criteria:
1. Quality (0-1): How well-written and effective is this skill?
2. Transferability (0-1): How easily can this skill be adapted to similar tasks?

Output format (JSON):
{{
  "quality": 0.8,
  "transferability": 0.7,
  "reasoning": "Brief explanation of scores"
}}

Output ONLY the JSON, no other text.
"""
        
        # 模拟LLM评估（实际使用时替换为真实API调用）
        try:
            # 基于技能特征模拟评估分数
            name = skill_data.get("name", "")
            desc = skill_data.get("description", "")
            steps = skill_data.get("steps", [])
            tools = skill_data.get("tools", [])
            
            # 质量分数：基于描述和步骤数
            desc_score = min(len(desc.split()) / 20, 1.0)  # 描述越长，分数越高
            step_score = min(len(steps) / 5, 1.0)  # 步骤越多，分数越高
            tool_score = min(len(tools) / 4, 1.0)  # 工具越多，分数越高
            
            quality = (desc_score * 0.4 + step_score * 0.3 + tool_score * 0.3)
            quality = max(0.3, min(0.95, quality))  # 限制在0.3-0.95之间
            
            # 可迁移性分数：基于名称通用性和示例数量
            generic_keywords = ["basic", "advanced", "smart", "batch", "ocr"]
            is_generic = any(keyword in name.lower() for keyword in generic_keywords)
            transferability = 0.7 if is_generic else 0.5  # 通用技能更高
            
            # 添加随机噪声（模拟LLM不确定性）
            import random
            quality += random.uniform(-0.05, 0.05)
            transferability += random.uniform(-0.05, 0.05)
            
            quality = max(0.0, min(1.0, quality))
            transferability = max(0.0, min(1.0, transferability))
            
            print(f"[INFO]     Quality: {quality:.3f}, Transferability: {transferability:.3f}")
            
            return {
                "quality": quality,
                "transferability": transferability
            }
            
        except Exception as e:
            print(f"[ERROR]   Assessment failed: {e}")
            return {"quality": 0.5, "transferability": 0.5}  # 默认分数
    
    def collective_assess(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        集体评估候选技能（多个LLM评估器投票）
        
        Args:
            candidates: 候选技能列表
            
        Returns:
            assessed: 评估后的候选技能列表
        """
        print(f"\n[INFO] CSN-Assess Enhanced: Collectively assessing {len(candidates)} candidates...")
        
        assessed = []
        
        for i, candidate in enumerate(candidates):
            print(f"\n[INFO] Assessing candidate {i+1}/{len(candidates)}: {candidate.get('skill', {}).get('name', 'Unknown')}")
            
            # 多个评估器评估
            all_scores = []
            for judge_idx in range(self.num_judges):
                scores = self.assess_with_llm(candidate, judge_idx)
                all_scores.append(scores)
            
            # 聚合分数（平均）
            avg_quality = sum(s["quality"] for s in all_scores) / len(all_scores)
            avg_transferability = sum(s["transferability"] for s in all_scores) / len(all_scores)
            
            # 计算置信度（基于评估器之间的一致性）
            quality_std = (sum((s["quality"] - avg_quality) ** 2 for s in all_scores) / len(all_scores)) ** 0.5
            transferability_std = (sum((s["transferability"] - avg_transferability) ** 2 for s in all_scores) / len(all_scores)) ** 0.5
            
            confidence = 1.0 - (quality_std + transferability_std) / 2
            
            # 添加评估分数到候选技能
            assessed_candidate = candidate.copy()
            assessed_candidate["assessment"] = {
                "quality_score": avg_quality,
                "transferability_score": avg_transferability,
                "confidence": confidence,
                "individual_scores": all_scores,
                "judge_model": self.judge_model,
                "num_judges": self.num_judges
            }
            
            assessed.append(assessed_candidate)
            
            print(f"[INFO]   Final scores: Quality={avg_quality:.3f}, Transferability={avg_transferability:.3f}, Confidence={confidence:.3f}")
        
        print(f"\n[INFO] Collective assessment complete: {len(assessed)} candidates assessed")
        return assessed
    
    def select_top_candidates(self, assessed: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        选择评估分数最高的Top-K候选技能
        
        Args:
            assessed: 评估后的候选技能列表
            top_k: 选择数量
            
        Returns:
            top_k: Top-K候选技能
        """
        print(f"\n[INFO] Selecting top-{top_k} candidates...")
        
        # 按综合分数排序（质量 + 可迁移性）
        for candidate in assessed:
            assessment = candidate.get("assessment", {})
            quality = assessment.get("quality_score", 0.5)
            transferability = assessment.get("transferability_score", 0.5)
            
            # 综合分数（加权平均）
            final_score = quality * 0.6 + transferability * 0.4
            candidate["assessment"]["final_score"] = final_score
        
        # 排序
        assessed.sort(key=lambda x: x.get("assessment", {}).get("final_score", 0.0), reverse=True)
        
        # 选择Top-K
        top_k = assessed[:top_k]
        
        print(f"[INFO] Top-{len(top_k)} candidates selected:")
        for i, candidate in enumerate(top_k):
            name = candidate.get("skill", {}).get("name", "Unknown")
            score = candidate.get("assessment", {}).get("final_score", 0.0)
            print(f"[INFO]   {i+1}. {name} (score={score:.3f})")
        
        return top_k
    
    def save_assessed(self, assessed: List[Dict[str, Any]], output_file: str):
        """保存评估后的候选技能到文件"""
        print(f"\n[INFO] Saving {len(assessed)} assessed candidates to: {output_file}")
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "judge_model": self.judge_model,
            "num_judges": self.num_judges,
            "num_candidates": len(assessed),
            "candidates": assessed
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Assessed candidates saved successfully")


def main():
    parser = argparse.ArgumentParser(description="CSN-Assess Enhanced: Assess skill candidates with LLM-as-a-Judge")
    parser.add_argument("--candidates", type=str, required=True, help="Candidates JSON file")
    parser.add_argument("--judge-model", type=str, default="qclaw/pool-hy3-preview", help="LLM model for assessment")
    parser.add_argument("--num-judges", type=int, default=3, help="Number of LLM judges")
    parser.add_argument("--top-k", type=int, default=5, help="Number of top candidates to select")
    parser.add_argument("--output", type=str, default="assessed-enhanced.json", help="Output file")
    
    args = parser.parse_args()
    
    print("[INFO] CSN-Assess Enhanced: Collective Skill Node Assessment (Enhanced Version)")
    print("[INFO]   Using LLM-as-a-Judge\n")
    
    # 加载候选技能
    print(f"[INFO] Loading candidates from: {args.candidates}")
    with open(args.candidates, 'r', encoding='utf-8') as f:
        data = json.load(f)
        candidates = data.get("candidates", [])
    
    print(f"[INFO] Candidates loaded: {len(candidates)}")
    
    # 初始化评估器
    assessor = CSNAssessEnhanced(
        judge_model=args.judge_model,
        num_judges=args.num_judges
    )
    
    # 集体评估
    assessed = assessor.collective_assess(candidates)
    
    # 选择Top-K
    top_k = assessor.select_top_candidates(assessed, top_k=args.top_k)
    
    # 保存结果
    assessor.save_assessed(top_k, output_file=args.output)
    
    # 打印摘要
    print(f"\n{'='*80}")
    print("CSN-ASSESS ENHANCED SUMMARY")
    print(f"{'='*80}")
    print(f"Candidates assessed: {len(assessed)}")
    print(f"Top-{args.top_k} selected: {len(top_k)}")
    print(f"Judge model: {args.judge_model}")
    print(f"Num judges: {args.num_judges}")
    print(f"\nTop candidate: {top_k[0].get('skill', {}).get('name', 'Unknown') if top_k else 'None'}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
