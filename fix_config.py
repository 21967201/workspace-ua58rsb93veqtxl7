#!/usr/bin/env python3
"""修复 today-task skill 的 config.py 文件"""

import os
import re

def fix_config_py():
    """修复 config.py 中的 _get_from_QClaw_global 方法"""
    
    # 文件路径
    config_py_path = r"D:\QClawX\data\workspace\skills\today-task\scripts\config.py"
    
    print(f"正在修复: {config_py_path}")
    
    # 读取文件
    with open(config_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录原始长度
    original_len = len(content)
    print(f"原始文件长度: {original_len} 字符")
    
    # 修复1: 替换错误的文件名 QClaw.json -> openclaw.json
    content = content.replace('QClaw.json', 'openclaw.json')
    print("✅ 修复1: 替换 QClaw.json -> openclaw.json")
    
    # 修复2: 替换错误的目录名 .QClaw -> .qclaw
    content = content.replace('".QClaw"', '".qclaw"')
    content = content.replace("'.QClaw'", "'.qclaw'")
    print("✅ 修复2: 替换 .QClaw -> .qclaw")
    
    # 修复3: 简化逻辑，移除对不存在的 .QClaw 目录的检查
    old_logic = '''            # 读取QClaw/QClaw全局配置文件
            # 优先检查QClaw路径（qclaw），其次QClaw路径（QClaw）
            user_home = os.path.expanduser("~")
            qclaw_config_path = os.path.join(user_home, ".qclaw", "openclaw.json")
            QClaw_config_path = os.path.join(user_home, ".qclaw", "openclaw.json")
            
            # 确定使用哪个配置文件
            if os.path.exists(qclaw_config_path):
                config_path = qclaw_config_path
                logger.info(f"使用QClaw配置路径: {config_path}")
            elif os.path.exists(QClaw_config_path):
                config_path = QClaw_config_path
                logger.info(f"使用QClaw配置路径: {config_path}")
            else:
                logger.warning(f"配置文件不存在: {qclaw_config_path} 和 {QClaw_config_path}")
                return 'NOT_SET_IN_QClaw'
            '''
    
    new_logic = '''            # 读取QClaw全局配置文件
            # QClaw的配置文件路径：~/.qclaw/openclaw.json
            user_home = os.path.expanduser("~")
            config_path = os.path.join(user_home, ".qclaw", "openclaw.json")
            
            # 检查配置文件是否存在
            if not os.path.exists(config_path):
                logger.warning(f"QClaw配置文件不存在: {config_path}")
                return 'NOT_SET_IN_QClaw'
            
            logger.info(f"使用QClaw配置路径: {config_path}")
            '''
    
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        print("✅ 修复3: 简化配置文件查找逻辑")
    else:
        print("⚠️ 未找到预期的老逻辑，跳过修复3")
    
    # 修复4: 统一变量名 QClaw_config -> qclaw_config
    content = content.replace('QClaw_config = json.load(f)', 'qclaw_config = json.load(f)')
    content = content.replace('QClaw_config.get(', 'qclaw_config.get(')
    print("✅ 修复4: 统一变量名为 qclaw_config")
    
    # 检查修改后长度
    new_len = len(content)
    print(f"修改后文件长度: {new_len} 字符")
    print(f"长度变化: {new_len - original_len} 字符")
    
    # 备份原文件
    backup_path = config_py_path + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(open(config_py_path, 'r', encoding='utf-8').read())
    print(f"✅ 已备份原文件到: {backup_path}")
    
    # 写入修复后的文件
    with open(config_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已修复并写入: {config_py_path}")
    
    # 验证修复
    print("\n" + "="*60)
    print("验证修复结果:")
    print("="*60)
    
    with open(config_py_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 检查关键行
    for i, line in enumerate(lines, 1):
        if '_get_from_QClaw_global' in line or 'openclaw.json' in line or 'config_path' in line:
            print(f"  L{i}: {line.rstrip()}")
    
    print("\n✅ 修复完成！")

if __name__ == '__main__':
    fix_config_py()
