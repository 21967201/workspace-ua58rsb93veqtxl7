# -*- coding: utf-8 -*-
import os, json
from collections import defaultdict

BASE = r"C:\Users\Administrator\.qclaw\workspace\sessions"
targets = {"GitHub同步", "技术突破监控"}
found = []
for d in os.listdir(BASE):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    for fn in os.listdir(dp):
        if fn.startswith("summary_") and fn.endswith(".md"):
            txt = open(os.path.join(dp, fn), "rb").read().decode("utf-8", errors="replace")
            name = ""
            sp = os.path.join(dp, "store.json")
            if os.path.exists(sp):
                try:
                    name = json.loads(open(sp, "rb").read().decode("utf-8", errors="replace")).get("name", "")
                except Exception:
                    pass
            if name in targets:
                found.append((name, dp, txt))

groups = defaultdict(list)
for n, dp, txt in found:
    groups[n].append((dp, txt))

for n in targets:
    print("=" * 70)
    print("TITLE: %s  (samples: %d)" % (n, len(groups[n])))
    print("=" * 70)
    for i, (dp, txt) in enumerate(groups[n][:4], 1):
        print("--- sample %d (%s) ---" % (i, dp))
        print(txt.strip()[:1600])
        print()
