# Task Scheduler Setup Script
# Generated: 2026-06-18T11:01:19.441104
# Weekly tasks to schedule: 3

$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================"
Write-Host "QClaw Auto Task Scheduler Setup"
Write-Host "========================================"
Write-Host ""


# Task: Weekly-Tech-Breakthrough-Monitor
Write-Host "Creating scheduled task: QClaw-Weekly-Tech-Breakthrough-Monitor"

$taskAction = New-ScheduledTaskAction -Execute "python" -Argument 'task_runner.py --tasks-file auto-tasks.json' -WorkingDirectory $ScriptDir
$taskTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek WED -At "13:00"
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "QClaw-Weekly-Tech-Breakthrough-Monitor" -Action $taskAction -Trigger $taskTrigger -Principal $taskPrincipal -Description "每周技术突破监控" -Force

Write-Host "  Created: QClaw-Weekly-Tech-Breakthrough-Monitor"

# Task: Weekly-Self-Evolution-Report
Write-Host "Creating scheduled task: QClaw-Weekly-Self-Evolution-Report"

$taskAction = New-ScheduledTaskAction -Execute "python" -Argument 'task_runner.py --tasks-file auto-tasks.json' -WorkingDirectory $ScriptDir
$taskTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek MON -At "11:00"
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "QClaw-Weekly-Self-Evolution-Report" -Action $taskAction -Trigger $taskTrigger -Principal $taskPrincipal -Description "每周自进化报告" -Force

Write-Host "  Created: QClaw-Weekly-Self-Evolution-Report"

# Task: Weekly-Task-Execution-Analysis
Write-Host "Creating scheduled task: QClaw-Weekly-Task-Execution-Analysis"

$taskAction = New-ScheduledTaskAction -Execute "python" -Argument 'task_runner.py --tasks-file auto-tasks.json' -WorkingDirectory $ScriptDir
$taskTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek MON -At "15:00"
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "QClaw-Weekly-Task-Execution-Analysis" -Action $taskAction -Trigger $taskTrigger -Principal $taskPrincipal -Description "每周任务执行分析" -Force

Write-Host "  Created: QClaw-Weekly-Task-Execution-Analysis"

Write-Host ""
Write-Host "========================================"
Write-Host "Task Scheduler Setup Complete"
Write-Host "========================================"
Write-Host ""
Write-Host "Created 3 scheduled tasks"
Write-Host ""
Write-Host "To view tasks, run: Get-ScheduledTask | Where-Object {$_.TaskName -like 'QClaw-*'}"
Write-Host "To remove all tasks, run: Get-ScheduledTask | Where-Object {$_.TaskName -like 'QClaw-*'} | Unregister-ScheduledTask -Confirm:$false"
