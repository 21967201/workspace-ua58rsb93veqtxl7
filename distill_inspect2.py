#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

skills_dir = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7\skills"
names = ["workflow-read-read-read", "workflow-exec-exec-exec",
         "workflow-web_search-web_search-web_search", "workflow-skillhub_install-skillhub_install-skillhu"]
for name in names:
    p = os.path.join(skills_dir, name)
    print("=" * 40)
    print("DIR:", name)
    if os.path.isdir(p):
        for fn in os.listdir(p):
            fp = os.path.join(p, fn)
            print("  FILE:", fn, os.path.getsize(fp), "bytes")
            if fn.endswith(".md") or fn.endswith(".json"):
                with open(fp, "r", encoding="utf-8", errors="replace") as f:
                    print(f.read()[:500])
    else:
        print("  (missing)")
