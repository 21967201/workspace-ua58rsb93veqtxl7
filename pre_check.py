#!/usr/bin/env python3
"""
每周错误预防检查脚本
模拟检查工作区文件的合规性
"""

import os
import json
from datetime import datetime

def check_workspace_compliance():
    """检查工作区文件的合规性"""
    workspace = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
    
    # 定义检查规则
    compliance_rules = {
        "required_files": ["AGENTS.md", "SOUL.md", "USER.md", "IDENTITY.md", "TOOLS.md"],
        "max_file_size_kb": 100,  # 最大文件大小100KB
        "allowed_extensions": [".md", ".py", ".txt", ".json"]
    }
    
    results = {
        "compliant": 0,
        "non_compliant": 0,
        "violations": [],
        "details": []
    }
    
    # 检查必需文件
    for required_file in compliance_rules["required_files"]:
        file_path = os.path.join(workspace, required_file)
        if os.path.exists(file_path):
            results["compliant"] += 1
            results["details"].append(f"[OK] {required_file} 存在")
        else:
            results["non_compliant"] += 1
            results["violations"].append(f"缺少必需文件: {required_file}")
            results["details"].append(f"[MISSING] {required_file} 不存在")
    
    # 检查所有文件
    for root, dirs, files in os.walk(workspace):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            # 检查文件扩展名
            if file_ext not in compliance_rules["allowed_extensions"]:
                results["non_compliant"] += 1
                results["violations"].append(f"不允许的文件类型: {file}")
                continue
            
            # 检查文件大小
            try:
                file_size_kb = os.path.getsize(file_path) / 1024
                if file_size_kb > compliance_rules["max_file_size_kb"]:
                    results["non_compliant"] += 1
                    results["violations"].append(f"文件过大: {file} ({file_size_kb:.1f}KB)")
            except:
                pass
    
    # 添加时间戳
    results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results["total"] = results["compliant"] + results["non_compliant"]
    
    return results

def main():
    """主函数"""
    print("开始执行每周错误预防检查...")
    results = check_workspace_compliance()
    
    print(f"\n检查结果 @ {results['timestamp']}")
    print("=" * 50)
    print(f"合规文件数: {results['compliant']}")
    print(f"违规文件数: {results['non_compliant']}")
    print(f"违规项数: {len(results['violations'])}")
    print(f"总文件数: {results['total']}")
    
    if results['violations']:
        print("\n违规项详情:")
        for i, violation in enumerate(results['violations'], 1):
            print(f"  {i}. {violation}")
    
    print("\n详细检查结果:")
    for detail in results['details']:
        # 移除可能的问题字符
        safe_detail = detail.replace('✓', '[OK]').replace('✗', '[X]')
        print(f"  {safe_detail}")
    
    # 返回结果供外部使用
    return results

if __name__ == "__main__":
    results = main()
    # 将结果输出为JSON格式，方便后续处理
    import sys
    print("\nJSON输出:")
    print(json.dumps(results, ensure_ascii=False, indent=2))