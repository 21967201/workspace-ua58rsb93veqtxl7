#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Distill scan: enumerate recent sessions, build title frequency, dump candidates."""
import os, json, datetime
from collections import Counter

BASE = r"C:\Users\Administrator\.qclaw\workspace\sessions"
CUTOFF = datetime.datetime.now() - datetime.timedelta(days=30)

def read_gbk(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except Exception:
        return raw.decode("gbk", errors="replace")

sessions = []
for d in os.listdir(BASE):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
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
    name = ""
    msg = 0
    sp = os.path.join(dp, "store.json")
    if os.path.exists(sp):
        try:
            st = json.loads(read_gbk(sp))
            name = st.get("name", "")
            msg = st.get("lastMessageCount", 0)
        except Exception:
            pass
    summary = ""
    for fn in sorted(os.listdir(dp)):
        if fn.startswith("summary_") and fn.endswith(".md"):
            summary += read_gbk(os.path.join(dp, fn)) + "\n"
    sessions.append({"dir": d, "name": name, "msg": msg, "summary": summary})

print("Scanned recent sessions:", len(sessions))
tc = Counter()
for s in sessions:
    t = (s["name"] or "").strip()
    if t:
        tc[t] += 1
print("\n=== Title frequency (>=2) ===")
for t, c in tc.most_common():
    if c >= 2:
        print(f"  {c:>3}x  {t}")
print("\nDistinct non-empty titles:", len([t for t in tc if t]))
print("Titles >=3:", {t: c for t, c in tc.items() if c >= 3})

# Build candidates with confidence
candidates = []
for t, c in tc.items():
    if c < 3:
        continue
    project_bound = any(p in t for p in ["1688", "GBrain", "华为", "美团", "美柚"])
    conf = min(1.0, 0.4 + c * 0.1)
    if not project_bound:
        conf = min(1.0, conf + 0.15)
    candidates.append({
        "title": t, "count": c, "project_bound": project_bound,
        "confidence": round(conf, 2),
    })
candidates.sort(key=lambda x: -x["confidence"])
print("\n=== Candidates (count>=3) ===")
for c in candidates:
    flag = "PROJECT-BOUND" if c["project_bound"] else "generic"
    sel = ">>> CREATE" if c["confidence"] > 0.7 and not c["project_bound"] else "--- skip"
    print(f"  conf={c['confidence']:.2f}  {c['title']} (x{c['count']}) [{flag}]  {sel}")

with open("distill_raw_scan.json", "w", encoding="utf-8") as f:
    json.dump({
        "count": len(sessions),
        "titles": dict(tc),
        "candidates": candidates,
        "sessions": [{"dir": s["dir"], "name": s["name"], "msg": s["msg"]} for s in sessions],
    }, f, ensure_ascii=False, indent=2)
print("\nWrote distill_raw_scan.json")
