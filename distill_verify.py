#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

sd = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7\skills"
for name in ["daily-tech-breakthrough-monitor", "GitHub同步推送-workflow"]:
    p = os.path.join(sd, name, "SKILL.md")
    print("=" * 50)
    print(name)
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()
    print(f"[{len(txt)} bytes] first 900 chars:")
    print(txt[:900])
