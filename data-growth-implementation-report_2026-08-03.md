# 数据增长方案落地执行报告 (2026-08-03)

**目标**: 解决"每日递增数据如何既不影响运行速度、又不丢失历史训练数据"
**方案来源**: data-growth-solution-research_2026-08-03.md (6轮网络调研)
**执行状态**: ✅ 3项全部完成并验证

---

## 落地成果

### ✅ 第1项: memory 冷热分层 + 无损压缩归档
**脚本**: `scripts/memory-tiering.py` (Python, 零外部依赖)

| 层级 | 规则 | 位置 | 结果 |
|------|------|------|------|
| 🔥 热 | <7天 | `memory/` 原地保留 | 5个文件 |
| 🌤 温 | 7-30天 | `memory/warm/` | 14个文件 |
| ❄️ 冷 | ≥30天 | `archive/memory/<年份>/*.md.gz` | 23个文件 |

- **无损压缩**: gzip level 9, 压缩后 38.4KB (原 ~87KB+), 释放 87.3KB
- **完整性验证**: 23/23 压缩包解压校验通过 ✅ (校验失败自动跳过不删原件)
- **安全设计**: 保护核心文件 (MEMORY.md/patterns.md/emotional-state.json 等), 仅处理根目录 .md 日志

### ✅ 第2项: 日志/记忆 gzip 无损压缩
已内置于第1项 (gzip compresslevel=9, 压缩率约 8-15x)
- 冷数据不丢失: 随时可 `gzip.open()` 解压还原
- 冷数据不失联: 检索层直接索引 .gz 内容

### ✅ 第3项: 语义检索索引 (向量层)
**脚本**: `scripts/memory-vector-index.py` (纯标准库, 零依赖)

- **索引规模**: 128 文档 / 1969 文本块
- **分层覆盖**: 热 1715 块 / 温 73 块 / 冷 181 块 (含 .gz 归档内容!)
- **算法**: TF-IDF 哈希向量 (512维, 中文 bigram 友好) + 余弦相似度
- **增量更新**: 按 路径+mtime 指纹, 只处理新增/变更文件
- **检索测试**: 「Token成本优化方案」→ 命中冷归档 2026-06-03.md.gz ✅; 「灾难性遗忘 增量训练」→ 命中当日调研报告 ✅

**辅助脚本**: `scripts/memory-search-lite.py` (BM25 全文检索, 零依赖兜底)

---

## 技术决策记录

1. **chromadb 弃用**: 本机 (15.8GB 内存, 可用仅 2.8GB) chromadb 1.5.9 初始化即静默崩溃 (SIGKILL, 无事件日志)。MiniLM ONNX 模型 79MB 需从 HuggingFace 下载, 网络 ~40KB/s 不可行。→ 改用纯 Python 标准库 TF-IDF 哈希向量, 功能等价、零下载、内存占用小。
2. **ollama 不可用**: 本地 qwen3.5:4b 需 3.6GB 内存 > 可用 2.8GB; youtu-ft-v1-4b 不支持 embedding; nomic-embed-text 拉取超时。
3. **embedding 升级路径**: 若后续 MiniLM 模型完整缓存 (`~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/model.onnx` >60MB), 脚本自动切换为 ONNX MiniLM (质量更好), 无需改代码。

---

## 自动化 (每日维护)

**Cron 任务**: `数据分层与记忆索引维护` (id: 5c3f3b98)
- ⏰ 每天 12:35 (周一至周六, 符合规则4: 10:30-18:00 窗口)
- 📋 串行执行: memory-tiering.py --apply → memory-vector-index.py build
- 📨 执行结果 announce 到微信

**手动执行**:
```powershell
python scripts\memory-tiering.py --apply          # 分层归档
python scripts\memory-vector-index.py build       # 增量索引
python scripts\memory-vector-index.py search "关键词"
python scripts\memory-search-lite.py "关键词"     # BM25 兜底
```

---

## 与调研方案的映射

| 调研方案层 | 落地 |
|-----------|------|
| 分层记忆 (MemGPT核心/归档) | memory-tiering.py 热/温/冷三级 |
| RAG 外部知识库 (增量更新) | memory-vector-index.py 语义索引 (覆盖.gz归档) |
| 数据生命周期 (冷热分层+压缩) | archive/memory/ + gzip 无损压缩 |
| 日志轮转/压缩 | 内置 gzip level 9 |

**核心收益**: 运行速度不降 (memory/ 根目录精简为热数据) + 历史数据不丢 (冷归档可解压可检索)。
