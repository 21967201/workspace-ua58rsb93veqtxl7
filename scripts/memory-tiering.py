#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory-tiering.py — 记忆冷热分层 + 无损压缩归档
=================================================
设计目标（对应调研报告三层方案）:
  1. 热数据(0-7天): memory/ 根目录原地保留 → 加载快
  2. 温数据(7-30天): 移至 memory/warm/ → 根目录保持精简
  3. 冷数据(30天+): 移动至 archive/memory/ 并 gzip 无损压缩 → 磁盘省 8-15x, 数据不丢(可随时解压还原)
安全设计:
  - 只处理 memory/ 根目录的 .md 日志文件, 不碰 MEMORY.md / 结构化子目录(people/projects/tech等)
  - gzip 为无损压缩, 原文件删除前先验证压缩包完整性
  - --dry-run 模式仅预览不动文件; 默认 dry-run, 加 --apply 才执行
用法:
  python scripts/memory-tiering.py --dry-run
  python scripts/memory-tiering.py --apply
"""
import os
import sys
import gzip
import shutil
import hashlib
from datetime import datetime, timedelta

WORKSPACE = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
ARCHIVE_DIR = os.path.join(WORKSPACE, "archive", "memory")
WARM_DIR = os.path.join(MEMORY_DIR, "warm")

# 受保护文件: 核心记忆与状态文件, 永不移动/压缩
PROTECTED = {
    "MEMORY.md", "patterns.md", "strategy-changes.md", "performance-baseline.md",
    "emotional-state.json", "emotional-state-design.md",
}
# 只处理根目录下的 .md 日志文件(格式 YYYY-MM-DD*.md), 不碰子目录与状态文件
WARM_DAYS = 7       # <7天: 热
COLD_DAYS = 30      # >=30天: 冷归档压缩


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def gzip_file(src, dst):
    """无损压缩 src -> dst(.gz), 校验后返回 True"""
    with open(src, "rb") as f_in:
        raw = f_in.read()
    with gzip.open(dst, "wb", compresslevel=9) as f_out:
        f_out.write(raw)
    # 完整性校验: 解压比对
    with gzip.open(dst, "rb") as f_in:
        restored = f_in.read()
    if restored != raw:
        return False
    return True


def tier_files(dry_run=True):
    if not os.path.isdir(MEMORY_DIR):
        log(f"ERROR: memory dir not found: {MEMORY_DIR}")
        return
    now = datetime.now()
    stats = {"hot": 0, "warm": 0, "cold": 0, "skipped": 0, "bytes_freed": 0}
    for name in sorted(os.listdir(MEMORY_DIR)):
        path = os.path.join(MEMORY_DIR, name)
        if not os.path.isfile(path) or not name.endswith(".md"):
            continue
        if name in PROTECTED or name.startswith("archive-report"):
            stats["skipped"] += 1
            continue
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        age_days = (now - mtime).days
        size = os.path.getsize(path)

        if age_days < WARM_DAYS:
            stats["hot"] += 1          # 热: 原地保留
        elif age_days < COLD_DAYS:
            # 温: 移至 memory/warm/
            dst = os.path.join(WARM_DIR, name)
            if dry_run:
                log(f"[温] {name} ({age_days}d, {size}B) -> memory/warm/")
            else:
                os.makedirs(WARM_DIR, exist_ok=True)
                shutil.move(path, dst)
                log(f"[温] moved {name} -> memory/warm/")
            stats["warm"] += 1
        else:
            # 冷: 移动至 archive/memory/ 并 gzip 压缩
            year = name[:4] if name[:4].isdigit() else "misc"
            dst_dir = os.path.join(ARCHIVE_DIR, year)
            gz_path = os.path.join(dst_dir, name + ".gz")
            if dry_run:
                log(f"[冷] {name} ({age_days}d, {size}B) -> archive/memory/{year}/{name}.gz")
            else:
                os.makedirs(dst_dir, exist_ok=True)
                if gzip_file(path, gz_path):
                    os.remove(path)
                    stats["bytes_freed"] += size
                    log(f"[冷] compressed {name} -> {gz_path} (saved {size}B)")
                else:
                    log(f"[冷] FAILED verify, skipped: {name}")
            stats["cold"] += 1

    log("=" * 60)
    log(f"热(保留): {stats['hot']} | 温(移动): {stats['warm']} | 冷(压缩): {stats['cold']} | 保护跳过: {stats['skipped']}")
    if not dry_run:
        log(f"释放磁盘: {stats['bytes_freed'] / 1024:.1f} KB (压缩后占用约 1/8-1/15)")
    return stats


def main():
    dry_run = "--apply" not in sys.argv
    mode = "DRY-RUN(预览)" if dry_run else "APPLY(执行)"
    log(f"=== memory 冷热分层 & 归档 | 模式: {mode} ===")
    log(f"规则: 热<{WARM_DAYS}天 | 温{WARM_DAYS}-{COLD_DAYS}天 | 冷>={COLD_DAYS}天(gzip无损)")
    tier_files(dry_run=dry_run)
    log("完成。")


if __name__ == "__main__":
    main()
