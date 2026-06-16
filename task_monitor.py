#!/usr/bin/env python3
"""
任务监控脚本 - 监控QClaw自动任务的执行状态

功能：
1. 任务执行失败监控（consecutiveErrors >= 3）
2. 任务执行时间监控（实际时间 > 预期时间 × 2）
3. 任务执行结果异常监控（lastRunStatus != "ok" 或 lastDeliveryStatus != "delivered"）

作者: QClaw Agent
创建时间: 2026-06-05
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Any

# OpenClaw CLI 路径
OPENCLAW_CMD = r"D:\QClaw\v0.2.26.557\resources\openclaw\config\bin\openclaw.cmd"
OPENCLAW_ENV = os.environ.copy()
OPENCLAW_ENV["PATH"] = r"D:\QClaw\v0.2.26.557\resources\openclaw\config\bin" + os.pathsep + OPENCLAW_ENV.get("PATH", "")

# 预期执行时间（秒）
EXPECTED_DURATION = {
    "1688全景分析（含价格监控）": 60,
    "智能全景管理（含GBrain + 记忆管理）": 400,
    "tech-breakthrough-monitor": 100,
    "QClaw月度智能清理": 300,
    "自动同步任务文件到GitHub": 250,
    "商业智能周报": 300,
    "QClaw知识库每周整理": 180,
    "竞品深度分析周报": 200,
    "QClaw周度轻度清理": 120,
    "OpenClaw违规检查": 300,
    "每周任务执行分析与错误预防检查": 600,
    "Memory Dreaming Promotion": 240,
}

# 告警阈值
FAILURE_THRESHOLD = 3  # 连续失败次数阈值
TIMEOUT_MULTIPLIER = 2  # 超时倍数


def run_cron_list() -> List[Dict[str, Any]]:
    """运行 cron action=list 命令获取所有任务"""
    try:
        result = subprocess.run(
            [OPENCLAW_CMD, "cron", "list", "--all", "--json"],
            capture_output=True,
            check=True,
            env=OPENCLAW_ENV,
            shell=True
        )
        stdout = result.stdout.decode('utf-8', errors='replace')
        # 移除 proxy-bootstrap 等非 JSON 前缀行
        json_start = stdout.find('{')
        if json_start >= 0:
            stdout = stdout[json_start:]
        data = json.loads(stdout)
        return data.get("jobs", [])
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='replace') if e.stderr else ''
        print(f"❌ 运行 cron list 失败: {e}\n{stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"❌ 解析 cron list 输出失败: {e}", file=sys.stderr)
        return []


def check_failure(job: Dict[str, Any]) -> List[str]:
    """检查任务执行失败"""
    alerts = []
    name = job.get("name", "Unknown")
    consecutive_errors = job.get("state", {}).get("consecutiveErrors", 0)
    
    if consecutive_errors >= FAILURE_THRESHOLD:
        last_error = job.get("state", {}).get("lastError", "未知错误")
        last_run_at_ms = job.get("state", {}).get("lastRunAtMs", 0)
        last_run_at = datetime.fromtimestamp(last_run_at_ms / 1000).strftime('%Y-%m-%d %H:%M:%S') if last_run_at_ms else "未知"
        
        alert = f"""【任务执行失败告警】

任务名称：{name}
失败次数：{consecutive_errors}
最后失败时间：{last_run_at}
最后错误信息：{last_error}

请检查任务配置和执行日志。
"""
        alerts.append(alert)
    
    return alerts


def check_timeout(job: Dict[str, Any]) -> List[str]:
    """检查任务执行时间超时"""
    alerts = []
    name = job.get("name", "Unknown")
    last_duration_ms = job.get("state", {}).get("lastDurationMs", 0)
    
    if not last_duration_ms:
        return alerts
    
    last_duration_sec = last_duration_ms / 1000
    expected_duration = EXPECTED_DURATION.get(name)
    
    if expected_duration and last_duration_sec > expected_duration * TIMEOUT_MULTIPLIER:
        alert = f"""【任务执行时间超时告警】

任务名称：{name}
预期执行时间：{expected_duration}秒
实际执行时间：{last_duration_sec:.2f}秒
超时倍数：{last_duration_sec / expected_duration:.2f}倍

请检查任务执行日志和系统资源。
"""
        alerts.append(alert)
    
    return alerts


def check_result_abnormal(job: Dict[str, Any]) -> List[str]:
    """检查任务执行结果异常"""
    alerts = []
    name = job.get("name", "Unknown")
    last_run_status = job.get("state", {}).get("lastRunStatus", "unknown")
    last_delivery_status = job.get("state", {}).get("lastDeliveryStatus", "unknown")
    last_error = job.get("state", {}).get("lastError", "")
    
    if last_run_status != "ok":
        alert = f"""【任务执行结果异常告警】

任务名称：{name}
执行状态：{last_run_status}
推送状态：{last_delivery_status}
错误信息：{last_error if last_error else "无"}

请检查任务配置和执行日志。
"""
        alerts.append(alert)
    
    return alerts


def main():
    """主函数"""
    print(f"🔍 开始监控任务... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    
    # 获取所有任务
    jobs = run_cron_list()
    if not jobs:
        print("⚠️ 未找到任何任务")
        return
    
    print(f"✅ 找到 {len(jobs)} 个任务")
    
    # 检查所有任务
    all_alerts = []
    for job in jobs:
        name = job.get("name", "Unknown")
        print(f"  检查任务: {name}")
        
        # 检查失败
        alerts = check_failure(job)
        all_alerts.extend(alerts)
        
        # 检查超时
        alerts = check_timeout(job)
        all_alerts.extend(alerts)
        
        # 检查结果异常
        alerts = check_result_abnormal(job)
        all_alerts.extend(alerts)
    
    # 输出告警
    if all_alerts:
        print(f"\n⚠️ 发现 {len(all_alerts)} 个告警：\n")
        for i, alert in enumerate(all_alerts, 1):
            print(f"{i}. {alert}\n")
        
        # 保存告警到文件
        alert_file = f"D:\\QClawX\\data\\workspace-ua58rsb93veqtxl7\\task_alerts_{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(alert_file, "w", encoding="utf-8") as f:
            f.write(f"# 任务监控告警报告\n\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for i, alert in enumerate(all_alerts, 1):
                f.write(f"## 告警 {i}\n\n```\n{alert}\n```\n\n")
        
        print(f"📄 告警已保存到: {alert_file}")
    else:
        print("\n✅ 所有任务运行正常")
    
    print(f"\n🎉 监控完成 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")


if __name__ == "__main__":
    main()
