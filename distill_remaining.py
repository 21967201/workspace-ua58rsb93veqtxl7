#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, shutil, json

sd = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7\skills"
quarantine = os.path.join(sd, "_quarantine_junk_2026-07-07")
remain = [d for d in os.listdir(sd) if d.startswith("workflow-")]
print("Remaining workflow-* dirs:", remain)
moved = []
for d in remain:
    shutil.move(os.path.join(sd, d), os.path.join(quarantine, d))
    moved.append(d)
print("Quarantined extra:", moved)

# Final skill count breakdown
all_dirs = [d for d in os.listdir(sd) if os.path.isdir(os.path.join(sd, d))]
real = [d for d in all_dirs if d != "_quarantine_junk_2026-07-07"]
print(f"\nTotal skill dirs now: {len(all_dirs)}")
print(f"  Real skills (excl. quarantine): {len(real)}")
print(f"  Quarantined junk: {len(os.listdir(quarantine))}")
print("\nReal skills:", sorted(real))

with open("distill_final_state.json", "w", encoding="utf-8") as f:
    json.dump({"real_skills": sorted(real), "quarantined": len(os.listdir(quarantine))}, f, ensure_ascii=False, indent=2)
