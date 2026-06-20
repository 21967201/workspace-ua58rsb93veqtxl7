#!/usr/bin/env python3
"""
Task Runner: 自动任务执行器

读取auto-tasks.json，检查并执行到期的任务。
支持单次任务、周期性任务、依赖检查。
"""

import json
import argparse
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pathlib import Path


class TaskRunner:
    """自动任务执行器"""
    
    def __init__(self, tasks_file: str = "auto-tasks.json"):
        """
        Args:
            tasks_file: 任务配置文件路径
        """
        self.tasks_file = tasks_file
        self.tasks = []
        self.execution_log = []
        
        # 加载任务
        self.load_tasks()
        
        print(f"[INFO] TaskRunner initialized")
        print(f"[INFO]   Tasks file: {tasks_file}")
        print(f"[INFO]   Total tasks: {len(self.tasks)}")
    
    def load_tasks(self):
        """加载任务列表"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                print(f"[INFO] Tasks loaded: {len(self.tasks)}")
        except Exception as e:
            print(f"[ERROR] Failed to load tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """保存任务列表（更新next_run等）"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["tasks"] = self.tasks
            
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[INFO] Tasks saved to: {self.tasks_file}")
        except Exception as e:
            print(f"[ERROR] Failed to save tasks: {e}")
    
    def get_due_tasks(self) -> List[Dict[str, Any]]:
        """
        获取所有到期的任务
        
        Returns:
            due_tasks: 到期的任务列表
        """
        now = datetime.now()
        due_tasks = []
        
        for task in self.tasks:
            # 检查next_run
            next_run_str = task.get("next_run")
            if not next_run_str:
                continue
            
            next_run = datetime.fromisoformat(next_run_str)
            
            if next_run <= now:
                due_tasks.append(task)
        
        return due_tasks
    
    def check_dependencies(self, task: Dict[str, Any]) -> bool:
        """
        检查任务依赖是否满足
        
        Args:
            task: 任务数据
            
        Returns:
            satisfied: 依赖是否满足
        """
        dependencies = task.get("dependencies", [])
        
        if not dependencies:
            return True  # 无依赖
        
        # 检查每个依赖是否已成功执行
        for dep_name in dependencies:
            dep_completed = self._is_dependency_completed(dep_name)
            if not dep_completed:
                print(f"[INFO]   Dependency not satisfied: {dep_name}")
                return False
        
        return True
    
    def _is_dependency_completed(self, dep_name: str) -> bool:
        """
        检查依赖任务是否已成功完成
        
        Args:
            dep_name: 依赖任务名称
            
        Returns:
            completed: 是否已完成
        """
        # 检查执行日志
        for log in self.execution_log:
            if log.get("task_name") == dep_name and log.get("status") == "success":
                return True
        
        # 也可以检查任务特定的完成标记文件
        # 这里简化为只检查日志
        
        return False
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个任务
        
        Args:
            task: 任务数据
            
        Returns:
            result: 执行结果 {"status": "success"/"failed", "output": ...}
        """
        task_name = task.get("name", "Unknown")
        script = task.get("script", "")
        
        print(f"\n[INFO] Executing task: {task_name}")
        print(f"[INFO]   Script: {script[:80]}...")
        
        # 检查依赖
        if not self.check_dependencies(task):
            print(f"[WARN]   Dependencies not satisfied, skipping")
            return {"status": "skipped", "reason": "dependencies not satisfied"}
        
        # 执行脚本
        try:
            result = subprocess.run(
                script,
                shell=True,
                capture_output=True,
                text=True,
                timeout=3600  # 1小时超时
            )
            
            if result.returncode == 0:
                print(f"[INFO]   Task executed successfully")
                print(f"[INFO]   Output: {result.stdout[:200]}...")
                
                # 记录日志
                log_entry = {
                    "task_name": task_name,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "returncode": result.returncode,
                    "output": result.stdout[:500]  # 截断
                }
                self.execution_log.append(log_entry)
                
                return {"status": "success", "output": result.stdout}
            else:
                print(f"[ERROR]   Task failed (returncode={result.returncode})")
                print(f"[ERROR]   Error: {result.stderr[:200]}...")
                
                # 记录日志
                log_entry = {
                    "task_name": task_name,
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed",
                    "returncode": result.returncode,
                    "error": result.stderr[:500]
                }
                self.execution_log.append(log_entry)
                
                return {"status": "failed", "error": result.stderr}
        
        except subprocess.TimeoutExpired:
            print(f"[ERROR]   Task timed out (1 hour)")
            return {"status": "timeout"}
        
        except Exception as e:
            print(f"[ERROR]   Task execution error: {e}")
            return {"status": "error", "message": str(e)}
    
    def update_next_run(self, task: Dict[str, Any]):
        """
        更新任务的next_run时间
        
        Args:
            task: 任务数据
        """
        schedule = task.get("schedule")
        
        if schedule:
            # 周期性任务：解析cron表达式并更新next_run
            # 简化版：假设schedule是cron格式（如 "0 13 * * 3"）
            # 这里需要实现cron解析逻辑
            # 简化：假设是每周任务，加7天
            if "weekly" in task.get("description", "").lower():
                next_run = datetime.now() + timedelta(days=7)
            else:
                # 默认：加1天
                next_run = datetime.now() + timedelta(days=1)
        else:
            # 单次任务：设置为未来（表示已完成）
            next_run = datetime.now() + timedelta(days=365)  # 1年后
        
        task["next_run"] = next_run.isoformat()
        print(f"[INFO]   Next run updated: {next_run.isoformat()}")
    
    def run(self, dry_run: bool = False):
        """
        运行Task Runner：检查并执行所有到期任务
        
        Args:
            dry_run: 干运行（不实际执行）
        """
        print(f"\n[INFO] TaskRunner starting...")
        print(f"[INFO]   Dry run: {dry_run}")
        
        # 获取到期任务
        due_tasks = self.get_due_tasks()
        
        print(f"[INFO] Due tasks: {len(due_tasks)}")
        
        if not due_tasks:
            print(f"[INFO] No due tasks, exiting")
            return
        
        # 按优先级排序
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        due_tasks.sort(key=lambda t: priority_order.get(t.get("priority", "LOW"), 2))
        
        # 执行任务
        for task in due_tasks:
            task_name = task.get("name", "Unknown")
            
            print(f"\n[INFO] Processing task: {task_name}")
            
            if dry_run:
                print(f"[INFO]   [DRY RUN] Would execute: {task.get('script', '')[:60]}...")
                continue
            
            # 执行任务
            result = self.execute_task(task)
            
            # 更新next_run
            if result["status"] == "success":
                self.update_next_run(task)
        
        # 保存更新后的任务列表
        self.save_tasks()
        
        # 保存执行日志
        self._save_execution_log()
        
        print(f"\n[INFO] TaskRunner completed")
        print(f"[INFO]   Tasks processed: {len(due_tasks)}")
        print(f"[INFO]   Execution log: task-runner-log.json")
    
    def _save_execution_log(self):
        """保存执行日志"""
        log_file = "task-runner-log.json"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "last_update": datetime.now().isoformat(),
                    "total_executions": len(self.execution_log),
                    "log": self.execution_log[-100:]  # 只保留最近100条
                }, f, indent=2, ensure_ascii=False)
            
            print(f"[INFO] Execution log saved: {log_file}")
        except Exception as e:
            print(f"[ERROR] Failed to save execution log: {e}")
    
    def list_tasks(self):
        """列出所有任务"""
        print(f"\n[INFO] Task List ({len(self.tasks)} tasks):")
        print(f"{'='*80}")
        
        for i, task in enumerate(self.tasks):
            name = task.get("name", "Unknown")
            priority = task.get("priority", "LOW")
            next_run = task.get("next_run", "N/A")
            
            print(f"{i+1}. {name} (Priority: {priority})")
            print(f"   Next run: {next_run}")
            print(f"   Script: {task.get('script', '')[:60]}...")
            print()
        
        print(f"{'='*80}")


def main():
    parser = argparse.ArgumentParser(description="Task Runner: Automated task executor")
    parser.add_argument("--tasks-file", type=str, default="auto-tasks.json", 
                       help="Tasks JSON file")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Dry run (don't actually execute tasks)")
    parser.add_argument("--list", action="store_true", 
                       help="List all tasks")
    parser.add_argument("--check-due", action="store_true", 
                       help="Check and show due tasks")
    
    args = parser.parse_args()
    
    print("[INFO] TaskRunner: Automated Task Executor")
    print("[INFO]   For P0 breakthrough auto-updates\n")
    
    # 初始化
    runner = TaskRunner(tasks_file=args.tasks_file)
    
    # 列出任务
    if args.list:
        runner.list_tasks()
        return
    
    # 检查到期任务
    if args.check_due:
        due_tasks = runner.get_due_tasks()
        print(f"\n[INFO] Due tasks ({len(due_tasks)}):")
        for task in due_tasks:
            print(f"  - {task.get('name')} (due: {task.get('next_run')})")
        return
    
    # 运行
    runner.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
