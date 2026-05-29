#!/usr/bin/env python3
"""完整修复 config.py - 直接重写问题方法"""

import os

def complete_fix():
    """完整修复 config.py"""
    
    config_py = r"D:\QClawX\data\workspace\skills\today-task\scripts\config.py"
    
    print("[STEP 1] 读取文件...")
    with open(config_py, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("[STEP 2] 查找问题方法...")
    in_method = False
    method_start = -1
    method_end = -1
    
    for i, line in enumerate(lines):
        if 'def _get_from_QClaw_global(self, key: str)' in line:
            in_method = True
            method_start = i
            print(f"  找到方法起始: L{i+1}")
        
        if in_method and method_end == -1:
            # 方法结束的标志是遇到下一个 def 或 class 或者空行+def
            if i > method_start and (line.strip().startswith('def ') or line.strip().startswith('class ')):
                method_end = i
                print(f"  找到方法结束: L{i}")
                break
    
    if method_end == -1:
        method_end = method_start + 50  # 保守估计
    
    print(f"[STEP 3] 重写方法 L{method_start+1} 到 L{method_end}...")
    
    # 新方法的代码
    new_method = '''    def _get_from_QClaw_global(self, key: str) -> str:
        """从QClaw全局配置获取配置值"""
        try:
            # 读取QClaw全局配置文件
            # QClaw的配置文件路径：~/.qclaw/openclaw.json
            user_home = os.path.expanduser("~")
            config_path = os.path.join(user_home, ".qclaw", "openclaw.json")
            
            # 检查配置文件是否存在
            if not os.path.exists(config_path):
                logger.warning(f"QClaw配置文件不存在: {config_path}")
                return 'NOT_SET_IN_QClaw'
            
            logger.info(f"使用QClaw配置路径: {config_path}")
            
            # 读取配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                qclaw_config = json.load(f)
            
            # 获取技能配置
            skill_config = qclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
            
            # 获取config中的值
            config_value = skill_config.get('config', {}).get(key)
            
            if config_value:
                # 对敏感信息（如authCode）进行脱敏处理
                if key == 'authCode' and isinstance(config_value, str) and len(config_value) > 4:
                    logger.debug(f"从QClaw全局配置读取 {key}: {config_value[:4]}***")
                else:
                    logger.debug(f"从QClaw全局配置读取 {key}: {config_value}")
                return config_value
            else:
                logger.debug(f"QClaw全局配置中未找到 {key}")
                return 'NOT_SET_IN_QClaw'
                
        except Exception as e:
            logger.error(f"读取QClaw全局配置失败: {str(e)}")
            return 'NOT_SET_IN_QClaw'

'''
    
    # 替换方法
    new_lines = lines[:method_start] + [new_method] + lines[method_end:]
    
    print("[STEP 4] 备份原文件...")
    backup_path = config_py + '.bak2'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"  备份到: {backup_path}")
    
    print("[STEP 5] 写入修复后的文件...")
    with open(config_py, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("[SUCCESS] 修复完成！")
    print("\n" + "="*60)
    print("验证修复结果:")
    print("="*60)
    
    # 验证
    with open(config_py, 'r', encoding='utf-8') as f:
        verify_lines = f.readlines()
    
    for i, line in enumerate(verify_lines[method_start:method_start+30], method_start+1):
        if 'config_path' in line or 'openclaw.json' in line or 'qclaw_config' in line:
            print(f"  L{i}: {line.rstrip()}")

if __name__ == '__main__':
    complete_fix()
