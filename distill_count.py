#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, datetime

BASE = r"C:\Users\Administrator\.qclaw\workspace\sessions"
CUTOFF = datetime.datetime.now() - datetime.timedelta(days=30)

total_dirs = 0
active_dirs = 0
for d in os.listdir(BASE):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    total_dirs += 1
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
    if recent:
        active_dirs += 1

print(f"Total session dirs: {total_dirs}")
print(f"Dirs with file activity in last 30d: {active_dirs}")

# Also: how many have store.json / summary
with_summary = 0
for d in os.listdir(BASE):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    if any(fn.startswith("summary_") and fn.endswith(".md") for fn in os.listdir(dp)):
        with_summary += 1
print(f"Dirs containing a summary_*.md: {with_summary}")
