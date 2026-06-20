#!/usr/bin/env python3
"""
CSTS Enhanced Pipeline: 完整流水线测试

按顺序执行：CSN-Gen → CSN-Assess → Skill Tree → Collective RL
"""

import json
import subprocess
import sys
from datetime import datetime


def run_command(cmd: list, description: str) -> bool:
    """运行命令并检查结果"""
    print(f"\n{'='*80}")
    print(f"[PIPELINE] {description}")
    print(f"{'='*80}")
    print(f"[CMD] {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"[SUCCESS] {description} completed successfully")
            print(result.stdout)
            return True
        else:
            print(f"[ERROR] {description} failed with return code {result.returncode}")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] {description} failed with exception: {e}")
        return False


def main():
    print("[PIPELINE] CSTS Enhanced: Full Pipeline Test")
    print("[PIPELINE]   Gen → Assess → Tree → RL\n")
    
    task = "读取PDF文件并提取文本内容"
    model = "qclaw/pool-hy3-preview"
    
    # 步骤1: CSN-Gen Enhanced
    success = run_command(
        ["python", "skills/csts-skill-generator/scripts/csn_gen_enhanced.py",
         "--task", task,
         "--models", model,
         "--num-candidates", "5",
         "--output", "pipeline-candidates.json"],
        "Step 1: CSN-Gen Enhanced"
    )
    if not success:
        print("[PIPELINE] ❌ Pipeline failed at Step 1")
        return
    
    # 步骤2: CSN-Assess Enhanced
    success = run_command(
        ["python", "skills/csts-skill-generator/scripts/csn_assess_enhanced.py",
         "--candidates", "pipeline-candidates.json",
         "--judge-model", model,
         "--num-judges", "3",
         "--top-k", "3",
         "--output", "pipeline-assessed.json"],
        "Step 2: CSN-Assess Enhanced"
    )
    if not success:
        print("[PIPELINE] ❌ Pipeline failed at Step 2")
        return
    
    # 步骤3: Skill Tree Enhanced
    success = run_command(
        ["python", "skills/csts-skill-generator/scripts/skill_tree_enhanced.py",
         "--assessed", "pipeline-assessed.json",
         "--output", "pipeline-skill-tree.json"],
        "Step 3: Skill Tree Enhanced"
    )
    if not success:
        print("[PIPELINE] ❌ Pipeline failed at Step 3")
        return
    
    # 步骤4: Collective RL Enhanced
    success = run_command(
        ["python", "skills/csts-skill-generator/scripts/collective_rl_enhanced.py",
         "--assessed", "pipeline-assessed.json",
         "--task", task,
         "--iterations", "5",
         "--output", "pipeline-rl-results.json"],
        "Step 4: Collective RL Enhanced"
    )
    if not success:
        print("[PIPELINE] ❌ Pipeline failed at Step 4")
        return
    
    # 步骤5: 验证最终结果
    print(f"\n{'='*80}")
    print("[PIPELINE] Step 5: Validation")
    print(f"{'='*80}")
    
    try:
        # 读取最终结果
        with open("pipeline-rl-results.json", 'r', encoding='utf-8') as f:
            rl_results = json.load(f)
        
        best_combination = rl_results.get("best_combination", [])
        best_reward = rl_results.get("best_reward", 0.0)
        
        print(f"[VALIDATION] Best reward: {best_reward:.3f}")
        print(f"[VALIDATION] Best combination ({len(best_combination)} skills):")
        for i, skill in enumerate(best_combination, 1):
            name = skill.get("skill", {}).get("name", "Unknown")
            print(f"[VALIDATION]   {i}. {name}")
        
        # 读取增强prompt
        with open("pipeline-rl-results-prompt.txt", 'r', encoding='utf-8') as f:
            augmented_prompt = f.read()
        
        print(f"[VALIDATION] Augmented prompt length: {len(augmented_prompt)} chars")
        print(f"[VALIDATION] ✅ Pipeline completed successfully!")
        
        # 保存流水线摘要
        summary = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "model": model,
            "steps_completed": 4,
            "best_reward": best_reward,
            "best_combination": [s.get("skill", {}).get("name", "") for s in best_combination],
            "augmented_prompt_length": len(augmented_prompt)
        }
        
        with open("pipeline-summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n[PIPELINE] ✅ All steps completed successfully!")
        print(f"[PIPELINE] Summary saved to: pipeline-summary.json")
        
    except Exception as e:
        print(f"[VALIDATION] ❌ Validation failed: {e}")
        return
    
    print(f"\n{'='*80}")
    print("[PIPELINE] CSTS ENHANCED PIPELINE COMPLETE")
    print(f"{'='*80}")
    print(f"Task: {task}")
    print(f"Model: {model}")
    print(f"Best reward: {best_reward:.3f}")
    print(f"Output files:")
    print(f"  - pipeline-candidates.json")
    print(f"  - pipeline-assessed.json")
    print(f"  - pipeline-skill-tree.json")
    print(f"  - pipeline-rl-results.json")
    print(f"  - pipeline-rl-results-prompt.txt")
    print(f"  - pipeline-summary.json")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
