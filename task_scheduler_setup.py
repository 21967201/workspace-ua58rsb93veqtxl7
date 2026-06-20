#!/usr/bin/env python3
"""
Task Scheduler Setup: 任务计划程序设置

创建Windows任务计划程序任务，以便自动执行auto-tasks.json中的周期性任务。
"""

import json
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict, Any


class TaskSchedulerSetup:
    """任务计划程序设置"""
    
    def __init__(self, tasks_file: str = "auto-tasks.json"):
        self.tasks_file = tasks_file
        self.tasks = []
        self.load_tasks()
    
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
    
    def get_weekly_tasks(self) -> List[Dict[str, Any]]:
        """获取所有周期性任务"""
        weekly_tasks = []
        
        for task in self.tasks:
            if task.get("schedule"):
                weekly_tasks.append(task)
        
        return weekly_tasks
    
    def create_scheduled_task(self, task: Dict[str, Any]) -> bool:
        """
        创建Windows任务计划程序任务
        
        Args:
            task: 任务数据
            
        Returns:
            success: 是否成功
        """
        task_name = f"QClaw-{task.get('name', 'Unknown')}"
        script = task.get("script", "")
        schedule = task.get("schedule", "")
        
        print(f"\n[INFO] Creating scheduled task: {task_name}")
        print(f"[INFO]   Schedule: {schedule}")
        print(f"[INFO]   Script: {script[:60]}...")
        
        # 构建schtasks命令
        # 注意：这里创建的是简化版任务，实际使用时需要根据schedule调整
        cmd = [
            "schtasks",
            "/create",
            "/tn", task_name,
            "/tr", f'python "{self.tasks_file.replace(chr(92), "/").replace("auto-tasks.json", "task_runner.py")}" --tasks-file "{self.tasks_file}"',
            "/sc", "weekly",  # 每周
            "/d", "MON",  # 周一
            "/st", "11:00",  # 11:00
            "/f"  # 强制覆盖
        ]
        
        print(f"[INFO]   Command: {' '.join(cmd)}")
        
        try:
            # 实际执行（已注释，实际运行时取消注释）
            # result = subprocess.run(cmd, capture_output=True, text=True)
            # if result.returncode == 0:
            #     print(f"[INFO]   Task created successfully")
            #     return True
            # else:
            #     print(f"[ERROR]   Task creation failed: {result.stderr}")
            #     return False
            
            # 模拟执行
            print(f"[INFO]   [SIMULATED] Task would be created")
            return True
        
        except Exception as e:
            print(f"[ERROR]   Task creation error: {e}")
            return False
    
    def setup_all_weekly_tasks(self, dry_run: bool = True):
        """
        设置所有周期性任务
        
        Args:
            dry_run: 干运行
        """
        print(f"\n[INFO] Setting up weekly tasks...")
        print(f"[INFO]   Dry run: {dry_run}")
        
        weekly_tasks = self.get_weekly_tasks()
        
        print(f"[INFO] Weekly tasks found: {len(weekly_tasks)}")
        
        for task in weekly_tasks:
            if dry_run:
                print(f"[INFO]   [DRY RUN] Would create: {task.get('name')}")
            else:
                success = self.create_scheduled_task(task)
                if success:
                    print(f"[INFO]   Created: {task.get('name')}")
                else:
                    print(f"[ERROR]   Failed to create: {task.get('name')}")
        
        print(f"\n[INFO] Setup complete")
    
    def generate_bat_file(self, output_file: str = "run-tasks.bat"):
        """
        生成批处理文件（用于手动运行）
        
        Args:
            output_file: 输出文件
        """
        print(f"\n[INFO] Generating batch file: {output_file}")
        
        content = f"""@echo off
REM Task Runner Batch File
REM Generated: {datetime.now().isoformat()}
REM 
REM This file runs all due tasks from auto-tasks.json

echo ========================================
echo QClaw Auto Task Runner
echo ========================================
echo.

cd /d "%~dp0"

echo Running Task Runner...
python task_runner.py --tasks-file auto-tasks.json

echo.
echo ========================================
echo Task Runner Complete
echo ========================================
pause
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[INFO] Batch file created: {output_file}")
            print(f"[INFO] Run this file manually to execute due tasks")
        
        except Exception as e:
            print(f"[ERROR] Failed to create batch file: {e}")
    
    def generate_powershell_scheduler(self, output_file: str = "setup-scheduled-task.ps1"):
        """
        生成PowerShell脚本（用于设置计划任务）
        
        Args:
            output_file: 输出文件
        """
        print(f"\n[INFO] Generating PowerShell scheduler: {output_file}")
        
        weekly_tasks = self.get_weekly_tasks()
        
        content = f"""# Task Scheduler Setup Script
# Generated: {datetime.now().isoformat()}
# Weekly tasks to schedule: {len(weekly_tasks)}

$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================"
Write-Host "QClaw Auto Task Scheduler Setup"
Write-Host "========================================"
Write-Host ""

"""
        
        for task in weekly_tasks:
            task_name = f"QClaw-{task.get('name', 'Unknown')}"
            schedule = task.get("schedule", "0 11 * * 1")
            
            # 解析简化的cron格式 (分 时 日 月 周)
            parts = schedule.split()
            if len(parts) >= 5:
                minute = parts[0]
                hour = parts[1]
                day_of_week = parts[4]
                
                # Windows schtasks使用不同的格式
                # 周一 = MON, 周三 = WED, 周五 = FRI
                day_map = {"1": "MON", "2": "TUE", "3": "WED", "4": "THU", "5": "FRI", "6": "SAT", "7": "SUN"}
                windows_day = day_map.get(day_of_week, "MON")
                
                content += f'''
# Task: {task.get('name')}
Write-Host "Creating scheduled task: {task_name}"

$taskAction = New-ScheduledTaskAction -Execute "python" -Argument 'task_runner.py --tasks-file auto-tasks.json' -WorkingDirectory $ScriptDir
$taskTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek {windows_day} -At "{hour}:{minute.zfill(2)}"
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "{task_name}" -Action $taskAction -Trigger $taskTrigger -Principal $taskPrincipal -Description "{task.get('description', '')}" -Force

Write-Host "  Created: {task_name}"
'''
        
        content += f"""
Write-Host ""
Write-Host "========================================"
Write-Host "Task Scheduler Setup Complete"
Write-Host "========================================"
Write-Host ""
Write-Host "Created {len(weekly_tasks)} scheduled tasks"
Write-Host ""
Write-Host "To view tasks, run: Get-ScheduledTask | Where-Object {{$_.TaskName -like 'QClaw-*'}}"
Write-Host "To remove all tasks, run: Get-ScheduledTask | Where-Object {{$_.TaskName -like 'QClaw-*'}} | Unregister-ScheduledTask -Confirm:$false"
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[INFO] PowerShell scheduler created: {output_file}")
            print(f"[INFO] Run with: powershell -ExecutionPolicy Bypass -File {output_file}")
        
        except Exception as e:
            print(f"[ERROR] Failed to create PowerShell scheduler: {e}")


def main():
    parser = argparse.ArgumentParser(description="Task Scheduler Setup: Create Windows scheduled tasks")
    parser.add_argument("--tasks-file", type=str, default="auto-tasks.json",
                       help="Tasks JSON file")
    parser.add_argument("--dry-run", action="store_true",
                       help="Dry run (don't actually create tasks)")
    parser.add_argument("--generate-bat", action="store_true",
                       help="Generate batch file")
    parser.add_argument("--generate-ps1", action="store_true",
                       help="Generate PowerShell scheduler")
    
    args = parser.parse_args()
    
    print("[INFO] Task Scheduler Setup")
    print("[INFO]   For P0 breakthrough auto-updates\n")
    
    # 初始化
    setup = TaskSchedulerSetup(tasks_file=args.tasks_file)
    
    # 生成批处理文件
    if args.generate_bat:
        setup.generate_bat_file()
        return
    
    # 生成PowerShell调度器
    if args.generate_ps1:
        setup.generate_powershell_scheduler()
        return
    
    # 设置所有周期性任务
    setup.setup_all_weekly_tasks(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
