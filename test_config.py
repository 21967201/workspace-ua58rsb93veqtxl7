#!/usr/bin/env python3
"""测试 today-task 配置加载"""

import sys
import os

# 添加技能路径
sys.path.insert(0, r'D:\QClawX\data\workspace\skills\today-task')

print("=" * 60)
print("测试1: 直接读取 QClaw 全局配置")
print("=" * 60)

# 直接读取全局配置
user_home = os.path.expanduser("~")
config_path = os.path.join(user_home, ".qclaw", "openclaw.json")

print(f"配置文件路径: {config_path}")
print(f"文件存在: {os.path.exists(config_path)}")

if os.path.exists(config_path):
    import json
    with open(config_path, 'r', encoding='utf-8') as f:
        qclaw_config = json.load(f)
    
    print(f"配置加载成功")
    
    # 获取 today-task 配置
    skill_config = qclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
    print(f"\ntoday-task 技能配置: {skill_config}")
    
    config_value = skill_config.get('config', {})
    print(f"\nconfig 字段内容: {config_value}")
    
    auth_code = config_value.get('authCode')
    push_url = config_value.get('pushServiceUrl')
    
    print(f"\nauthCode: {auth_code}")
    print(f"pushServiceUrl: {push_url}")
    
    if auth_code:
        print("\n✅ authCode 读取成功!")
    else:
        print("\n❌ authCode 读取失败!")
    
    if push_url:
        print("✅ pushServiceUrl 读取成功!")
    else:
        print("❌ pushServiceUrl 读取失败!")

print("\n" + "=" * 60)
print("测试2: 通过 Config 类读取")
print("=" * 60)

try:
    from scripts.config import Config
    c = Config()
    print(f"Config 对象创建成功")
    print(f"config 字典内容: {c.config}")
    
    auth_code = c.config.get('auth_code') or c.config.get('authCode')
    hiboard_url = c.config.get('hiboard_url') or c.config.get('pushServiceUrl')
    
    print(f"\nauth_code/authCode: {auth_code}")
    print(f"hiboard_url/pushServiceUrl: {hiboard_url}")
    
    if auth_code and hiboard_url:
        print("\n✅ 配置全部读取成功!")
    else:
        print("\n❌ 配置读取不完整!")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试3: 测试推送功能")
print("=" * 60)

# 测试创建任务 JSON
try:
    print("\n3.1 测试 create_task_json.py...")
    # 先创建一个测试内容文件
    test_content_path = r'D:\QClawX\data\workspace-ua58rsb93veqtxl7\test_content.txt'
    with open(test_content_path, 'w', encoding='utf-8') as f:
        f.write("这是一个测试任务内容\n时间: 2026-05-29 17:30")
    
    print(f"测试内容文件已创建: {test_content_path}")
    
    # 调用 create_task_json.py
    import subprocess
    result = subprocess.run(
        ['python', r'D:\QClawX\data\workspace\skills\today-task\scripts\create_task_json.py',
         '测试任务', test_content_path],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    print(f"stdout: {result.stdout}")
    print(f"stderr: {result.stderr}")
    print(f"returncode: {result.returncode}")
    
    if result.returncode == 0:
        print("✅ create_task_json.py 执行成功!")
    else:
        print("❌ create_task_json.py 执行失败!")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("完成")
print("=" * 60)
