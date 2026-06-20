#!/usr/bin/env python3
"""
Collective Skill RL: 集体技能强化学习

主动选择多个相关技能，拓宽解空间探索
"""

import json
import argparse
import random
from typing import List, Dict, Any, Tuple
from datetime import datetime


class CollectiveSkillRL:
    """Collective Skill Reinforcement Learning"""
    
    def __init__(self, skill_tree_file: str, embedding_model: str = "simple"):
        """
        Args:
            skill_tree_file: 技能树文件路径
            embedding_model: embedding模型 ("simple", "sentence-transformers")
        """
        self.skill_tree_file = skill_tree_file
        self.embedding_model = embedding_model
        self.skills = []  # 技能列表
        self.task_embeddings = {}  # 任务embedding缓存
        
        # 加载技能树
        self.load_skill_tree()
        
        print(f"[INFO] CollectiveSkillRL initialized")
        print(f"[INFO]   Skill tree: {skill_tree_file}")
        print(f"[INFO]   Skills loaded: {len(self.skills)}")
    
    def load_skill_tree(self):
        """加载技能树"""
        try:
            with open(self.skill_tree_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取所有技能
            nodes = data.get("nodes", {})
            self.skills = [node_data.get("skill_data", {}) for node_data in nodes.values()]
            
            print(f"[INFO] Skill tree loaded: {len(self.skills)} skills")
        except Exception as e:
            print(f"[ERROR] Failed to load skill tree: {e}")
            self.skills = []
    
    def encode_task(self, task: str) -> List[float]:
        """
        编码任务（简化版：词袋模型）
        
        Args:
            task: 任务描述
            
        Returns:
            embedding: 任务embedding
        """
        # 简化版：使用字符频率作为embedding
        chars = [0] * 256  # ASCII
        for char in task:
            code = ord(char) % 256
            chars[code] += 1
        
        # 归一化
        total = sum(chars)
        if total > 0:
            embedding = [c / total for c in chars]
        else:
            embedding = chars
        
        return embedding
    
    def compute_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """计算余弦相似度"""
        # 简化版：点积（因为我们的embedding是归一化的）
        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        return dot_product
    
    def retrieve_skills(self, task: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        检索相关技能
        
        Args:
            task: 任务描述
            top_k: 返回前K个
            
        Returns:
            results: [(skill, similarity_score), ...]
        """
        print(f"[INFO] Retrieving top-{top_k} skills for task: {task[:50]}...")
        
        # 编码任务
        task_emb = self.encode_task(task)
        
        # 计算相似度
        similarities = []
        for skill_data in self.skills:
            skill = skill_data.get("skill", {})
            skill_desc = skill.get("description", "")
            
            # 编码技能描述
            skill_emb = self.encode_task(skill_desc)
            
            # 计算相似度
            sim = self.compute_similarity(task_emb, skill_emb)
            
            similarities.append((skill_data, sim))
        
        # 排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前K个
        results = similarities[:top_k]
        
        print(f"[INFO] Retrieved {len(results)} skills")
        for i, (skill_data, sim) in enumerate(results):
            skill = skill_data.get("skill", {})
            print(f"[INFO]   {i+1}. {skill.get('name', 'Unknown')} (sim={sim:.3f})")
        
        return results
    
    def select_skills(self, task: str, top_k: int = 3, strategy: str = "diverse") -> List[Dict[str, Any]]:
        """
        选择技能组合
        
        Args:
            task: 任务描述
            top_k: 选择前K个技能
            strategy: 选择策略 ("greedy", "diverse", "random")
            
        Returns:
            selected: 选定的技能列表
        """
        print(f"[INFO] Selecting skills (strategy={strategy})...")
        
        # 检索相关技能
        retrieved = self.retrieve_skills(task, top_k=top_k * 2)
        
        if strategy == "greedy":
            # 贪心选择：取相似度最高的K个
            selected = [skill_data for skill_data, _ in retrieved[:top_k]]
            
        elif strategy == "diverse":
            # 多样性选择：最大化最小相似度
            selected = []
            remaining = retrieved.copy()
            
            # 第一个：选择相似度最高的
            if remaining:
                selected.append(remaining.pop(0)[0])
            
            # 后续：选择与已选技能最不相似的
            while len(selected) < top_k and remaining:
                best_idx = 0
                best_min_sim = -1
                
                for i, (candidate, _) in enumerate(remaining):
                    # 计算与所有已选技能的最小相似度
                    candidate_emb = self.encode_task(
                        candidate.get("skill", {}).get("description", "")
                    )
                    
                    min_sim = min(
                        self.compute_similarity(
                            candidate_emb,
                            self.encode_task(s.get("skill", {}).get("description", ""))
                        )
                        for s in selected
                    )
                    
                    if min_sim > best_min_sim:
                        best_min_sim = min_sim
                        best_idx = i
                
                if best_idx >= 0:
                    selected.append(remaining.pop(best_idx)[0])
            
        elif strategy == "random":
            # 随机选择
            indices = random.sample(range(len(retrieved)), min(top_k, len(retrieved)))
            selected = [retrieved[i][0] for i in indices]
            
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        print(f"[INFO] Selected {len(selected)} skills:")
        for i, skill_data in enumerate(selected):
            skill = skill_data.get("skill", {})
            print(f"[INFO]   {i+1}. {skill.get('name', 'Unknown')}")
        
        return selected
    
    def augment_reasoning(self, task: str, selected_skills: List[Dict[str, Any]]) -> str:
        """
        增强推理：将选定的技能注入到prompt
        
        Args:
            task: 任务描述
            selected_skills: 选定的技能
            
        Returns:
            augmented_prompt: 增强后的prompt
        """
        print(f"[INFO] Augmenting reasoning with {len(selected_skills)} skills...")
        
        # 构建技能描述部分
        skills_desc = ""
        for i, skill_data in enumerate(selected_skills):
            skill = skill_data.get("skill", {})
            skills_desc += f"\n### Skill {i+1}: {skill.get('name', 'Unknown')}\n"
            skills_desc += f"**Description**: {skill.get('description', '')}\n"
            skills_desc += f"**Steps**:\n"
            for step in skill.get("steps", []):
                skills_desc += f"- {step}\n"
        
        # 构建增强prompt
        augmented_prompt = f"""You are a helpful AI assistant.

## Task
{task}

## Relevant Skills
You have access to the following skills that may help with this task:
{skills_desc}

## Instructions
1. Analyze the task carefully
2. Consider which skills are relevant
3. Use the skills appropriately to solve the task
4. Verify your solution

Let's solve this step by step.
"""
        
        print(f"[INFO] Prompt augmented (length: {len(augmented_prompt)} chars)")
        
        return augmented_prompt
    
    def train_rl(self, training_tasks: List[Dict[str, Any]], num_episodes: int = 100):
        """
        训练RL（简化版：基于规则的策略）
        
        Args:
            training_tasks: 训练任务列表
            num_episodes: 训练轮数
        """
        print(f"[INFO] Training RL (simplified version)...")
        print(f"[INFO]   Training tasks: {len(training_tasks)}")
        print(f"[INFO]   Episodes: {num_episodes}")
        
        # 简化版：不实际训练，只是模拟
        # 实际应实现：
        # 1. Policy network (πθ)
        # 2. Reward function (task success, token efficiency)
        # 3. RL algorithm (PPO/REINFORCE)
        
        print(f"[INFO] RL training complete (simulated)")
        print(f"[INFO]   Note: This is a simplified version.")
        print(f"[INFO]   For full implementation, use PyTorch/TensorFlow.")


def main():
    parser = argparse.ArgumentParser(description="Collective Skill RL: Select and augment with skills")
    parser.add_argument("--task", type=str, help="Task description")
    parser.add_argument("--skill-tree", type=str, default="memory/csts-skill-tree.json", 
                       help="Skill tree file")
    parser.add_argument("--top-k", type=int, default=3, help="Select top-K skills")
    parser.add_argument("--strategy", type=str, default="diverse", 
                       choices=["greedy", "diverse", "random"],
                       help="Skill selection strategy")
    parser.add_argument("--output-prompt", type=str, help="Output augmented prompt to file")
    parser.add_argument("--train", action="store_true", help="Train RL (simulated)")
    parser.add_argument("--training-tasks", type=str, help="Training tasks JSON file")
    
    args = parser.parse_args()
    
    # 初始化
    rl = CollectiveSkillRL(skill_tree_file=args.skill_tree)
    
    if args.train:
        # 训练模式
        training_tasks = []
        if args.training_tasks:
            with open(args.training_tasks, 'r', encoding='utf-8') as f:
                training_tasks = json.load(f)
        else:
            # 使用默认训练任务
            training_tasks = [
                {"task": "Read a PDF file", "expected_output": "Text content"},
                {"task": "Extract text from PDF", "expected_output": "Extracted text"}
            ]
        
        rl.train_rl(training_tasks, num_episodes=100)
    
    elif args.task:
        # 推理模式：选择技能并增强prompt
        print(f"\n[INFO] Running inference for task: {args.task}")
        
        # 选择技能
        selected = rl.select_skills(args.task, top_k=args.top_k, strategy=args.strategy)
        
        # 增强推理
        augmented_prompt = rl.augment_reasoning(args.task, selected)
        
        # 输出
        if args.output_prompt:
            with open(args.output_prompt, 'w', encoding='utf-8') as f:
                f.write(augmented_prompt)
            print(f"\n[INFO] Augmented prompt saved to: {args.output_prompt}")
        else:
            print(f"\n[INFO] Augmented prompt:")
            print("=" * 80)
            print(augmented_prompt)
            print("=" * 80)
    
    else:
        print("[ERROR] Must specify --task or --train")
        print("[INFO] Usage examples:")
        print("  Inference: python collective_rl.py --task 'Read PDF' --top-k 3")
        print("  Training:  python collective_rl.py --train --training-tasks tasks.json")


if __name__ == "__main__":
    main()
