#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最简推送测试 - 直接推送，绕过损坏的 task_push.py"""

import sys
import os
import json
import requests

# 读取配置
user_home = os.path.expanduser("~")
config_path = os.path.join(user_home, ".qclaw", "openclaw.json")

with open(config_path, 'r', encoding='utf-8') as f:
    qclaw_config = json.load(f)

skill_config = qclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
config = skill_config.get('config', {})

auth_code = config.get('authCode')
push_url = config.get('pushServiceUrl')

print("=" * 60)
print("配置读取结果：")
print(f"  authCode: {auth_code[:6]}..." if auth_code and len(auth_code) > 6 else f"  authCode: {auth_code}")
print(f"  pushServiceUrl: {push_url}")
print("=" * 60)

if not auth_code or not push_url:
    print("[FAIL] 配置不完整，退出")
    sys.exit(1)

# 读取刚才生成的任务 JSON 文件
json_file = r"D:\QClawX\data\workspace\skills\today-task\scripts\智能分析与记忆管理【测试】_20260529_174206.json"
if not os.path.exists(json_file):
    print(f"[FAIL] JSON 文件不存在: {json_file}")
    sys.exit(1)

with open(json_file, 'r', encoding='utf-8') as f:
    task_data = json.load(f)

print(f"\n任务 JSON 读取成功：")
print(f"  task_name: {task_data.get('task_name')}")
print(f"  task_content 长度: {len(task_data.get('task_content', ''))} 字符")
print(f"  task_result: {task_data.get('task_result')}")

# 构造推送数据（参考 hiboards_client.py 的格式）
push_data = {
    "authCode": auth_code,
    "msgContent": [
        {
            "title": task_data.get("task_name", "测试任务"),
            "content": task_data.get("task_content", ""),
            "result": task_data.get("task_result", "任务已完成"),
            "timestamp": task_data.get("timestamp", "")
        }
    ]
}

print(f"\n推送数据构造完成")
print(f"  push_url: {push_url}")
print(f"  msgContent 条目数: {len(push_data['msgContent'])}")

# 执行推送
print(f"\n正在推送...")
try:
    response = requests.post(
        push_url,
        json=push_data,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    print(f"  HTTP 状态码: {response.status_code}")
    print(f"  响应内容: {response.text[:500]}")
    
    if response.status_code == 200:
        print("\n[SUCCESS] 推送成功！请检查负一屏是否收到消息")
    else:
        print(f"\n[FAIL] 推送失败，HTTP {response.status_code}")
except Exception as e:
    print(f"\n[FAIL] 推送异常: {e}")

print("=" * 60)
