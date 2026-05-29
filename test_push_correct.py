#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""正确的推送测试 - 按照 hiboards_client.py 的标准格式"""

import sys
import os
import json
import requests
from datetime import datetime

# 读取 QClaw 全局配置
user_home = os.path.expanduser("~")
config_path = os.path.join(user_home, ".qclaw", "openclaw.json")

with open(config_path, 'r', encoding='utf-8') as f:
    qclaw_config = json.load(f)

skill_config = qclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
config = skill_config.get('config', {})

auth_code = config.get('authCode')
push_url = config.get('pushServiceUrl')

print("=" * 60)
print("配置读取：")
print(f"  authCode: {auth_code[:8]}..." if auth_code and len(auth_code) > 8 else f"  authCode: {auth_code}")
print(f"  pushServiceUrl: {push_url}")
print("=" * 60)

if not auth_code or not push_url:
    print("[FAIL] 配置不完整，退出")
    sys.exit(1)

# 读取任务 JSON 文件
json_file = r"D:\QClawX\data\workspace\skills\today-task\scripts\智能分析与记忆管理【测试】_20260529_174206.json"
with open(json_file, 'r', encoding='utf-8') as f:
    task_data = json.load(f)

print(f"\n任务 JSON 读取成功：")
print(f"  task_name: {task_data.get('task_name')}")
print(f"  task_content 长度: {len(task_data.get('task_content', ''))} 字符")
print(f"  task_result: {task_data.get('task_result')}")

# 构造推送数据（严格按照 hiboards_client.py 格式）
push_data = {
    "authCode": auth_code,
    "msgContent": [
        {
            "msgId": f"task-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "scheduleTaskId": f"sched-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "summary": task_data.get("task_name", "测试任务")[:100],
            "result": task_data.get("task_result", "任务已完成"),
            "content": task_data.get("task_content", ""),
            "source": "QClaw-today-task"
        }
    ]
}

# 按照 hiboards_client.py，数据要包一层 data
wrapped_data = {"data": push_data}

# 生成 x-trace-id（必须！）
trace_id = f"task-push-{datetime.now().strftime('%Y%m%d%H%M%S')}"
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "QClaw-TaskPusher/2.0",
    "x-trace-id": trace_id
}

print(f"\n推送数据构造完成：")
print(f"  push_url: {push_url}")
print(f"  x-trace-id: {trace_id}")
print(f"  msgContent 条目数: {len(push_data['msgContent'])}")

# 执行推送
print(f"\n正在推送...")
try:
    response = requests.post(
        push_url,
        json=wrapped_data,   # 用 json= 自动序列化 + 设置 Content-Type
        headers=headers,
        timeout=30
    )
    print(f"  HTTP 状态码: {response.status_code}")
    print(f"  响应内容: {response.text[:500]}")
    
    # 检查业务状态码
    if response.status_code == 200:
        result = response.json()
        code = result.get('code')
        desc = result.get('desc', '')
        message = result.get('message', '')
        
        print(f"\n  业务响应: code={code}, desc={desc}, message={message}")
        
        # 成功状态码
        if str(code) in ['0000000000', '0', '000000000', '0000500000']:
            print("\n[SUCCESS] 推送成功！请检查负一屏是否收到消息")
        else:
            print(f"\n[FAIL] 业务失败: code={code}, desc={desc}")
    else:
        print(f"\n[FAIL] HTTP 失败: {response.status_code}")
        
except Exception as e:
    print(f"\n[FAIL] 推送异常: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
