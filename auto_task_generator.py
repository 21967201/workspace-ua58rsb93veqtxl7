#!/usr/bin/env python3
"""
Auto Task Generator: 自动任务生成器

基于今天完成的P0突破集成工作，生成后续自动更新任务。
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any


class AutoTaskGenerator:
    """自动任务生成器"""
    
    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir
        self.tasks = []
        
    def generate_csts_tasks(self):
        """生成CSTS相关自动任务"""
        print("[INFO] Generating CSTS auto tasks...")
        
        tasks = [
            {
                "name": "CSTS-Enhance-CSN-Gen",
                "description": "增强CSN-Gen：实际调用LLM API",
                "priority": "HIGH",
                "estimated_hours": 4,
                "dependencies": [],
                "next_run": (datetime.now() + timedelta(days=1)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/csn_gen_enhanced.py --task 'Read PDF' --models 'qclaw/pool-hy3-preview' --output candidates.json"
            },
            {
                "name": "CSTS-Enhance-CSN-Assess",
                "description": "增强CSN-Assess：实现LLM-as-a-Judge",
                "priority": "HIGH",
                "estimated_hours": 6,
                "dependencies": ["CSTS-Enhance-CSN-Gen"],
                "next_run": (datetime.now() + timedelta(days=2)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/csn_assess_enhanced.py --candidates candidates.json --output assessed.json"
            },
            {
                "name": "CSTS-Benchmark-Eval",
                "description": "在GAIA/SWE-bench上评估CSTS",
                "priority": "MEDIUM",
                "estimated_hours": 8,
                "dependencies": ["CSTS-Enhance-CSN-Assess"],
                "next_run": (datetime.now() + timedelta(days=7)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/benchmark_eval.py --benchmark gaia --output csts-benchmark-results.json"
            }
        ]
        
        self.tasks.extend(tasks)
        print(f"[INFO]   Generated {len(tasks)} CSTS tasks")
        
    def generate_skillspector_tasks(self):
        """生成SkillSpector相关自动任务"""
        print("[INFO] Generating SkillSpector auto tasks...")
        
        tasks = [
            {
                "name": "SkillSpector-Expand-Patterns",
                "description": "扩展漏洞模式到64个（16类风险）",
                "priority": "HIGH",
                "estimated_hours": 6,
                "dependencies": [],
                "next_run": (datetime.now() + timedelta(days=1)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/skillspector_expand.py --output skillspector-full.json"
            },
            {
                "name": "SkillSpector-LLM-Semantic",
                "description": "实现LLM语义分析",
                "priority": "MEDIUM",
                "estimated_hours": 5,
                "dependencies": ["SkillSpector-Expand-Patterns"],
                "next_run": (datetime.now() + timedelta(days=3)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/skillspector_llm.py --input test-skill.md --output report-llm.json"
            },
            {
                "name": "SkillSpector-CI-CD",
                "description": "集成到CI/CD流水线",
                "priority": "LOW",
                "estimated_hours": 3,
                "dependencies": ["SkillSpector-LLM-Semantic"],
                "next_run": (datetime.now() + timedelta(days=5)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/skillspector_ci.py --config ci-config.json"
            }
        ]
        
        self.tasks.extend(tasks)
        print(f"[INFO]   Generated {len(tasks)} SkillSpector tasks")
        
    def generate_egss_tasks(self):
        """生成EGSS相关自动任务"""
        print("[INFO] Generating EGSS auto tasks...")
        
        tasks = [
            {
                "name": "EGSS-Integrate-Logprobs",
                "description": "集成真实LLM logprobs计算熵",
                "priority": "HIGH",
                "estimated_hours": 5,
                "dependencies": [],
                "next_run": (datetime.now() + timedelta(days=2)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/egss_logprobs.py --skills memory/csts-skill-tree.json --output egss-logprobs-results.json"
            },
            {
                "name": "EGSS-Full-Loop",
                "description": "实现完整的熵引导循环",
                "priority": "MEDIUM",
                "estimated_hours": 7,
                "dependencies": ["EGSS-Integrate-Logprobs"],
                "next_run": (datetime.now() + timedelta(days=4)).isoformat(),
                "script": "python skills/csts-skill-generator/scripts/egss_full_loop.py --task 'Complex task' --iterations 5 --output egss-loop-results.json"
            }
        ]
        
        self.tasks.extend(tasks)
        print(f"[INFO]   Generated {len(tasks)} EGSS tasks")
        
    def generate_p1_evaluation_tasks(self):
        """生成P1级突破评估任务"""
        print("[INFO] Generating P1 evaluation tasks...")
        
        tasks = [
            {
                "name": "P1-Evaluate-superpowers",
                "description": "评估superpowers (8.5/10)",
                "priority": "MEDIUM",
                "estimated_hours": 4,
                "dependencies": [],
                "next_run": (datetime.now() + timedelta(days=3)).isoformat(),
                "script": "python scripts/evaluate_p1.py --breakthrough superpowers --output p1-superpowers-eval.json"
            },
            {
                "name": "P1-Evaluate-agent-skills",
                "description": "评估agent-skills (8.3/10)",
                "priority": "MEDIUM",
                "estimated_hours": 4,
                "dependencies": [],
                "next_run": (datetime.now() + timedelta(days=4)).isoformat(),
                "script": "python scripts/evaluate_p1.py --breakthrough agent-skills --output p1-agent-skills-eval.json"
            }
        ]
        
        self.tasks.extend(tasks)
        print(f"[INFO]   Generated {len(tasks)} P1 evaluation tasks")
        
    def generate_weekly_maintenance_tasks(self):
        """生成每周维护任务"""
        print("[INFO] Generating weekly maintenance tasks...")
        
        tasks = [
            {
                "name": "Weekly-Tech-Breakthrough-Monitor",
                "description": "每周技术突破监控",
                "priority": "HIGH",
                "estimated_hours": 2,
                "schedule": "0 13 * * 3",  # 每周三 13:00
                "script": "python scripts/tech_breakthrough_monitor.py --output weekly-tech-report.json"
            },
            {
                "name": "Weekly-Self-Evolution-Report",
                "description": "每周自进化报告",
                "priority": "HIGH",
                "estimated_hours": 3,
                "schedule": "0 11 * * 1",  # 每周一 11:00
                "script": "python scripts/self_evolution_report.py --output weekly-evolution-report.json"
            },
            {
                "name": "Weekly-Task-Execution-Analysis",
                "description": "每周任务执行分析",
                "priority": "MEDIUM",
                "estimated_hours": 2,
                "schedule": "0 15 * * 1",  # 每周一 15:00
                "script": "python scripts/task_execution_analysis.py --output weekly-task-analysis.json"
            }
        ]
        
        self.tasks.extend(tasks)
        print(f"[INFO]   Generated {len(tasks)} weekly maintenance tasks")
        
    def save_tasks(self, output_file: str):
        """保存任务列表到文件"""
        print(f"\n[INFO] Saving {len(self.tasks)} tasks to: {output_file}")
        
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "workspace": self.workspace_dir,
            "total_tasks": len(self.tasks),
            "tasks": self.tasks
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Tasks saved successfully")
        
    def print_summary(self):
        """打印任务摘要"""
        print(f"\n{'='*80}")
        print("AUTO TASK GENERATION SUMMARY")
        print(f"{'='*80}")
        print(f"Total tasks generated: {len(self.tasks)}")
        print(f"\nBy priority:")
        
        priority_counts = {}
        for task in self.tasks:
            priority = task.get("priority", "LOW")
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        for priority in ["HIGH", "MEDIUM", "LOW"]:
            count = priority_counts.get(priority, 0)
            print(f"  {priority}: {count} tasks")
        
        print(f"\nBy category:")
        categories = {
            "CSTS": [t for t in self.tasks if "CSTS" in t["name"]],
            "SkillSpector": [t for t in self.tasks if "SkillSpector" in t["name"]],
            "EGSS": [t for t in self.tasks if "EGSS" in t["name"]],
            "P1-Evaluation": [t for t in self.tasks if "P1" in t["name"]],
            "Weekly-Maintenance": [t for t in self.tasks if "Weekly" in t["name"]]
        }
        
        for cat, tasks in categories.items():
            print(f"  {cat}: {len(tasks)} tasks")
        
        print(f"\nNext runs:")
        for task in sorted(self.tasks, key=lambda x: x.get("next_run", "9999"))[:5]:
            print(f"  {task['name']}: {task.get('next_run', 'N/A')}")
        
        print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(description="Auto Task Generator: Generate automated tasks for P0 breakthroughs")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace directory")
    parser.add_argument("--output", type=str, default="auto-tasks.json", help="Output tasks JSON file")
    parser.add_argument("--category", type=str, choices=["all", "csts", "skillspector", "egss", "p1", "weekly"],
                       default="all", help="Task category to generate")
    
    args = parser.parse_args()
    
    print("[INFO] Auto Task Generator")
    print("[INFO]   Based on 2026-06-18 P0 breakthrough integration work\n")
    
    # Initialize generator
    generator = AutoTaskGenerator(workspace_dir=args.workspace)
    
    # Generate tasks by category
    if args.category in ["all", "csts"]:
        generator.generate_csts_tasks()
    
    if args.category in ["all", "skillspector"]:
        generator.generate_skillspector_tasks()
    
    if args.category in ["all", "egss"]:
        generator.generate_egss_tasks()
    
    if args.category in ["all", "p1"]:
        generator.generate_p1_evaluation_tasks()
    
    if args.category in ["all", "weekly"]:
        generator.generate_weekly_maintenance_tasks()
    
    # Save tasks
    generator.save_tasks(output_file=args.output)
    
    # Print summary
    generator.print_summary()


if __name__ == "__main__":
    main()
