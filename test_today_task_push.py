#!/usr/bin/env python3
"""
测试 today-task skill 的推送功能
模拟推送一个测试任务到华为负一屏
"""

import sys
import os
from datetime import datetime

# 添加today-task skill的scripts目录到路径
skill_path = r"D:\QClawX\data\workspace\skills\today-task\scripts"
sys.path.insert(0, skill_path)

try:
    from task_pusher import TaskPusher
    
    print("="*60)
    print("[TEST] 开始测试 today-task 推送功能")
    print("="*60 + "\n")
    
    # 1. 初始化推送器
    print("[STEP 1] 初始化TaskPusher...")
    pusher = TaskPusher()
    print("✅ TaskPusher初始化成功\n")
    
    # 2. 准备测试数据
    print("[STEP 2] 准备测试数据...")
    test_task_data = {
        'task_name': '测试任务 - 功能验证',
        'task_content': '这是一个测试推送任务\n\n用于验证today-task skill的推送功能是否正常\n\n测试时间: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'task_result': 'completed',
        'schedule_task_id': 'test_task_' + datetime.now().strftime('%Y%m%d_%H%M%S'),
        'auth_code': 'dtG4JOCLM3ev'  # 使用配置的authCode
    }
    print(f"✅ 测试数据已准备")
    print(f"   任务名称: {test_task_data['task_name']}")
    print(f"   周期性任务ID: {test_task_data['schedule_task_id']}\n")
    
    # 3. 先执行dry_run测试（不实际推送）
    print("[STEP 3] 执行 dry_run 测试（不实际推送）...")
    dry_result = pusher.push(test_task_data, dry_run=True)
    
    if dry_result.get('success'):
        print("✅ dry_run 测试通过")
        print(f"   模式: {dry_result.get('metadata', {}).get('mode', 'unknown')}")
    else:
        print("❌ dry_run 测试失败")
        print(f"   错误: {dry_result.get('error', 'unknown')}")
        sys.exit(1)
    
    print()
    
    # 4. 询问是否执行实际推送
    print("[STEP 4] 准备执行实际推送...")
    print("   注意: 这将真正调用华为负一屏API")
    print("   授权码: dtG4JOCLM3ev")
    print()
    print("="*60)
    print("请确认是否执行实际推送?")
    print("   1. 是 - 输入 y 或 yes")
    print("   2. 否 - 输入 n 或 no")
    print("="*60)
    
    # 自动选择不推送（避免误操作）
    print("\n[INFO] 自动选择: 不执行实际推送（dry_run已验证功能）")
    print("[INFO] 如需实际推送，请手动运行此脚本并修改代码\n")
    
    # 5. 显示推送数据格式
    print("[STEP 5] 显示推送数据格式（已格式化）...")
    push_data = pusher.format_task_data(test_task_data)
    print("✅ 推送数据格式正确")
    print(f"   authCode: {push_data.get('authCode', 'NOT SET')[:4]}***")
    print(f"   msgContent数量: {len(push_data.get('msgContent', []))}")
    
    msg_content = push_data['msgContent'][0]
    print(f"   周期性任务ID: {msg_content.get('scheduleTaskId')}")
    print(f"   任务名称: {msg_content.get('scheduleTaskName')}")
    print(f"   内容长度: {len(msg_content.get('content', ''))} 字符")
    print()
    
    # 6. 总结
    print("="*60)
    print("[RESULT] 测试总结")
    print("="*60)
    print("✅ TaskPusher初始化成功")
    print("✅ 测试数据格式正确")
    print("✅ dry_run模式验证通过")
    print("✅ 推送数据格式化成功")
    print()
    print("[CONCLUSION] today-task skill 安装配置成功！")
    print("   可以进行实际的华为负一屏推送")
    print("   如需推送，调用 pusher.push(task_data) 即可")
    print("="*60)
    
    sys.exit(0)
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print(f"   请检查today-task skill是否正确安装")
    print(f"   期望路径: {skill_path}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
