#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory-vector-index.py — 记忆语义检索索引 v3 (纯标准库, 零外部依赖)
====================================================================
对应调研报告"层面2: RAG 外部知识库"。之前 chromadb 在本机静默崩溃(内存不足), 故改用
纯 Python 标准库实现的 TF-IDF 向量索引 + 余弦相似度检索。功能等价:
  - 切块 → TF-IDF 哈希向量(512维, 中文bigram友好) → 增量持久化到 JSON
  - 覆盖 memory/ 全部 md(含 warm/) + archive/memory/ 的 .gz 压缩归档
  - 数据永久保留: 索引只是副本, 原始文件不动
用法:
  python scripts/memory-vector-index.py build [--force]  # 构建/增量更新
  python scripts/memory-vector-index.py search "关键词" [topN]
  python scripts/memory-vector-index.py stats
"""
import os
import sys
import gzip
import re
import json
import math
import hashlib
from collections import Counter
from datetime import datetime

# Windows 控制台 GBK 下安全输出(emoji等)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

WORKSPACE = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
ARCHIVE_DIR = os.path.join(WORKSPACE, "archive", "memory")
INDEX_FILE = os.path.join(MEMORY_DIR, "memory-index.json")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 60
DIM = 512


def log(msg):
    print(msg, flush=True)


def tokenize(text):
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    for seg in re.findall(r"[\u4e00-\u9fff]+", text):
        tokens.extend(seg[i:i + 2] for i in range(len(seg) - 1))
    return tokens


def hash_vec(tokens):
    v = [0.0] * DIM
    if not tokens:
        return v
    tf = Counter(tokens)
    norm = math.sqrt(len(tokens))
    for tok, cnt in tf.items():
        h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
        v[h % DIM] += (1 if (h >> 8) % 2 == 0 else -1) * (1 + math.log(cnt)) / norm
    return v


def read_any(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rb") as f:
            return f.read().decode("utf-8", errors="replace")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def collect_sources():
    files = []
    for root, dirs, names in os.walk(MEMORY_DIR):
        dirs[:] = [d for d in dirs if d != ".dreams"]
        for n in names:
            if n.endswith(".md") and not n.endswith(".gz") and not n.startswith("memory-index"):
                files.append(os.path.join(root, n))
    if os.path.isdir(ARCHIVE_DIR):
        for root, _, names in os.walk(ARCHIVE_DIR):
            for n in names:
                if n.endswith(".md.gz"):
                    files.append(os.path.join(root, n))
    return files


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= size:
        return [text] if text.strip() else []
    chunks, step = [], size - overlap
    for i in range(0, len(text), step):
        c = text[i:i + size]
        if c.strip():
            chunks.append(c)
    return chunks


def _doc_key(path):
    """文件级 key: 路径+mtime(增量指纹)"""
    mtime = os.path.getmtime(path)
    return f"{os.path.relpath(path, WORKSPACE)}|{int(mtime)}"


def build(force=False):
    # 读取现有索引
    index = {"docs": {}}
    if os.path.isfile(INDEX_FILE) and not force:
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index = json.load(f)
        except Exception:
            index = {"docs": {}}

    sources = collect_sources()
    # 移除已不存在的文档
    current_keys = {_doc_key(p) for p in sources}
    stale = [k for k in index["docs"] if k.split("|")[0] not in {p.split("|")[0] for p in current_keys}]
    # 简化: 用相对路径判断
    cur_paths = {os.path.relpath(p, WORKSPACE) for p in sources}
    stale = [k for k in index["docs"] if k.split("|")[0] not in cur_paths]
    for k in stale:
        del index["docs"][k]

    added = updated = skipped = 0
    for path in sources:
        key = _doc_key(path)
        rel = os.path.relpath(path, WORKSPACE)
        if key in index["docs"]:
            skipped += 1
            continue
        try:
            text = read_any(path)
        except Exception as e:
            log(f"  [skip] {rel}: {e}")
            continue
        chunks = chunk_text(text)
        if not chunks:
            continue
        tier = "冷" if ".gz" in path else ("温" if os.sep + "warm" + os.sep in path else "热")
        docs = []
        for i, c in enumerate(chunks):
            docs.append({
                "id": f"{rel}#{i}",
                "text": c,
                "vec": hash_vec(tokenize(c)),
                "path": rel,
                "tier": tier,
                "mtime": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
            })
        index["docs"][key] = docs
        if stale or force:
            updated += 1
        else:
            added += 1

    index["_meta"] = {
        "built": datetime.now().isoformat(),
        "total_chunks": sum(len(v) for v in index["docs"].values()),
        "total_docs": len(index["docs"]),
    }
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)
    log(f"构建完成: 新增 {added} | 更新 {updated} | 未变 {skipped} | 文档 {len(index['docs'])} | 块 {index['_meta']['total_chunks']}")


def _cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return dot / (na * nb)


def search(query, top_k=5):
    if not os.path.isfile(INDEX_FILE):
        log("索引不存在, 先运行 build")
        return
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)
    qv = hash_vec(tokenize(query))
    scored = []
    for docs in index["docs"].values():
        for d in docs:
            s = _cosine(qv, d["vec"])
            if s > 0.05:
                scored.append((s, d))
    scored.sort(reverse=True, key=lambda x: x[0])
    log(f"\n=== 语义检索: {query} (top {min(top_k, len(scored))}/{len(scored)} 命中) ===")
    for i, (s, d) in enumerate(scored[:top_k], 1):
        preview = re.sub(r"\s+", " ", d["text"])[:180]
        log(f"\n[{i}] 相似度 {s:.3f} | [{d['tier']}] {d['path']} | {d['mtime'][:10]}")
        log(f"    {preview}...")


def stats():
    if not os.path.isfile(INDEX_FILE):
        log("索引不存在")
        return
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)
    log(f"索引文件: {INDEX_FILE}")
    log(f"文档数: {index['_meta']['total_docs']} | 块数: {index['_meta']['total_chunks']} | 构建于: {index['_meta']['built'][:16]}")
    tiers = {}
    for docs in index["docs"].values():
        for d in docs:
            tiers[d["tier"]] = tiers.get(d["tier"], 0) + 1
    log(f"分层覆盖: {tiers}")


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else "build"
    if cmd == "build":
        build(force="--force" in args)
    elif cmd == "search":
        top = 5
        if len(args) > 1 and args[-1].isdigit():
            top = int(args[-1])
            args = args[:-1]
        q = " ".join(args[1:])
        if q:
            search(q, top)
        else:
            log('用法: memory-vector-index.py search "关键词" [topN]')
    elif cmd == "stats":
        stats()
    else:
        log("用法: build [--force] | search \"关键词\" [topN] | stats")
