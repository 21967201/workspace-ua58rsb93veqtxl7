#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json, shutil

skills_dir = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7\skills"
quarantine = os.path.join(skills_dir, "_quarantine_junk_2026-07-07")
os.makedirs(quarantine, exist_ok=True)

moved = []
for d in sorted(os.listdir(skills_dir)):
    dp = os.path.join(skills_dir, d)
    if not os.path.isdir(dp):
        continue
    if d.startswith("workflow-") and re.fullmatch(
        r"workflow-(exec|read|write|edit|process|web_search|skillhub_install)"
        r"(-(exec|read|write|edit|process|web_search|skillhub_install))*", d):
        dst = os.path.join(quarantine, d)
        shutil.move(dp, dst)
        moved.append(d)

print(f"Quarantined {len(moved)} junk 'workflow-*' n-gram skills -> {quarantine}")

# Verify the two real recurring skills are healthy
report = {}
for name in ["GitHub同步推送-workflow", "daily-tech-breakthrough-monitor",
             "自动报告生成-workflow", "负一屏推送-workflow", "csts-skill-generator",
             "experience-tracker", "token-tracker", "meituan-miyou-integration"]:
    p = os.path.join(skills_dir, name)
    report[name] = os.path.isdir(p)

# Check GitHub skill has the dynamic-branch fix from 07-06
gh = os.path.join(skills_dir, "GitHub同步推送-workflow", "SKILL.md")
github_fixed = False
if os.path.exists(gh):
    with open(gh, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()
    github_fixed = ("abbrev-ref" in txt) or ("master" in txt and "分支" in txt)
print("GitHub skill dynamic-branch fix present:", github_fixed)
print("Real skills present:", {k: v for k, v in report.items()})

with open("distill_cleanup_result.json", "w", encoding="utf-8") as f:
    json.dump({"quarantined": len(moved), "github_fixed": github_fixed,
               "real_skills_present": report}, f, ensure_ascii=False, indent=2)
