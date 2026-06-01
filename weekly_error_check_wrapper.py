#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Error Prevention Check - 统一执行脚本
避免隔离会话执行复杂性，所有逻辑在此脚本中完成
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def run_pre_check():
    """运行 pre_check.py 并返回结果"""
    try:
        result = subprocess.run(
            [sys.executable, "pre_check.py"],
            cwd=r"D:\QClawX\data\workspace-ua58rsb93veqtxl7",
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        
        if result.returncode != 0:
            return None, f"脚本执行失败: {result.stderr}"
        
        # 解析 JSON 输出
        output_lines = result.stdout.strip().split('\n')
        json_start = -1
        for i, line in enumerate(output_lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start == -1:
            return None, "未找到JSON输出"
        
        json_str = '\n'.join(output_lines[json_start:])
        data = json.loads(json_str)
        return data, None
        
    except Exception as e:
        return None, str(e)

def write_to_memory_md(results):
    """记录结果到 MEMORY.md"""
    try:
        memory_path = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7\MEMORY.md"
        
        # 读取现有内容
        content = ""
        if os.path.exists(memory_path):
            with open(memory_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        
        # 创建今日记录
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_entry = f"\n\n[**{today}] 每周错误预防检查 - {results['compliant']}/{results['total']} 合规，{len(results['violations'])} 项违规**\n"
        new_entry += f"- 合规文件: {results['compliant']}个\n"
        new_entry += f"- 违规文件: {results['non_compliant']}个\n"
        new_entry += f"- 违规项数: {len(results['violations'])}项\n"
        
        if results['violations']:
            new_entry += "- 主要违规类型: " + ", ".join(results['violations'][:5]) + "...\n"
        
        # 写入文件
        with open(memory_path, 'a', encoding='utf-8-sig') as f:
            f.write(new_entry)
        
        return True, "已记录到MEMORY.md"
        
    except Exception as e:
        return False, str(e)

def push_to_huawei(results):
    """推送结果到华为负一屏"""
    try:
        # 创建任务JSON
        create_cmd = [
            sys.executable,
            r"D:\QClawX\data\workspace\skills\today-task\scripts\create_task_json.py",
            "Weekly Error Prevention Check",
            json.dumps(results, ensure_ascii=False, indent=2)
        ]
        
        result1 = subprocess.run(create_cmd, capture_output=True, text=True, encoding='utf-8')
        
        # 推送
        today = datetime.now().strftime("%Y-%m-%d")
        push_cmd = [
            sys.executable,
            r"D:\QClawX\data\workspace\skills\today-task\scripts\task_push.py",
            "--data", f"Weekly_Error_Prevention_Check_{today}.json"
        ]
        
        result2 = subprocess.run(push_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if "success" in result2.stdout and '"success": true' in result2.stdout:
            return True, "推送成功"
        else:
            return False, f"推送失败: {result2.stdout}"
            
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("Weekly Error Prevention Check - 统一执行脚本")
    print("=" * 60)
    
    # 步骤1：运行检查
    print("\n[1/4] 运行 pre_check.py...")
    results, error = run_pre_check()
    
    if error:
        print(f"[错误] {error}")
        return
    
    print(f"[成功] 检查完成: {results['compliant']}/{results['total']} 合规, {len(results['violations'])} 项违规")
    
    # 步骤2：记录到MEMORY.md
    print("\n[2/4] 记录到MEMORY.md...")
    success, msg = write_to_memory_md(results)
    if success:
        print(f"[成功] {msg}")
    else:
        print(f"[错误] 记录失败: {msg}")
    
    # 步骤3：如有违规，推送
    if len(results['violations']) > 0:
        print("\n[3/4] 推送到华为负一屏...")
        success, msg = push_to_huawei(results)
        if success:
            print(f"[成功] {msg}")
        else:
            print(f"[错误] 推送失败: {msg}")
            # 重试一次
            print("\n[3b/4] 重试推送...")
            success, msg = push_to_huawei(results)
            if success:
                print(f"[成功] 重试成功: {msg}")
            else:
                print(f"[错误] 重试失败: {msg}")
    else:
        print("\n[3/4] 全部合规，无需推送")
    
    # 步骤4：生成摘要
    print("\n[4/4] 生成摘要...")
    summary = f"每周错误预防检查完成\n"
    summary += f"- 合规: {results['compliant']}/{results['total']}\n"
    summary += f"- 违规: {len(results['violations'])}项\n"
    
    if len(results['violations']) > 0:
        summary += f"\n主要违规: {results['violations'][0]}\n"
        summary += f"（完整列表见 MEMORY.md）"
    
    print("\n" + "=" * 60)
    print("执行完成！")
    print("=" * 60)
    print(f"\n{summary}")
    
    return summary

if __name__ == "__main__":
    try:
        summary = main()
        # 输出JSON格式结果供cron任务读取
        print("\nJSON输出:")
        print(json.dumps({"success": True, "summary": summary}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"\n[错误] 执行失败: {e}")
        print("\nJSON输出:")
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)
