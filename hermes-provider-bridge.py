import subprocess
import json
import os
import sys
from pathlib import Path

HERMES_CLI = r"D:\QClaw\v0.2.35.624\resources\python\python.exe"
HERMES_MODULE = "hermes_cli"
HERMES_HOME = r"C:\Users\Administrator\.hermes"
HERMES_LIBS = r"D:\QClaw\v0.2.35.624\resources\hermes\libs"

def call_hermes(prompt: str, model: str = "glm-4-flash", max_turns: int = 1) -> dict:
    env = os.environ.copy()
    env["HERMES_HOME"] = HERMES_HOME
    env["PYTHONPATH"] = HERMES_LIBS
    
    cmd = [
        HERMES_CLI, "-m", HERMES_MODULE,
        "-z", prompt,
        "--model", model,
        "--max-turns", str(max_turns),
        "--no-stream"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # 解析输出
        output = result.stdout
        errors = result.stderr
        
        # 尝试提取 JSON 响应
        if "assistant" in output.lower():
            # Hermes CLI 输出可能是 markdown 或 JSON
            return {
                "success": result.returncode == 0,
                "model": model,
                "response": output.strip(),
                "error": errors.strip() if errors else None,
                "exit_code": result.returncode
            }
        else:
            return {
                "success": False,
                "model": model,
                "response": output.strip() or errors.strip(),
                "error": "No valid response",
                "exit_code": result.returncode
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "model": model,
            "response": "",
            "error": "Timeout after 120s",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "model": model,
            "response": "",
            "error": str(e),
            "exit_code": -1
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No prompt provided"}))
        sys.exit(1)
    
    prompt = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "glm-4-flash"
    
    result = call_hermes(prompt, model)
    print(json.dumps(result, ensure_ascii=False, indent=2))
