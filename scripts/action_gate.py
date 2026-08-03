#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Gate — 确定性行动闸门 (Harness System2 层)
零依赖纯 Python 实现，替代 OPA/Rego 外部引擎。

用法:
  python action_gate.py --check "rm -rf /tmp/x"      # 命令风险
  python action_gate.py --path "C:\\Users\\x\\a.txt"  # 路径风险
  python action_gate.py --emotion                      # 情感状态
  python action_gate.py --full --command "..." --path "..."  # 完整闸门
"""
import argparse
import json
import os
import re
import sys

# ---------- 常量 ----------
BLOCK_COMMANDS = [
    r"rm\s+-rf", r"Remove-Item\s+-Recurse", r"del\s+/s", r"diskpart",
    r"format\s+[a-z]:", r"bootrec", r"reg\s+delete", r"sc\s+delete",
    r"taskkill\s+/f", r"shutdown", r"Format-Volume", r"Clear-Disk",
]

WARN_COMMANDS = [
    r"rm\b", r"Remove-Item", r"del\b", r"reg\s+add", r"net\s+user",
    r"New-ItemProperty", r"Set-ItemProperty", r"Move-Item",
]

SAFE_ROOT = r"D:\QClawX"
EMOTION_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "emotional-state.json")

# ---------- 判定函数 ----------
def check_command(cmd: str) -> dict:
    """命令风险判定。"""
    if not cmd:
        return {"verdict": "allow", "level": 0, "reasons": ["empty command"]}
    for pat in BLOCK_COMMANDS:
        if re.search(pat, cmd, re.IGNORECASE):
            return {"verdict": "block", "level": 3, "reasons": [f"blocked command pattern: {pat}"]}
    for pat in WARN_COMMANDS:
        if re.search(pat, cmd, re.IGNORECASE):
            return {"verdict": "warn", "level": 2, "reasons": [f"warning command pattern: {pat}"]}
    return {"verdict": "allow", "level": 0, "reasons": ["command not in blocklist"]}

def check_path(path: str) -> dict:
    """路径写入风险判定。"""
    if not path:
        return {"verdict": "allow", "level": 0, "reasons": ["empty path"]}
    p = path.replace("/", "\\")
    if p.upper().startswith(SAFE_ROOT.upper()):
        return {"verdict": "allow", "level": 0, "reasons": [f"path inside {SAFE_ROOT}"]}
    if re.match(r"^[A-Z]:\\$", p) or re.match(r"^[A-Z]:\\Windows", p, re.IGNORECASE):
        return {"verdict": "block", "level": 3, "reasons": ["system critical path"]}
    if re.match(r"^[A-Z]:\\Users\\.+\\Desktop", p, re.IGNORECASE) or \
       re.match(r"^[A-Z]:\\Users\\.+\\Downloads", p, re.IGNORECASE):
        return {"verdict": "warn", "level": 2, "reasons": ["user directory (Desktop/Downloads)"]}
    return {"verdict": "warn", "level": 1, "reasons": ["path outside D:\\QClawX"]}

def check_emotion() -> dict:
    """情感状态检查 (PAD 模型)。"""
    try:
        with open(EMOTION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        default = data.get("default", {})
        p = float(default.get("pleasure", 0))
        a = float(default.get("arousal", 0))
        high_risk = p < -0.5 and a > 0.5
        return {
            "verdict": "warn" if high_risk else "allow",
            "level": 2 if high_risk else 0,
            "reasons": ["high-risk emotion (P<-0.5, A>0.5) → escalate"] if high_risk else ["emotion stable"],
            "emotion": default,
        }
    except FileNotFoundError:
        return {"verdict": "allow", "level": 0, "reasons": ["no emotion file"], "emotion": None}

def full_gate(command: str, path: str) -> dict:
    """完整闸门：命令 + 路径 + 情感，取最高等级。"""
    results = [check_command(command), check_path(path), check_emotion()]
    max_level = max(r["level"] for r in results)
    reasons = []
    for r in results:
        reasons.extend(r["reasons"])
    verdict = "block" if max_level >= 3 else ("warn" if max_level >= 2 else "allow")
    out = {"verdict": verdict, "level": max_level, "reasons": reasons}
    for r in results:
        if "emotion" in r and r["emotion"]:
            out["emotion"] = r["emotion"]
    return out

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Action Gate — 确定性行动闸门")
    ap.add_argument("--check", help="检查命令风险")
    ap.add_argument("--path", help="检查路径风险")
    ap.add_argument("--emotion", action="store_true", help="检查情感状态")
    ap.add_argument("--full", action="store_true", help="完整闸门")
    ap.add_argument("--command", help="完整闸门: 命令")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    if args.full:
        result = full_gate(args.command or "", args.path or "")
    elif args.check:
        result = check_command(args.check)
    elif args.path:
        result = check_path(args.path)
    elif args.emotion:
        result = check_emotion()
    else:
        result = {"verdict": "allow", "level": 0, "reasons": ["no check requested"]}

    if args.json or args.full:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"verdict={result['verdict']} level={result['level']} reasons={result['reasons']}")
    sys.exit(0 if result["level"] < 3 else 2)

if __name__ == "__main__":
    main()
