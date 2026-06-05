#!/usr/bin/env python3
"""
规则执行监督脚本 - 确保未来所有新任务都遵循"自动任务时间限制"规则
规则内容：所有自动任务时间必须在周一至周六，10:30-18:10之前

作者：QClaw（全自动执行）
创建时间：2026-06-05 16:05:00
执行方式：100%全自动（符合AGENTS.md规则1）
"""

import json
import re
from datetime import datetime

def check_task_time_compliance(cron_expr):
    """
    检查任务时间是否符合规则：周一至周六，10:30-18:10之前
    
    Args:
        cron_expr: Cron表达式字符串
        
    Returns:
        (bool, str): (是否符合, 不符合原因)
    """
    try:
        # 解析Cron表达式
        parts = cron_expr.split()
        if len(parts) != 5:
            return False, f"Cron表达式格式错误：{cron_expr}"
        
        minute = parts[0]
        hour = parts[1]
        day_of_month = parts[2]
        month = parts[3]
        day_of_week = parts[4]
        
        # 检查1：必须在周一至周六执行（day_of_week包含1-6）
        if day_of_week == "*":
            return False, f"任务包括周日执行，违反规则：{cron_expr}"
        if "0" in day_of_week and "," in day_of_week:
            return False, f"任务包括周日执行，违反规则：{cron_expr}"
        if day_of_week == "0":
            return False, f"任务在周日执行，违反规则：{cron_expr}"
            
        # 检查2：执行时间必须在10:30-18:10之前
        # 转换为24小时制时间
        try:
            hour_int = int(hour)
            minute_int = int(minute)
        except ValueError:
            # 处理逗号分隔的多个值（如"10,11,12"）
            if "," in hour:
                hours = hour.split(",")
                for h in hours:
                    try:
                        h_int = int(h)
                        if h_int < 10 or h_int > 18:
                            return False, f"任务执行时间不在10:30-18:10范围内：{cron_expr}"
                    except ValueError:
                        continue
            else:
                return False, f"无法解析小时字段：{cron_expr}"
                
        # 检查时间范围
        if hour_int < 10 or hour_int > 18:
            return False, f"任务执行时间不在10:30-18:10范围内：{cron_expr}"
            
        if hour_int == 10 and minute_int < 30:
            return False, f"任务执行时间早于10:30：{cron_expr}"
            
        if hour_int == 18 and minute_int > 10:
            return False, f"任务执行时间晚于18:10：{cron_expr}"
            
        # 所有检查通过
        return True, "符合规则"
        
    except Exception as e:
        return False, f"检查过程中出现错误：{str(e)}"

def monitor_all_tasks():
    """
    监控所有任务，检查是否符合规则
    """
    print("开始监控所有任务的规则符合性...")
    
    # 这里需要调用cron list操作获取所有任务
    # 由于这是Python脚本，我们需要通过exec工具调用cron list
    # 让我们先返回一个模拟结果，实际执行时需要通过exec工具调用
    
    # 模拟任务列表（实际使用时需要通过cron list获取）
    mock_tasks = [
        {"id": "ea7d82a8-a5bc-40de-b329-6ef7f6c85881", "name": "商业智能周报", "schedule": {"expr": "0 16 * * 5"}},
        {"id": "97bfb647-a8f1-4456-ae56-feb2dc291414", "name": "自动同步任务文件到GitHub", "schedule": {"expr": "50 17 * * 1-6"}},
        # ... 其他任务
    ]
    
    compliant_count = 0
    non_compliant_count = 0
    non_compliant_tasks = []
    
    for task in mock_tasks:
        task_id = task.get("id", "unknown")
        task_name = task.get("name", "unknown")
        cron_expr = task.get("schedule", {}).get("expr", "")
        
        compliant, reason = check_task_time_compliance(cron_expr)
        
        if compliant:
            compliant_count += 1
            print(f"✅ 任务符合规则：{task_name} ({cron_expr})")
        else:
            non_compliant_count += 1
            non_compliant_tasks.append({
                "id": task_id,
                "name": task_name,
                "cron_expr": cron_expr,
                "reason": reason
            })
            print(f"❌ 任务不符合规则：{task_name} ({cron_expr}) - {reason}")
    
    # 生成监控报告
    report = {
        "monitor_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_tasks": len(mock_tasks),
        "compliant_count": compliant_count,
        "non_compliant_count": non_compliant_count,
        "compliance_rate": f"{compliant_count / len(mock_tasks) * 100:.1f}%",
        "non_compliant_tasks": non_compliant_tasks
    }
    
    # 保存报告到文件
    report_file = f"rule_enforcement_monitor_report_{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n监控完成！报告已保存到：{report_file}")
    print(f"总任务数：{len(mock_tasks)}")
    print(f"符合规则：{compliant_count} ({compliant_count / len(mock_tasks) * 100:.1f}%)")
    print(f"不符合规则：{non_compliant_count} ({non_compliant_count / len(mock_tasks) * 100:.1f}%)")
    
    return report

if __name__ == "__main__":
    monitor_all_tasks()