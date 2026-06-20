#!/usr/bin/env python3
"""
CSN-Gen: Collective Skill Node Generation (Fixed Version)

利用多模型集体知识探索多样化候选技能
支持无numpy/sentence-transformers环境
"""

import json
import argparse
from typing import List, Dict, Any


class CSNGenerator:
    """Collective Skill Node Generation"""
    
    def __init__(self, models: List[str], temperature_range: tuple = (0.7, 1.2)):
        """
        Args:
            models: 模型列表 (e.g., ["qclaw/pool-hy3-preview", "gpt-4"])
            temperature_range: 温度范围 (min, max)
        """
        self.models = models
        self.temp_min, self.temp_max = temperature_range
        self.encoder = None  # 简化版不使用encoder
        
        print("[INFO] CSN-Generator initialized (simplified mode, no dependencies)")
    
    def generate_candidates(self, task_description: str, num_candidates: int = 10) -> List[Dict[str, Any]]:
        """
        生成候选技能节点
        
        Args:
            task_description: 任务描述
            num_candidates: 每个模型生成的候选技能数
            
        Returns:
            candidates: 候选技能列表 [{"model": ..., "skill": ..., "prompt": ...}, ...]
        """
        candidates = []
        
        for model in self.models:
            print(f"[INFO] Generating candidates with model: {model}")
            
            # 简化版：使用模板生成候选技能 (实际应调用LLM API)
            model_candidates = self._generate_with_model(model, task_description, num_candidates)
            candidates.extend(model_candidates)
        
        print(f"[INFO] Generated {len(candidates)} total candidates")
        return candidates
    
    def _generate_with_model(self, model: str, task: str, n: int) -> List[Dict[str, Any]]:
        """使用单个模型生成候选技能 (简化版)"""
        # TODO: 实际应调用OpenClaw API / sessions_spawn
        # 这里使用模板模拟生成
        
        candidates = []
        for i in range(n):
            candidate = {
                "model": model,
                "skill": {
                    "name": f"Skill_{model.replace('/', '_')}_{i}",
                    "description": f"Candidate skill for task: {task[:50]}...",
                    "steps": [
                        f"Step 1: Analyze task: {task}",
                        f"Step 2: Execute action using {model}",
                        f"Step 3: Verify result"
                    ],
                    "prompt_template": f"You are a helpful assistant. Task: {task}\nUse the following steps:\n{{steps}}"
                },
                "temperature": self.temp_min + (self.temp_max - self.temp_min) * (i / max(n-1, 1))
            }
            candidates.append(candidate)
        
        return candidates
    
    def deduplicate(self, candidates: List[Dict[str, Any]], similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        去重：基于简单词汇重叠相似度
        
        Args:
            candidates: 候选技能列表
            similarity_threshold: 相似度阈值 (>, 5 视为重复)
            
        Returns:
            deduplicated: 去重后的候选技能
        """
        print(f"[INFO] Deduplicating {len(candidates)} candidates (simple method)...")
        
        # 简单去重：基于文本重叠
        texts = [c["skill"]["description"].lower() for c in candidates]
        
        deduplicated = []
        used = set()
        
        for i, cand in enumerate(candidates):
            if i in used:
                continue
            
            # 找到所有与i相似的候选 (基于词汇重叠)
            words_i = set(texts[i].split())
            
            for j, text_j in enumerate(texts):
                if j <= i or j in used:
                    continue
                
                words_j = set(text_j.split())
                overlap = len(words_i & words_j) / max(len(words_i), len(words_j), 1)
                
                if overlap > similarity_threshold:
                    used.add(j)
            
            deduplicated.append(cand)
        
        print(f"[INFO] Deduplicated: {len(candidates)} -> {len(deduplicated)}")
        return deduplicated
    
    def select_diverse(self, candidates: List[Dict[str, Any]], k: int = 5) -> List[Dict[str, Any]]:
        """
        选择最多样化的K个候选技能 (简化版：随机选择)
        
        Args:
            candidates: 候选技能列表
            k: 要选择的数量
            
        Returns:
            selected: 选定的K个候选技能
        """
        print(f"[INFO] Selecting {k} diverse candidates (simplified: first-k)")
        
        # 简化版：选择前K个
        selected = candidates[:min(k, len(candidates))]
        
        print(f"[INFO] Selected {len(selected)} candidates")
        return selected


def main():
    parser = argparse.ArgumentParser(description="CSN-Gen: Collective Skill Node Generation (Simplified)")
    parser.add_argument("--task", type=str, required=True, help="Task description")
    parser.add_argument("--models", type=str, required=True, help="Comma-separated model names")
    parser.add_argument("--num-candidates", type=int, default=10, help="Number of candidates per model")
    parser.add_argument("--output", type=str, default="candidates.json", help="Output file")
    parser.add_argument("--top-k", type=int, default=5, help="Select top-K diverse candidates")
    
    args = parser.parse_args()
    
    # 解析模型列表
    models = [m.strip() for m in args.models.split(",")]
    
    print("[INFO] Starting CSN-Gen (Simplified Version)")
    print(f"[INFO]   Task: {args.task}")
    print(f"[INFO]   Models: {models}")
    print(f"[INFO]   Candidates per model: {args.num_candidates}")
    print(f"[INFO]   Top-K diverse: {args.top_k}")
    
    # 初始化生成器
    generator = CSNGenerator(models=models)
    
    # 生成候选技能
    candidates = generator.generate_candidates(args.task, args.num_candidates)
    
    # 去重
    candidates = generator.deduplicate(candidates, similarity_threshold=0.5)
    
    # 选择多样化的Top-K
    candidates = generator.select_diverse(candidates, k=args.top_k)
    
    # 保存结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    
    print(f"[INFO] Results saved to: {args.output}")
    print(f"[INFO] Total candidates: {len(candidates)}")


if __name__ == "__main__":
    main()
