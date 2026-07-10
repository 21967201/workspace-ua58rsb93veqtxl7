#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Distill workflow discovery: scan sessions, find recurring patterns, distill to skills."""
import os, json, re, glob, datetime
from collections import Counter, defaultdict

BASE = r"C:\Users\Administrator\.qclaw\workspace\sessions"
CUTOFF = datetime.datetime.now() - datetime.timedelta(days=30)

def read_utf8(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")

def read_gbk_fallback(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except Exception:
        return raw.decode("gbk", errors="replace")

# 1. Find session dirs with recent activity
sessions = []
for d in os.listdir(BASE):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    # recent file?
    recent = False
    for root, _, files in os.walk(dp):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
            except Exception:
                continue
            if mtime >= CUTOFF:
                recent = True
                break
        if recent:
            break
    if not recent:
        continue
    # parse store.json and summary
    store = {}
    sp = os.path.join(dp, "store.json")
    name = ""
    msg_count = 0
    if os.path.exists(sp):
        try:
            store = json.loads(read_gbk_fallback(sp))
            name = store.get("name", "")
            msg_count = store.get("lastMessageCount", 0)
        except Exception as e:
            pass
    # summary files
    summaries = []
    for fn in sorted(os.listdir(dp)):
        if fn.startswith("summary_") and fn.endswith(".md"):
            summaries.append(read_utf8(os.path.join(dp, fn)))
    sessions.append({
        "dir": d,
        "name": name,
        "msg_count": msg_count,
        "summary": "\n".join(summaries),
    })

print(f"Scanned sessions (recent 30d): {len(sessions)}")

# 2. Build a normalized task-title frequency map
title_counter = Counter()
for s in sessions:
    t = (s["name"] or "").strip()
    if t:
        title_counter[t] += 1

print("\n=== Task title frequency (min repeat >=3) ===")
recurring_titles = {t: c for t, c in title_counter.items() if c >= 3}
for t, c in title_counter.most_common():
    mark = "<<< recurring" if c >= 3 else ""
    print(f"  {c:>3}x  {t}  {mark}")

# 3. Extract step patterns from summaries (numbered step lines)
step_pat = re.compile(r"^\s*\d+[\.\)、]\s*(.*)$", re.MULTILINE)
keyword_pat = re.compile(r"^(扫描|识别|验证|提取|写入|生成|创建|更新|检查|推送|同步|分析|压缩|合并|修复|评估|搜索|读取|调用|报告|保存|导出)[：:]?\s*(.*)$")

# Build a normalized "verb + keyword" signature for each summary's step list
step_signatures = defaultdict(list)
for s in sessions:
    steps = step_pat.findall(s["summary"])
    sig = []
    for st in steps:
        st = st.strip()
        m = keyword_pat.match(st)
        if m:
            verb = m.group(1)
            sig.append(verb)
    if sig:
        key = " > ".join(sig)
        step_signatures[key].append(s["name"])

print(f"\n=== Distinct step-signature chains: {len(step_signatures)} ===")
sig_counter = Counter()
for key, names in step_signatures.items():
    sig_counter[key] = len(step_signatures[key])

# 4. Verb frequency across all summaries (tool/task action patterns)
verb_counter = Counter()
for s in sessions:
    for st in step_pat.findall(s["summary"]):
        m = keyword_pat.match(st.strip())
        if m:
            verb_counter[m.group(1)] += 1

print("\n=== Verb/action frequency across summaries ===")
for v, c in verb_counter.most_common():
    print(f"  {c:>3}x  {v}")

# Save raw analysis for the report
analysis = {
    "scan_time": datetime.datetime.now().isoformat(timespec="seconds"),
    "scanned": len(sessions),
    "recurring_titles": recurring_titles,
    "title_counter": dict(title_counter),
    "verb_counter": dict(verb_counter),
    "sessions": [{"dir": s["dir"], "name": s["name"], "msg_count": s["msg_count"]} for s in sessions],
}
with open(os.path.join(os.path.dirname(__file__), "distill_analysis.json"), "w", encoding="utf-8") as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

# 5. Identify candidate skills (repeating + self-contained + generic)
# Heuristic: title repeats >=3 AND not project-bound (1688/GBrain specific kept but flagged)
candidates = []
for t, c in recurring_titles.items():
    # genericity: does it reference specific project names?
    project_bound = any(p in t for p in ["1688", "GBrain", "腾讯文档"])
    conf = min(1.0, 0.4 + c * 0.1)
    if not project_bound:
        conf = min(1.0, conf + 0.15)
    candidates.append({"title": t, "count": c, "project_bound": project_bound, "confidence": round(conf, 2)})

print("\n=== Skill candidates (confidence>0.7) ===")
for c in sorted(candidates, key=lambda x: -x["confidence"]):
    flag = "PROJECT-BOUND" if c["project_bound"] else ""
    sel = ">>> CREATE" if c["confidence"] > 0.7 else "--- skip"
    print(f"  conf={c['confidence']:.2f}  {c['title']} (x{c['count']}) {flag}  {sel}")

# Save candidates
with open(os.path.join(os.path.dirname(__file__), "distill_candidates.json"), "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)
