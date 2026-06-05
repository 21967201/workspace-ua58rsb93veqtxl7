#!/usr/bin/env python3
"""
监控优化后任务执行情况
监控17个已优化时间的任务是否按新时间正确执行
"""

import json
import subprocess
import sys
from datetime import datetime, timezone

def get_all_tasks():
    """获取所有任务（包括enabled和disabled）"""
    try:
        result = subprocess.run(
            ["cron", "list", "includeDisabled=true"],
            capture_output=True,
            text=True,
            check=True
        )
        tasks_json = result.stdout
        tasks_data = json.loads(tasks_json)
        return tasks_data.get("jobs", [])
    except Exception as e:
        print(f"获取任务列表失败: {e}")
        return []

def check_task_execution_status(task):
    """检查任务执行状态"""
    task_id = task.get("id", "unknown")
    task_name = task.get("name", "unknown")
    
    state = task.get("state", {})
    last_run_at_ms = state.get("lastRunAtMs")
    last_run_status = state.get("lastRunStatus")
    consecutive_errors = state.get("consecutiveErrors", 0)
    
    # 检查最后执行时间是否在合理范围内（过去24小时内）
    execution_time_ok = False
    if last_run_at_ms:
        last_run_time = datetime.fromtimestamp(last_run_at_ms / 1000, tz=timezone.utc)
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
        "task_id": task_id,
        "task_name": task_name,
        "last_run_at_ms": last_run_at_ms,
        "last_run_status": last_run_status,
        "consecutive_errors": consecutive_errors,
        "execution_time_ok": execution_time_ok,
        "execution_status_ok": execution_status_ok,
        "no_consecutive_errors": no_consecutive_errors,
        "overall_ok": execution_time_ok and execution_status_ok and no_consecutive_errors
    }

def check_task_time_conflicts(all_tasks):
    """检查任务时间冲突"""
    # 解析所有任务的执行时间
    task_times = []
    
    for task in all_tasks:
        schedule = task.get("schedule", {})
        cron_expr = schedule.get("expr", "")
        
        if not cron_expr:
            continue
            
        # 简单解析Cron表达式（只检查分钟和小时）
        parts = cron_expr.split()
        if len(parts) >= 2:
            minute = parts[0]
            hour = parts[1]
            
            # 转换为分钟数（从00:00开始）
            try:
                time_minutes = int(hour) * 60 + int(minute)
                task_times.append({
                    "task_id": task.get("id"),
                    "task_name": task.get("name"),
                    "time_minutes": time_minutes,
                    "cron_expr": cron_expr
                })
            except ValueError:
                continue
    
    # 检查是否有任务在同一分钟执行
    conflicts = []
    time_groups = {}
    
    for task_time in task_times:
        time_minutes = task_time["time_minutes"]
        if time_minutes not in time_groups:
            time_groups[time_minutes] = []
        time_groups[time_minutes].append(task_time)
    
    for time_minutes, tasks_at_time in time_groups.items():
        if len(tasks_at_time) > 1:
            conflict = {
                "time_minutes": time_minutes,
                "time_str": f"{time_minutes // 60:02d}:{time_minutes % 60:02d}",
                "conflicting_tasks": [t["task_name"] for t in tasks_at_time]
            }
            conflicts.append(conflict)
    
    return conflicts

def check_task_delivery_status(task):
    """检查任务delivery状态"""
    task_id = task.get("id", "unknown")
    task_name = task.get("name", "unknown")
    
    state = task.get("state", {})
    last_delivered = state.get("lastDelivered")
    last_delivery_status = state.get("lastDeliveryStatus")
    
    # 检查delivery配置
    delivery = task.get("delivery", {})
    delivery_mode = delivery.get("mode")
    delivery_channel = delivery.get("channel")
    delivery_to = delivery.get("to")
    
    # 检查delivery配置是否正确
    delivery_config_ok = (
        delivery_mode == "announce" and
        delivery_channel == "wechat-access" and
        delivery_to == "last"
    )
    
    # 检查最后推送是否成功
    delivery_status_ok = (
        last_delivered is True and
        last_delivery_status in ["delivered", "not-requested"]
    )
    
    return {
        "task_id": task_id,
        "task_name": task_name,
        "delivery_mode": delivery_mode,
        "delivery_channel": delivery_channel,
        "delivery_to": delivery_to,
        "last_delivered": last_delivered,
        "last_delivery_status": last_delivery_status,
        "delivery_config_ok": delivery_config_ok,
        "delivery_status_ok": delivery_status_ok,
        "overall_ok": delivery_config_ok and delivery_status_ok
    }

def main():
    print("开始监控优化后任务执行情况...")
    
    # 步骤1：获取所有任务
    all_tasks = get_all_tasks()
    print(f"获取到 {len(all_tasks)} 个任务")
    
    if not all_tasks:
        print("没有任务需要监控")
        return
    
    # 步骤2：检查每个任务的执行状态
    print("\n=== 任务执行状态检查 ===")
    execution_results = []
    for task in all_tasks:
        result = check_task_execution_status(task)
        execution_results.append(result)
        
        status_icon = "✅" if result["overall_ok"] else "❌"
        print(f"{status_icon} {result['task_name']}: 执行状态={'正常' if result['overall_ok'] else '异常'}")
    
    # 步骤3：检查任务时间冲突
    print("\n=== 任务时间冲突检查 ===")
    conflicts = check_task_time_conflicts(all_tasks)
    
    if conflicts:
        print(f"发现 {len(conflicts)} 个时间冲突:")
        for conflict in conflicts:
            print(f"  - 时间 {conflict['time_str']}: {', '.join(conflict['conflicting_tasks'])}")
    else:
        print("✅ 没有发现时间冲突")
    
    # 步骤4：检查任务delivery状态
    print("\n=== 任务Delivery状态检查 ===")
    delivery_results = []
    for task in all_tasks:
        result = check_task_delivery_status(task)
        delivery_results.append(result)
        
        status_icon = "✅" if result["overall_ok"] else "❌"
        print(f"{status_icon} {result['task_name']}: Delivery状态={'正常' if result['overall_ok'] else '异常'}")
    
    # 步骤5：生成监控报告
    print("\n=== 生成监控报告 ===")
    
    # 统计
    total_tasks = len(all_tasks)
    execution_ok_count = sum(1 for r in execution_results if r["overall_ok"])
    delivery_ok_count = sum(1 for r in delivery_results if r["overall_ok"])
    conflicts_count = len(conflicts)
    
    # 创建报告
    report = {
        "monitor_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_tasks": total_tasks,
        "execution_status": {
            "ok_count": execution_ok_count,
            "error_count": total_tasks - execution_ok_count,
            "ok_rate": f"{execution_ok_count / total_tasks * 100:.1f}%"
        },
        "delivery_status": {
            "ok_count": delivery_ok_count,
            "error_count": total_tasks - delivery_ok_count,
            "ok_rate": f"{delivery_ok_count / total_tasks * 100:.1f}%"
        },
        "time_conflicts": {
            "has_conflicts": conflicts_count > 0,
            "conflicts_count": conflicts_count,
            "conflicts_details": conflicts
        },
        "details": {
            "execution_results": execution_results,
            "delivery_results": delivery_results
        }
    }
    
    # 保存报告
    report_file = f"monitoring_report_optimized_tasks_{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 监控报告已保存: {report_file}")
    print(f"   任务执行正常率: {execution_ok_count}/{total_tasks} ({execution_ok_count / total_tasks * 100:.1f}%)")
    print(f"   Delivery正常率: {delivery_ok_count}/{total_tasks} ({delivery_ok_count / total_tasks * 100:.1f}%)")
    print(f"   时间冲突: {'有' if conflicts_count > 0 else '无'} ({conflicts_count}个)")
    
    # 步骤6：如果有问题，推送告警
    if execution_ok_count < total_tasks or delivery_ok_count < total_tasks or conflicts_count > 0:
        print("\n=== 推送告警 ===")
        
        alert_content = "监控发现以下问题：\n"
        
        if execution_ok_count < total_tasks:
            alert_content += f"- 任务执行异常: {total_tasks - execution_ok_count}个任务\n"
            
        if delivery_ok_count < total_tasks:
            alert_content += f"- 任务Delivery异常: {total_tasks - delivery_ok_count}个任务\n"
            
        if conflicts_count > 0:
            alert_content += f"- 任务时间冲突: {conflicts_count}个冲突\n"
        
        print(f"告警内容: {alert_content}")
        
        # 这里可以调用推送逻辑
        # 例如：调用today-task技能推送告警
        print("告警推送功能待实现...")
    else:
        print("\n✅ 所有任务运行正常，无需推送告警")

if __name__ == "__main__":
    main()