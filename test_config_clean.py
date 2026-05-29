#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 today-task 配置加载和推送功能"""

import sys
import os
import json

# 添加技能路径
sys.path.insert(0, r'D:\QClawX\data\workspace\skills\today-task')

print("=" * 60)
print("测试1: 直接读取 QClaw 全局配置")
print("=" * 60)

# 直接读取全局配置
user_home = os.path.expanduser("~")
config_path = os.path.join(user_home, ".qclaw", "openclaw.json")

print("配置文件路径: " + config_path)
print("文件存在: " + str(os.path.exists(config_path)))

if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        qclaw_config = json.load(f)
    
    print("配置加载成功")
    
    # 获取 today-task 配置
    skill_config = qclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
    print("\ntoday-task 技能配置: " + str(skill_config))
    
    config_value = skill_config.get('config', {})
    print("\nconfig 字段内容: ")
    for k, v in config_value.items():
        if 'auth' in k.lower():
            print("  " + k + ": " + str(v[:4]) + "***" if len(str(v)) > 4 else "  " + k + ": " + str(v))
        else:
            print("  " + k + ": " + str(v))
    
    auth_code = config_value.get('authCode')
    push_url = config_value.get('pushServiceUrl')
    
    print("\nauthCode: " + str(auth_code))
    print("pushServiceUrl: " + str(push_url))
    
    if auth_code:
        print("\n[OK] authCode 读取成功!")
    else:
        print("\n[FAIL] authCode 读取失败!")
    
    if push_url:
        print("[OK] pushServiceUrl 读取成功!")
    else:
        print("[FAIL] pushServiceUrl 读取失败!")

print("\n" + "=" * 60)
print("测试2: 通过 Config 类读取")
print("=" * 60)

try:
    from scripts.config import Config
    c = Config()
    print("Config 对象创建成功")
    print("config 字典 keys: " + str(list(c.config.keys())))
    
    auth_code = c.config.get('auth_code') or c.config.get('authCode')
    hiboard_url = c.config.get('hiboard_url') or c.config.get('pushServiceUrl')
    
    print("\nauth_code/authCode: " + str(auth_code))
    print("hiboard_url/pushServiceUrl: " + str(hiboard_url))
    
    if auth_code and hiboard_url:
        print("\n[OK] 配置全部读取成功!")
    else:
        print("\n[FAIL] 配置读取不完整!")
        
except Exception as e:
    print("[FAIL] 错误: " + str(e))
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("完成")
print("=" * 60)
