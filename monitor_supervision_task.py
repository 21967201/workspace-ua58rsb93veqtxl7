#!/usr/bin/env python3
"""
监控监督任务执行情况
监控"规则执行监督（自动任务时间限制）"任务是否按预期工作
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timezone
import glob

def get_supervision_task():
    """获取监督任务"""
    try:
        result = subprocess.run(
            ["cron", "list", "includeDisabled=true"],
            capture_output=True,
            text=True,
            check=True
        )
        tasks_json = result.stdout
        tasks_data = json.loads(tasks_json)
        all_tasks = tasks_data.get("jobs", [])
        
        # 查找监督任务
        for task in all_tasks:
            if "规则执行监督" in task.get("name", ""):
                return task
        
        return None
    except Exception as e:
        print(f"获取监督任务失败: {e}")
        return None

def check_supervision_task_status(task):
    """检查监督任务执行状态"""
    if not task:
        return {
            "task_found": False,
            "error": "未找到监督任务"
        }
    
    task_id = task.get("id", "unknown")
    task_name = task.get("name", "unknown")
    
    state = task.get("state", {})
    last_run_at_ms = state.get("lastRunAtMs")
    last_run_status = state.get("lastRunStatus")
    consecutive_errors = state.get("consecutiveErrors", 0)
    
    # 检查最后执行时间是否在合理范围内（过去24小时内）
    execution_time_ok = False
    last_run_time_str = "未知"
    
    if last_run_at_ms:
        last_run_time = datetime.fromtimestamp(last_run_at_ms / 1000, tz=timezone.utc)
        last_run_time_str = last_run_time.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        current_time = datetime.now(timezone.utc)
        time_diff_hours = (current_time - last_run_time).total_seconds() / 3600
        
        # 如果任务在过去24小时内执行过，认为执行时间OK
        if time_diff_hours <= 24:
            execution_time_ok = True
    
    # 检查执行状态
    execution_status_ok = (last_run_status == "ok")
    
    # 检查连续错误
    no_consecutive_errors = (consecutive_errors == 0)
    
    return {
        "task_found": True,
        "task_id": task_id,
        "task_name": task_name,
        "last_run_at_ms": last_run_at_ms,
        "last_run_time_str": last_run_time_str,
        "last_run_status": last_run_status,
        "consecutive_errors": consecutive_errors,
        "execution_time_ok": execution_time_ok,
        "execution_status_ok": execution_status_ok,
        "no_consecutive_errors": no_consecutive_errors,
        "overall_ok": execution_time_ok and execution_status_ok and no_consecutive_errors
    }

def check_supervision_report():
    """检查监督报告是否生成"""
    # 查找最新的监督报告文件
    report_pattern = "rule_enforcement_monitor_report_*.json"
    report_files = glob.glob(report_pattern)
    
    if not report_files:
        return {
            "report_found": False,
            "error": "未找到监督报告文件"
        }
    
    # 按修改时间排序，取最新的
    latest_report = max(report_files, key=os.path.getmtime)
    latest_report_mtime = os.path.getmtime(latest_report)
    latest_report_time = datetime.fromtimestamp(latest_report_mtime, tz=timezone.utc)
    
    # 检查报告生成时间是否在合理范围内（过去24小时内）
    current_time = datetime.now(timezone.utc)
    time_diff_hours = (current_time - latest_report_time).total_seconds() / 3600
    
    report_generated_ok = (time_diff_hours <= 24)
    
    # 读取报告内容
    try:
        with open(latest_report, "r", encoding="utf-8") as f:
            report_content = json.load(f)
            
        return {
            "report_found": True,
            "report_file": latest_report,
            "report_generated_at": latest_report_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "report_generated_ok": report_generated_ok,
            "report_content": report_content,
            "compliant_count": report_content.get("compliant_count", 0),
            "non_compliant_count": report_content.get("non_compliant_count", 0),
            "compliance_rate": report_content.get("compliance_rate", "0%")
        }
    except Exception as e:
        return {
            "report_found": True,
            "report_file": latest_report,
            "report_generated_at": latest_report_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "report_generated_ok": report_generated_ok,
            "error": f"读取报告内容失败: {e}"
        }

def check_alert_push():
    """检查告警推送是否成功"""
    # 查找最新的告警推送文件
    alert_pattern = "规则执行监督告警_*.json"
    alert_files = glob.glob(alert_pattern)
    
    if not alert_files:
        return {
            "alert_found": False,
            "message": "未找到告警推送文件（可能所有任务都符合规则，无需告警）"
        }
    
    # 按修改时间排序，取最新的
    latest_alert = max(alert_files, key=os.path.getmtime)
    latest_alert_mtime = os.path.getmtime(latest_alert)
    latest_alert_time = datetime.fromtimestamp(latest_alert_mtime, tz=timezone.utc)
    
    # 检查告警文件生成时间是否在合理范围内（过去24小时内）
    current_time = datetime.now(timezone.utc)
    time_diff_hours = (current_time - latest_alert_time).total_seconds() / 3600
    
    alert_push_ok = (time_diff_hours <= 24)
    
    return {
        "alert_found": True,
        "alert_file": latest_alert,
        "alert_generated_at": latest_alert_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "alert_push_ok": alert_push_ok
    }

def main():
    print("开始监控监督任务执行情况...")
    
    # 步骤1：检查监督任务执行状态
    print("\n=== 监督任务执行状态检查 ===")
    supervision_task = get_supervision_task()
    task_status = check_supervision_task_status(supervision_task)
    
    if task_status["task_found"]:
        status_icon = "✅" if task_status["overall_ok"] else "❌"
        print(f"{status_icon} 监督任务: {task_status['task_name']}")
        print(f"   最后执行时间: {task_status['last_run_time_str']}")
        print(f"   最后执行状态: {task_status['last_run_status']}")
        print(f"   连续错误次数: {task_status['consecutive_errors']}")
        print(f"   执行时间正常: {'是' if task_status['execution_time_ok'] else '否'}")
        print(f"   执行状态正常: {'是' if task_status['execution_status_ok'] else '否'}")
        print(f"   无连续错误: {'是' if task_status['no_consecutive_errors'] else '否'}")
    else:
        print(f"❌ {task_status['error']}")
    
    # 步骤2：检查监督报告生成
    print("\n=== 监督报告生成检查 ===")
    report_status = check_supervision_report()
    
    if report_status["report_found"]:
        status_icon = "✅" if report_status["report_generated_ok"] else "❌"
        print(f"{status_icon} 监督报告: {report_status['report_file']}")
        print(f"   报告生成时间: {report_status['report_generated_at']}")
        print(f"   报告生成正常: {'是' if report_status['report_generated_ok'] else '否'}")
        
        if "report_content" in report_status:
            print(f"   符合规则任务数: {report_status['compliant_count']}")
            print(f"   不符合规则任务数: {report_status['non_compliant_count']}")
            print(f"   规则符合率: {report_status['compliance_rate']}")
    else:
        print(f"❌ {report_status['error']}")
    
    # 步骤3：检查告警推送
    print("\n=== 告警推送检查 ===")
    alert_status = check_alert_push()
    
    if alert_status["alert_found"]:
        status_icon = "✅" if alert_status["alert_push_ok"] else "❌"
        print(f"{status_icon} 告警推送: {alert_status['alert_file']}")
        print(f"   告警生成时间: {alert_status['alert_generated_at']}")
        print(f"   告警推送正常: {'是' if alert_status['alert_push_ok'] else '否'}")
    else:
        print(f"ℹ️  {alert_status['message']}")
    
    # 步骤4：生成监控报告
    print("\n=== 生成监控报告 ===")
    
    # 创建报告
    report = {
        "monitor_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "supervision_task_status": task_status,
        "supervision_report_status": report_status,
        "alert_push_status": alert_status,
        "overall_ok": (
            task_status.get("overall_ok", False) and
            report_status.get("report_generated_ok", False) and
            (not alert_status.get("alert_found", False) or alert_status.get("alert_push_ok", False))
        )
    }
    
    # 保存报告
    report_file = f"monitoring_report_supervision_task_{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 监控报告已保存: {report_file}")
    
    # 打印总结
    overall_ok = report["overall_ok"]
    status_icon = "✅" if overall_ok else "❌"
    print(f"\n{status_icon} 监督任务监控总结: {'一切正常' if overall_ok else '发现问题'}")
    
    # 步骤5：如果有问题，推送告警
    if not overall_ok:
        print("\n=== 推送告警 ===")
        
        alert_content = "监督任务监控发现以下问题：\n"
        
        if not task_status.get("overall_ok", False):
            alert_content += "- 监督任务执行异常\n"
            
        if not report_status.get("report_generated_ok", False):
            alert_content += "- 监督报告生成异常\n"
            
        if alert_status.get("alert_found", False) and not alert_status.get("alert_push_ok", False):
            alert_content += "- 告警推送异常\n"
        
        print(f"告警内容: {alert_content}")
        
        # 这里可以调用推送逻辑
        # 例如：调用today-task技能推送告警
        print("告警推送功能待实现...")
    else:
        print("\n✅ 监督任务运行正常，无需推送告警")

if __name__ == "__main__":
    main()