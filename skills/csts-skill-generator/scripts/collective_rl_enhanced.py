#!/usr/bin/env python3
"""
Collective RL Enhanced: 增强版集体强化学习

基于CSTS论文，实现技能组合强化学习策略。
"""

import json
import argparse
import random
from typing import List, Dict, Any
from datetime import datetime


class CollectiveRLEnhanced:
    """增强版集体强化学习策略"""
    
    def __init__(self, num_iterations: int = 5, exploration_rate: float = 0.2, learning_rate: float = 0.1):
        """
        Args:
            num_iterations: 强化学习迭代次数
            exploration_rate: 探索率（epsilon）
            learning_rate: 学习率
        """
        self.num_iterations = num_iterations
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.q_values = {}  # Q值表
        self.visit_counts = {}  # 访问计数
        
        print(f"[INFO] Collective RL Enhanced initialized")
        print(f"[INFO]   Iterations: {num_iterations}")
        print(f"[INFO]   Exploration rate: {exploration_rate}")
        print(f"[INFO]   Learning rate: {learning_rate}")
    
    def _get_state_key(self, skill_scores: List[Dict[str, Any]]) -> str:
        """
        获取状态键（简化版）
        
        Args:
            skill_scores: 技能评分列表
            
        Returns:
            state_key: 状态键
        """
        # 按分数排序并取Top-3
        sorted_skills = sorted(skill_scores, key=lambda x: x.get("final_score", 0.0), reverse=True)
        top_3 = [s.get("skill", {}).get("name", "Unknown") for s in sorted_skills[:3]]
        return "|".join(top_3)
    
    def _get_reward(self, combined_skill: Dict[str, Any], base_skills: List[Dict[str, Any]]) -> float:
        """
        计算奖励（简化版）
        
        Args:
            combined_skill: 组合后的技能
            base_skills: 基础技能列表
            
        Returns:
            reward: 奖励值
        """
        # 基于技能组合的多样性和质量计算奖励
        skill_names = [s.get("skill", {}).get("name", "") for s in base_skills]
        
        # 奖励1：技能多样性
        unique_names = len(set(skill_names))
        diversity_reward = unique_names / max(len(skill_names), 1)
        
        # 奖励2：平均质量
        avg_quality = sum(s.get("assessment", {}).get("quality_score", 0.5) for s in base_skills) / max(len(base_skills), 1)
        
        # 奖励3：组合效率（基于步骤数）
        total_steps = sum(len(s.get("skill", {}).get("steps", [])) for s in base_skills)
        efficiency_reward = 1.0 / (1.0 + total_steps / 10)  # 步骤越少，效率越高
        
        # 聚合奖励
        reward = (diversity_reward * 0.3 + avg_quality * 0.4 + efficiency_reward * 0.3)
        
        return reward
    
    def _select_action(self, state: str, available_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        选择动作（epsilon-greedy）
        
        Args:
            state: 当前状态
            available_skills: 可选技能列表
            
        Returns:
            selected: 选中的技能组合
        """
        # epsilon-greedy策略
        if random.random() < self.exploration_rate:
            # 探索：随机选择
            print(f"[INFO]   Exploration: randomly selecting {min(3, len(available_skills))} skills")
            selected = random.sample(available_skills, min(3, len(available_skills)))
        else:
            # 利用：选择Q值最高的组合
            print(f"[INFO]   Exploitation: selecting top skills by Q-value")
            
            # 简单策略：选择质量最高的技能
            sorted_skills = sorted(available_skills, 
                                 key=lambda x: x.get("assessment", {}).get("final_score", 0.0), 
                                 reverse=True)
            selected = sorted_skills[:min(3, len(sorted_skills))]
        
        return selected
    
    def _update_q_value(self, state: str, action: List[Dict[str, Any]], reward: float, next_state: str):
        """
        更新Q值（Q-learning）
        
        Args:
            state: 当前状态
            action: 动作
            reward: 奖励
            next_state: 下一状态
        """
        action_key = "|".join([s.get("skill", {}).get("name", "Unknown") for s in action])
        key = f"{state}->{action_key}"
        
        # 初始化Q值
        if key not in self.q_values:
            self.q_values[key] = 0.0
            self.visit_counts[key] = 0
        
        # Q-learning更新
        self.visit_counts[key] += 1
        alpha = self.learning_rate / (1.0 + self.visit_counts[key] * 0.1)  # 衰减学习率
        
        # 获取下一状态的最大Q值
        next_max_q = 0.0
        if next_state in self.q_values:
            next_max_q = max(self.q_values.values())  # 简化：使用全局最大
        
        # 更新Q值
        self.q_values[key] += alpha * (reward + 0.9 * next_max_q - self.q_values[key])
    
    def train(self, assessed_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        训练强化学习策略
        
        Args:
            assessed_skills: 评估后的技能列表
            
        Returns:
            best_combination: 最佳技能组合
        """
        print(f"\n[INFO] Collective RL: Training with {len(assessed_skills)} skills...")
        
        best_combination = None
        best_reward = -float("inf")
        training_log = []
        
        for iteration in range(self.num_iterations):
            print(f"\n[INFO] Iteration {iteration+1}/{self.num_iterations}")
            
            # 获取当前状态
            state = self._get_state_key(assessed_skills)
            print(f"[INFO]   State: {state[:50]}...")
            
            # 选择动作
            selected = self._select_action(state, assessed_skills)
            print(f"[INFO]   Selected: {[s.get('skill', {}).get('name', 'Unknown') for s in selected]}")
            
            # 计算奖励
            reward = self._get_reward(selected, selected)
            print(f"[INFO]   Reward: {reward:.3f}")
            
            # 获取下一状态
            next_state = self._get_state_key(assessed_skills)
            
            # 更新Q值
            self._update_q_value(state, selected, reward, next_state)
            
            # 记录训练日志
            training_log.append({
                "iteration": iteration + 1,
                "state": state,
                "selected": [s.get("skill", {}).get("name", "") for s in selected],
                "reward": reward
            })
            
            # 更新最佳组合
            if reward > best_reward:
                best_reward = reward
                best_combination = selected.copy()
                print(f"[INFO]   New best! Reward={best_reward:.3f}")
        
        print(f"\n[INFO] Training complete. Best reward: {best_reward:.3f}")
        
        return {
            "best_combination": best_combination,
            "best_reward": best_reward,
            "training_log": training_log,
            "q_values": self.q_values
        }
    
    def generate_augmented_prompt(self, task: str, best_combination: List[Dict[str, Any]]) -> str:
        """
        生成增强prompt
        
        Args:
            task: 原始任务描述
            best_combination: 最佳技能组合
            
        Returns:
            augmented_prompt: 增强后的prompt
        """
        print(f"\n[INFO] Generating augmented prompt...")
        
        # 构建技能描述
        skill_descriptions = []
        for skill in best_combination:
            skill_data = skill.get("skill", {})
            name = skill_data.get("name", "Unknown")
            desc = skill_data.get("description", "")
            steps = skill_data.get("steps", [])
            
            skill_desc = f"""
## {name}
Description: {desc}
Steps:
"""
            for i, step in enumerate(steps, 1):
                skill_desc += f"  {i}. {step}\n"
            
            skill_descriptions.append(skill_desc)
        
        # 构建增强prompt
        augmented_prompt = f"""Task: {task}

## Available Skills
You have access to the following collective skills that can be combined to solve this task:

{"=".join(skill_descriptions)}

## Strategy
1. Analyze the task and identify which skills are most relevant
2. Combine the selected skills to create an optimal solution
3. Execute the combined skills in the correct order
4. Adapt and refine as needed based on results

Generate a solution using the available skills.
"""
        
        print(f"[INFO] Augmented prompt generated ({len(augmented_prompt)} chars)")
        
        return augmented_prompt
    
    def save_results(self, results: Dict[str, Any], output_file: str):
        """保存训练结果"""
        print(f"\n[INFO] Saving results to: {output_file}")
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "num_iterations": self.num_iterations,
            "exploration_rate": self.exploration_rate,
            "learning_rate": self.learning_rate,
            "best_reward": results.get("best_reward", 0.0),
            "best_combination": results.get("best_combination", []),
            "training_log": results.get("training_log", []),
            "num_q_values": len(results.get("q_values", {}))
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Results saved successfully")


def main():
    parser = argparse.ArgumentParser(description="Collective RL Enhanced: Train RL strategy for skill combination")
    parser.add_argument("--assessed", type=str, required=True, help="Assessed skills JSON file")
    parser.add_argument("--task", type=str, default="读取PDF并提取文本", help="Original task")
    parser.add_argument("--iterations", type=int, default=5, help="Number of training iterations")
    parser.add_argument("--exploration", type=float, default=0.2, help="Exploration rate (epsilon)")
    parser.add_argument("--output", type=str, default="collective-rl-results.json", help="Output file")
    
    args = parser.parse_args()
    
    print("[INFO] Collective RL Enhanced: Collective Reinforcement Learning (Enhanced Version)")
    print("[INFO]   Skill combination optimization\n")
    
    # 加载评估后的技能
    print(f"[INFO] Loading assessed skills from: {args.assessed}")
    with open(args.assessed, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assessed_skills = data.get("candidates", [])
    
    print(f"[INFO] Skills loaded: {len(assessed_skills)}")
    
    # 初始化强化学习
    rl = CollectiveRLEnhanced(
        num_iterations=args.iterations,
        exploration_rate=args.exploration,
        learning_rate=0.1
    )
    
    # 训练
    results = rl.train(assessed_skills)
    
    # 生成增强prompt
    augmented_prompt = rl.generate_augmented_prompt(args.task, results.get("best_combination", []))
    
    # 保存结果
    rl.save_results(results, output_file=args.output)
    
    # 保存增强prompt
    prompt_file = args.output.replace(".json", "-prompt.txt")
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(augmented_prompt)
    print(f"[INFO] Augmented prompt saved to: {prompt_file}")
    
    # 打印摘要
    print(f"\n{'='*80}")
    print("COLLECTIVE RL ENHANCED SUMMARY")
    print(f"{'='*80}")
    print(f"Skills: {len(assessed_skills)}")
    print(f"Iterations: {args.iterations}")
    print(f"Best reward: {results.get('best_reward', 0.0):.3f}")
    print(f"Best combination:")
    for skill in results.get("best_combination", []):
        print(f"  - {skill.get('skill', {}).get('name', 'Unknown')}")
    print(f"Q-values learned: {len(results.get('q_values', {}))}")
    print(f"\nAugmented prompt length: {len(augmented_prompt)} chars")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
