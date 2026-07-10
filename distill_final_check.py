#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
sd = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7\skills"
q = os.path.join(sd, "_quarantine_junk_2026-07-07")
real = sorted(d for d in os.listdir(sd) if os.path.isdir(os.path.join(sd, d)) and d != "_quarantine_junk_2026-07-07")
print("Active skills:", real)
print("Quarantined count:", len(os.listdir(q)))
print("Quarantine dir exists:", os.path.isdir(q))
