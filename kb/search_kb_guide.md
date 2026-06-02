# QClaw 原生知识库 - 混合搜索脚本

## 功能
模拟跨库搜索：同时搜索 `memory/` 和 `kb/` 目录

## 使用方法

```powershell
# 基本搜索
.\search_kb.ps1 -Query "AI技术"

# 搜索特定分类
.\search_kb.ps1 -Query "张三" -Category "people"

# 搜索多个分类
.\search_kb.ps1 -Query "项目" -Category "projects,tech"
```

## 搜索范围

| 目录 | 内容 | 搜索方式 |
|------|------|----------|
| `memory/*.md` | 每日日志、人物、项目、技术笔记 | `memory_search` 工具 |
| `kb/*.md` | 结构化知识库 | `Select-String` (PowerShell) |
| `MEMORY.md` | 核心记忆索引 | `memory_search` 工具 |

## 实现原理

1. **Layer 1 + 3 搜索**：调用 `memory_search` 搜索 `memory/` 和 `MEMORY.md`
2. **Layer 3 补充搜索**：用 `Select-String` 搜索 `kb/` 目录
3. **结果合并**：去重后返回统一格式

## 限制

- `kb/` 目录使用**关键词搜索** (Select-String)，不是语义搜索
- `memory/` 目录使用**语义搜索** (memory_search)，效果更好
- 未来可以将 `kb/` 重要内容定期合并到 `memory/` 以实现统一语义搜索

## 定期维护任务 (每周一执行)

1. **提取重要知识**：从 `memory/*.md` 提取重要信息到 `kb/*.md`
2. **更新索引**：更新 `MEMORY.md` 中的知识库索引
3. **清理过期内容**：归档或删除 `memory/*.md` 中的临时内容
