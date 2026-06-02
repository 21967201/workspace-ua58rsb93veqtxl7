#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QClaw 原生知识库 - 每周整理脚本
功能: 从 memory/ 提取重要知识到 kb/ 结构化目录
"""

import os
import re
from datetime import datetime, timedelta

# 配置
WORKSPACE_ROOT = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
DAYS_BACK = 7

def main():
    # 设置控制台输出编码为 UTF-8
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("[每周知识整理]")
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_BACK)
    
    print(f"   时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
    print()
    
    # 统计
    stats = {
        "people": 0,
        "projects": 0,
        "tech": 0,
        "decisions": 0,
        "ai_breakthrough": 0
    }
    
    # 步骤1: 扫描 memory/ 目录
    print("[步骤1] 步骤1: 扫描 memory/ 目录...")
    memory_dir = os.path.join(WORKSPACE_ROOT, "memory")
    
    memory_files = []
    for root, dirs, files in os.walk(memory_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if start_date <= mtime <= end_date:
                    memory_files.append(file_path)
    
    print(f"   找到 {len(memory_files)} 个文件")
    print()
    
    # 步骤2: 提取重要知识
    print("[步骤2] 步骤2: 提取重要知识...")
    
    for file_path in memory_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检测人物信息
        if re.search(r"(人物|人员|同事|朋友)", content):
            print(f"   [人物] 在 {os.path.basename(file_path)} 中发现人物信息")
            stats["people"] += 1
        
        # 检测项目信息
        if re.search(r"(项目|任务|工作)", content):
            print(f"   [项目] 在 {os.path.basename(file_path)} 中发现项目信息")
            stats["projects"] += 1
        
        # 检测技术信息
        if re.search(r"(技术|工具|框架|语言)", content):
            print(f"   [技术] 在 {os.path.basename(file_path)} 中发现技术信息")
            stats["tech"] += 1
        
        # 检测决策信息
        if re.search(r"(决策|决定|选择|方案)", content):
            print(f"   [决策] 在 {os.path.basename(file_path)} 中发现决策信息")
            stats["decisions"] += 1
        
        # 检测AI技术突破
        if re.search(r"AI.*(技术|突破|进展|模型)", content):
            print(f"   [AI突破] 在 {os.path.basename(file_path)} 中发现AI技术突破信息")
            stats["ai_breakthrough"] += 1
    
    print()
    
    # 步骤3: 生成整理报告
    print("[步骤3] 步骤3: 生成整理报告...")
    
    report_date = end_date.strftime("%Y-%m-%d")
    report_path = os.path.join(WORKSPACE_ROOT, "kb", f"weekly_organize_report_{report_date}.md")
    
    report_content = f"# 每周知识整理报告 - {report_date}\n\n"
    report_content += "## [每周知识整理] 时间范围\n\n"
    report_content += f"- 开始: {start_date.strftime('%Y-%m-%d')}\n"
    report_content += f"- 结束: {end_date.strftime('%Y-%m-%d')}\n\n"
    
    report_content += "## [步骤3] 统计摘要\n\n"
    report_content += "| 类别 | 发现数量 |\n"
    report_content += "|------|----------|\n"
    report_content += f"| 人物 | {stats['people']} |\n"
    report_content += f"| 项目 | {stats['projects']} |\n"
    report_content += f"| 技术 | {stats['tech']} |\n"
    report_content += f"| 决策 | {stats['decisions']} |\n"
    report_content += f"| AI突破 | {stats['ai_breakthrough']} |\n\n"
    
    report_content += "## [步骤2] 建议操作\n\n"
    report_content += "1. **创建知识条目**: 将重要信息从 memory/ 迁移到 kb/\n"
    report_content += "2. **更新 MEMORY.md**: 添加知识库索引\n"
    report_content += "3. **清理临时内容**: 归档 memory/ 中的临时文件\n\n"
    
    report_content += "## 🔗 相关文件\n\n"
    for file_path in memory_files:
        rel_path = os.path.relpath(file_path, WORKSPACE_ROOT)
        report_content += f"- .\\{rel_path}\n"
    
    # 保存报告
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"   [完成] 报告已保存: {report_path}")
    print()
    
    # 步骤4: 自动创建知识条目 (示例)
    print("[步骤4] 步骤4: 自动创建知识条目 (示例)...")
    
    if stats["ai_breakthrough"] > 0:
        ai_file_path = os.path.join(WORKSPACE_ROOT, "kb", "ai-breakthrough", f"{report_date}.md")
        
        if not os.path.exists(ai_file_path):
            ai_content = f"# AI技术突破 - {report_date}\n\n"
            ai_content += "## 本周发现\n\n"
            ai_content += "- 待补充: 从 memory/ 中提取具体内容\n\n"
            
            with open(ai_file_path, "w", encoding="utf-8") as f:
                f.write(ai_content)
            
            print(f"   [完成] 已创建: {ai_file_path}")
    
    print()
    
    # 完成
    print("[完成] 每周整理完成!")
    print()
    print("[步骤3] 统计:")
    print(f"   人物: {stats['people']} 条")
    print(f"   项目: {stats['projects']} 条")
    print(f"   技术: {stats['tech']} 条")
    print(f"   决策: {stats['decisions']} 条")
    print(f"   AI突破: {stats['ai_breakthrough']} 条")
    print()
    print(f"[报告] 报告: {report_path}")
    print()
    print("[下一步] 下一步:")
    print("   1. 查看报告")
    print("   2. 迁移知识: 将 memory/ 重要信息复制到 kb/")
    print("   3. 手动更新: 编辑 kb/ 中的具体文件")

if __name__ == "__main__":
    main()
