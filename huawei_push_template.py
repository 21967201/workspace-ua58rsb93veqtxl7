#!/usr/bin/env python3
"""
华为负一屏推送模板
需要完整的authCode才能使用
"""

import requests
import json
from datetime import datetime

def push_to_huawei(auth_code, title, content):
    """
    推送消息到华为负一屏
    
    Args:
        auth_code: 完整的授权码
        title: 推送标题
        content: 推送内容
    
    Returns:
        推送结果
    """
    # 华为负一屏API端点（示例，实际需要确认正确的API）
    url = "https://api.huawei.com/negative-screen/push"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_code}"
    }
    
    payload = {
        "title": title,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "priority": "normal"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {"success": True, "response": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_check_result(result):
    """格式化检查结果为推送内容"""
    content = f"""每周错误预防检查结果 @ {result['timestamp']}
    
合规: {result['compliant']}/{result['total']} 文件
违规: {len(result['violations'])} 项

主要违规类型:
"""
    for i, violation in enumerate(result['violations'][:5], 1):  # 只显示前5项
        content += f"{i}. {violation}\n"
    
    if len(result['violations']) > 5:
        content += f"... 还有 {len(result['violations']) - 5} 项违规"
    
    return content

if __name__ == "__main__":
    # 示例用法
    print("华为负一屏推送模板")
    print("需要提供完整的authCode才能使用")
    
    # 示例数据
    sample_result = {
        "timestamp": "2026-05-28 09:42:21",
        "compliant": 5,
        "non_compliant": 20,
        "violations": ["缺少必需文件: config", "文件过大: example.txt"],
        "total": 25
    }
    
    content = format_check_result(sample_result)
    print("\n推送内容预览:")
    print(content)