#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# 读取报告内容
with open('1688全景分析报告_2026-06-06.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 构造正确格式的任务数据
task_data = {
    'task_name': '1688全面分析（全景+竞品）',
    'task_result': '已完成店铺监控、店铺诊断、竞品分析、价格监控和全景分析',
    'task_content': content
}

# 保存为JSON文件
output_file = '1688全面分析（全景+竞品）_2026-06-06_fixed.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(task_data, f, ensure_ascii=False, indent=2)

print(f'[OK] 任务JSON文件已创建: {output_file}')
print(f'[INFO] 文件大小: {len(json.dumps(task_data, ensure_ascii=False))} 字节')
