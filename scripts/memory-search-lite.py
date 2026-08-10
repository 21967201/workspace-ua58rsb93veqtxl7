#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory-search-lite.py — 零依赖记忆全文检索(BM25降级方案)
=========================================================
用途: 当向量模型不可用时的检索兜底。纯 Python 标准库, 无需任何外部依赖。
覆盖范围: memory/ 全部 md(含 warm/) + archive/memory/ 的 .gz 压缩归档
        → 冷数据压缩后依然可被检索到, 实现"归档不失联"
算法: BM25 + 中文二元切分(bigram), 对中文场景比朴素关键词匹配显著更准
用法:
  python scripts/memory-search-lite.py "Token 压缩"
  python scripts/memory-search-lite.py "灾难性遗忘" 10
"""
import os
import sys
import gzip
import re
import math
from collections import Counter

WORKSPACE = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
ARCHIVE_DIR = os.path.join(WORKSPACE, "archive", "memory")
CHUNK_SIZE = 500
K1, B = 1.5, 0.75   # BM25 参数


def tokenize(text):
    """中英混合切词: 英文按词, 中文按二元组"""
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    han = re.findall(r"[\u4e00-\u9fff]+", text)
    for seg in han:
        if len(seg) == 1:
            tokens.append(seg)
        else:
            tokens.extend(seg[i:i + 2] for i in range(len(seg) - 1))
    return tokens


def read_any(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rb") as f:
            return f.read().decode("utf-8", errors="replace")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def collect_chunks():
    """返回 [(source_label, chunk_text)]"""
    chunks = []
    sources = []
    for root, dirs, names in os.walk(MEMORY_DIR):
        dirs[:] = [d for d in dirs if d not in ("memory-index", ".dreams")]
        for n in names:
            if n.endswith(".md"):
                sources.append(os.path.join(root, n))
    if os.path.isdir(ARCHIVE_DIR):
        for root, _, names in os.walk(ARCHIVE_DIR):
            for n in names:
                if n.endswith(".md.gz"):
                    sources.append(os.path.join(root, n))
    for path in sources:
        try:
            text = read_any(path)
        except Exception:
            continue
        rel = os.path.relpath(path, WORKSPACE)
        tier = "冷·归档" if ".gz" in path else ("温" if os.sep + "warm" + os.sep in path else "热")
        for i in range(0, len(text), CHUNK_SIZE):
            seg = text[i:i + CHUNK_SIZE].strip()
            if seg:
                chunks.append((f"[{tier}] {rel}", seg))
    return chunks


def bm25_search(query, chunks, top_k=5):
    q_tokens = tokenize(query)
    if not q_tokens:
        return []
    docs = [tokenize(c[1]) for c in chunks]
    N = len(docs)
    avgdl = sum(len(d) for d in docs) / N if N else 0
    # 文档频率
    df = Counter()
    for d in docs:
        for t in set(d):
            if t in q_tokens:
                df[t] += 1
    scores = []
    for idx, d in enumerate(docs):
        tf = Counter(d)
        dl = len(d)
        score = 0.0
        for t in q_tokens:
            if t not in tf:
                continue
            idf = math.log((N - df[t] + 0.5) / (df[t] + 0.5) + 1)
            score += idf * (tf[t] * (K1 + 1)) / (tf[t] + K1 * (1 - B + B * dl / avgdl))
        if score > 0:
            scores.append((score, idx))
    scores.sort(reverse=True)
    return scores[:top_k]


def main():
    if len(sys.argv) < 2:
        print('用法: python memory-search-lite.py "关键词" [topN]')
        return
    args = sys.argv[1:]
    top_k = 5
    if args[-1].isdigit():
        top_k = int(args[-1])
        args = args[:-1]
    query = " ".join(args)

    chunks = collect_chunks()
    print(f"索引范围: {len(chunks)} 个文本块 (含热/温/冷归档)")
    results = bm25_search(query, chunks, top_k)
    if not results:
        print(f"未找到与「{query}」相关的内容")
        return
    print(f"\n=== 检索: {query} (top {len(results)}) ===")
    for rank, (score, idx) in enumerate(results, 1):
        label, text = chunks[idx]
        preview = re.sub(r"\s+", " ", text)[:200]
        print(f"\n[{rank}] score={score:.2f} | {label}")
        print(f"    {preview}...")


if __name__ == "__main__":
    main()
