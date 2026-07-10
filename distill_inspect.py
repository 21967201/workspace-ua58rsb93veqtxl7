#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, re, datetime
from collections import Counter

base = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
skills_dir = os.path.join(base, "skills")

# 1. Count junk workflow-* skills from 06-23 run
junk = [d for d in os.listdir(skills_dir) if d.startswith("workflow-")]
pure_tool = [d for d in junk if re.fullmatch(
    r"workflow-(exec|read|write|edit|process|web_search|skillhub_install)"
    r"(-(exec|read|write|edit|process|web_search|skillhub_install))*", d)]
print("Junk 'workflow-*' skills:", len(junk), "| pure tool-n-gram:", len(pure_tool))

# 2. Verify key skills
for name in ["GitHub同步推送-workflow", "daily-tech-breakthrough-monitor",
             "自动报告生成-workflow", "负一屏推送-workflow"]:
    p = os.path.join(skills_dir, name)
    if os.path.isdir(p):
        files = os.listdir(p)
        print(f"[{name}] files={files}")
    else:
        print(f"[{name}] MISSING")

# 3. Step-verb chain analysis across recent summaries for NEW genuine patterns
sessions_raw = r"C:\Users\Administrator\.qclaw\workspace\sessions"
CUTOFF = datetime.datetime.now() - datetime.timedelta(days=30)

def read_gbk(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except Exception:
        return raw.decode("gbk", errors="replace")

sigs = Counter()
for d in os.listdir(sessions_raw):
    dp = os.path.join(sessions_raw, d)
    if not os.path.isdir(dp):
        continue
    recent = False
    for root, _, files in os.walk(dp):
        for fn in files:
            try:
                if datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, fn))) >= CUTOFF:
                    recent = True
                    break
            except Exception:
                pass
        if recent:
            break
    if not recent:
        continue
    summary = ""
    for fn in sorted(os.listdir(dp)):
        if fn.startswith("summary_") and fn.endswith(".md"):
            summary += read_gbk(os.path.join(dp, fn)) + "\n"
    verbs = re.findall(
        r"(扫描|识别|验证|提取|写入|生成|创建|更新|检查|推送|同步|分析|压缩|合并|修复|评估|搜索|读取|调用|报告|保存|导出|定位|整理|固化|封装|通知|部署|监控)",
        summary)
    if verbs:
        sigs[">".join(verbs[:8])] += 1

print("\n=== Distinct step-verb chains:", len(sigs))
print("Top 10 most common step chains:")
for s, c in sigs.most_common(10):
    print(f"  {c}x  {s}")
