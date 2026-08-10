#!/usr/bin/env python3
"""
Hermes CLI Bridge - OpenClaw Provider Wrapper
测试 Hermes Python CLI 调用
"""
import subprocess
import json
import os
import sys
from pathlib import Path

# 配置
HERMES_CLI = r"D:\QClaw\v0.2.35.624\resources\python\python.exe"
HERMES_MODULE = "hermes_cli"
HERMES_HOME = r"C:\Users\Administrator\.hermes"
HERMES_LIBS = r"D:\QClaw\v0.2.35.624\resources\hermes\libs"

def call_hermes(prompt: str, model: str = "glm-4-flash") -> dict:
    """调用 Hermes CLI 获取响应"""
    env = os.environ.copy()
    env["HERMES_HOME"] = HERMES_HOME
    env["PYTHONPATH"] = HERMES_LIBS
    # 强制 UTF-8 输出
    env["PYTHONIOENCODING"] = "utf-8"
    
    # 正确的 Hermes CLI 参数（-z 是 one-shot 模式）
    cmd = [
        HERMES_CLI, "-m", HERMES_MODULE,
        "-z", prompt,
        "--model", model
    ]
    
    try:
        # 使用 UTF-8 编码
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120
        )
        
        output = result.stdout
        errors = result.stderr
        
        if result.returncode == 0 and output.strip():
            return {
                "success": True,
                "model": model,
                "exit_code": 0,
                "response": output.strip(),
                "error": errors.strip() if errors else None
            }
        else:
            return {
                "success": False,
                "model": model,
                "exit_code": result.returncode,
                "response": output.strip() if output else "",
                "error": errors.strip() if errors else ("Exit code " + str(result.returncode))
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "model": model,
            "exit_code": -1,
            "response": "",
            "error": "Timeout after 120s"
        }
    except Exception as e:
        return {
            "success": False,
            "model": model,
            "exit_code": -1,
            "response": "",
            "error": str(e)
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: hermes-cli-test.py <prompt> [model]"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "glm-4-flash"
    
    result = call_hermes(prompt, model)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
