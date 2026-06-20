#!/usr/bin/env python3
"""
CSN-Gen: Collective Skill Node Generation

利用多模型集体知识探索多样化候选技能
"""

import json
import argparse
from typing import List, Dict, Any

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  numpy not available, using simple similarity")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️  sentence-transformers not available, will use simple deduplication")


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
        
        # 加载sentence-transformers (如果可用)
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            print("📦 Loading sentence-transformers model...")
            self.encoder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        else:
            self.encoder = None
    
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
            print(f"🔄 Generating candidates with model: {model}")
            
            # 简化版：使用模板生成候选技能 (实际应调用LLM API)
            model_candidates = self._generate_with_model(model, task_description, num_candidates)
            candidates.extend(model_candidates)
        
        print(f"✅ Generated {len(candidates)} total candidates")
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
    
    def deduplicate(self, candidates: List[Dict[str, Any]], similarity_threshold: float = 0.9) -> List[Dict[str, Any]]:
        """
        去重：基于语义相似度
        
        Args:
            candidates: 候选技能列表
            similarity_threshold: 相似度阈值 (>, 9 视为重复)
            
        Returns:
            deduplicated: 去重后的候选技能
        """
        if not self.encoder:
            print("⚠️  No encoder available, skipping deduplication")
            return candidates
        
        print(f"🔍 Deduplicating {len(candidates)} candidates...")
        
        # 编码所有候选技能
        texts = [c["skill"]["description"] for c in candidates]
        embeddings = self.encoder.encode(texts)
        
        # 去重
        deduplicated = []
        used = set()
        
        if NUMPY_AVAILABLE:
            for i, cand in enumerate(candidates):
                if i in used:
                    continue
                
                # 找到所有与i相似的候选
                similarities = np.dot(embeddings, embeddings[i]) / (
                    np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embeddings[i]) + 1e-8
                )
                
                similar_indices = np.where(similarities > similarity_threshold)[0]
        else:
            # 简化版：基于文本重叠的去重
            for i, cand in enumerate(candidates):
                if i in used:
                    continue
                
                text_i = texts[i].lower()
                similar_indices = [i]
                
                for j, text_j in enumerate(texts):
                    if j != i and j not in used:
                        # 简单相似度：词汇重叠
                        words_i = set(text_i.split())
                        words_j = set(text_j.lower().split())
                        overlap = len(words_i & words_j) / max(len(words_i), len(words_j), 1)
                        
                        if overlap > similarity_threshold:
                            similar_indices.append(j)
        
        # 保留第一个，标记其他的为已使用
        for idx in similar_indices:
            if idx != i:
                used.add(idx)
            
            # 保留第一个，标记其他的为已使用
            deduplicated.append(cand)
            for j in similar_indices:
                if j != i:
                    used.add(j)
        
        print(f"✅ Deduplicated: {len(candidates)} → {len(deduplicated)}")
        return deduplicated
    
    def select_diverse(self, candidates: List[Dict[str, Any]], k: int = 5) -> List[Dict[str, Any]]:
        """
        选择最多样化的K个候选技能
        
        Args:
            candidates: 候选技能列表
            k: 要选择的数量
            
        Returns:
            selected: 选定的K个候选技能
        """
        if not self.encoder or len(candidates) <= k:
            return candidates[:k]
        
        print(f"🎯 Selecting {k} most diverse candidates...")
        
        if NUMPY_AVAILABLE:
            # 编码
            texts = [c["skill"]["description"] for c in candidates]
            embeddings = self.encoder.encode(texts)
            
            # 贪心选择：最大化最小相似度
            selected_indices = [0]  # 从第一个开始
            
            while len(selected_indices) < k:
                best_idx = -1
                best_score = -1
                
                for i in range(len(candidates)):
                    if i in selected_indices:
                        continue
                    
                    # 计算i与所有已选候选的最小相似度
                    min_sim = min(
                        np.dot(embeddings[i], embeddings[j]) / (
                            np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]) + 1e-8
                        )
                        for j in selected_indices
                    )
                    
                    if min_sim > best_score:
                        best_score = min_sim
                        best_idx = i
                
                if best_idx == -1:
                    break
                
                selected_indices.append(best_idx)
        else:
            # 简化版：随机选择K个
            selected_indices = list(range(min(k, len(candidates))))
        
        selected = [candidates[i] for i in selected_indices]
        print(f"✅ Selected {len(selected)} diverse candidates")
        
        return selected


def main():
    parser = argparse.ArgumentParser(description="CSN-Gen: Collective Skill Node Generation")
    parser.add_argument("--task", type=str, required=True, help="Task description")
    parser.add_argument("--models", type=str, required=True, help="Comma-separated model names")
    parser.add_argument("--num-candidates", type=int, default=10, help="Number of candidates per model")
    parser.add_argument("--output", type=str, default="candidates.json", help="Output file")
    parser.add_argument("--top-k", type=int, default=5, help="Select top-K diverse candidates")
    
    args = parser.parse_args()
    
    # 解析模型列表
    models = [m.strip() for m in args.models.split(",")]
    
    print(f"🚀 Starting CSN-Gen")
    print(f"   Task: {args.task}")
    print(f"   Models: {models}")
    print(f"   Candidates per model: {args.num_candidates}")
    print(f"   Top-K diverse: {args.top_k}")
    
    # 初始化生成器
    generator = CSNGenerator(models=models)
    
    # 生成候选技能
    candidates = generator.generate_candidates(args.task, args.num_candidates)
    
    # 去重
    candidates = generator.deduplicate(candidates, similarity_threshold=0.9)
    
    # 选择多样化的Top-K
    candidates = generator.select_diverse(candidates, k=args.top_k)
    
    # 保存结果
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results saved to: {args.output}")
    print(f"📊 Total candidates: {len(candidates)}")


if __name__ == "__main__":
    main()
