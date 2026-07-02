#!/usr/bin/env python3
"""
Quick analysis of session files to understand structure
"""
import json
import os
from collections import Counter

SESSION_DIR = r"D:\QClawX\data\.qclaw\agents\main\sessions"

# 读取第一个 session 文件，了解结构
session_files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.jsonl')][:5]

print("=== Session File Structure Analysis ===\n")

for filename in session_files:
    filepath = os.path.join(SESSION_DIR, filename)
    print(f"\n分析文件: {filename}")
    print("-" * 50)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"  总行数: {len(lines)}")
            
            # 分析前3行
            for i, line in enumerate(lines[:3]):
                try:
                    data = json.loads(line.strip())
                    print(f"\n  第 {i+1} 行:")
                    print(f"    type: {data.get('type', 'N/A')}")
                    
                    # 检查是否有工具调用
                    if 'tool' in str(data):
                        print(f"    包含工具调用信息")
                        
                    # 检查是否有消息
                    if data.get('type') == 'message':
                        print(f"    role: {data.get('data', {}).get('role', 'N/A')}")
                        
                except json.JSONDecodeError as e:
                    print(f"  JSON 解析错误: {e}")
                    
    except Exception as e:
        print(f"  读取错误: {e}")

print("\n=== 工具调用提取测试 ===\n")

# 尝试提取工具调用
tool_calls = []
for filename in session_files[:3]:
    filepath = os.path.join(SESSION_DIR, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    
                    # 查找工具调用
                    if 'toolName' in str(data):
                        # 尝试不同的可能路径
                        tool_name = None
                        
                        if 'data' in data and 'toolName' in data['data']:
                            tool_name = data['data']['toolName']
                        elif 'toolName' in data:
                            tool_name = data['toolName']
                        elif 'name' in data:
                            tool_name = data['name']
                            
                        if tool_name:
                            tool_calls.append(tool_name)
                            
                except:
                    continue
                    
    except:
        continue

print(f"找到 {len(tool_calls)} 个工具调用")
if tool_calls:
    print("\n前10个工具调用:")
    for i, tool in enumerate(tool_calls[:10]):
        print(f"  {i+1}. {tool}")
    
    print(f"\n工具使用频率:")
    tool_counter = Counter(tool_calls)
    for tool, count in tool_counter.most_common(10):
        print(f"  {tool}: {count} 次")
