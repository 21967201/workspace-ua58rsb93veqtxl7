# QClaw 原生知识库 - 混合方案

## 🎯 设计理念

**三层知识架构**，各司其职，协同工作：

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Memory System (日常知识)                      │
│  - MEMORY.md (核心记忆)                                │
│  - memory/YYYY-MM-DD.md (每日日志)                    │
│  - 语义搜索: memory_search                            │
└─────────────────────────────────────────────────────────┘
                         ↓ 协同
┌─────────────────────────────────────────────────────────┐
│  Layer 2: LCM (对话历史)                              │
│  - 自动捕获重要对话                                    │
│  - 压缩存储: lcm_grep, lcm_expand, lcm_describe    │
│  - 回溯历史决策                                        │
└─────────────────────────────────────────────────────────┘
                         ↓ 提取
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Custom KB (结构化知识)                       │
│  - kb/ 目录分类存储                                    │
│  - 人物/项目/技术/决策                                 │
│  - 跨库搜索: memory_search(corpus: "all")           │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 目录结构

```
D:\QClawX\data\workspace-ua58rsb93veqtxl7\
├── MEMORY.md                    # 核心记忆索引
├── memory\                     # Layer 1: 日常记忆
│   ├── YYYY-MM-DD.md          # 每日日志
│   ├── people\                # 人物知识库
│   │   └── *.md
│   ├── projects\              # 项目知识库
│   │   └── *.md
│   ├── tech\                  # 技术知识库
│   │   └── *.md
│   └── decisions\            # 决策记录
│       └── *.md
├── kb\                        # Layer 3: 结构化知识库
│   ├── people\                # 人物档案
│   │   └── *.md
│   ├── projects\              # 项目文档
│   │   └── *.md
│   ├── tech\                  # 技术文档
│   │   └── *.md
│   ├── ai-breakthrough\      # AI技术突破
│   │   └── YYYY-MM-DD.md
│   └── decisions\            # 重要决策
│       └── YYYY-MM-DD-*.md
└── lcm\                       # Layer 2: LCM管理(自动)
    └── (由QClaw自动管理)
```

---

## 🔧 使用指南

### Layer 1: Memory System (日常知识)

**写入场景**：
- 用户提到人物/项目/技术 → 自动记录到 `memory/people/*.md` 等
- 每日工作日志 → 自动生成 `memory/YYYY-MM-DD.md`
- 重要决策 → 记录到 `memory/decisions/*.md`

**搜索命令**：
```powershell
# 语义搜索 Memory System
memory_search --query="人物名/项目名/技术关键词"

# 精确读取
memory_get --path="memory/people/张三.md"
```

---

### Layer 2: LCM (对话历史)

**自动捕获**：
- 重要对话自动压缩存储
- 支持正则表达式和全文搜索

**搜索命令**：
```powershell
# 搜索历史对话
lcm_grep --pattern="项目名" --mode="full_text"

# 扩展压缩摘要
lcm_expand --summaryIds=@("sum_xxx")

# 查看条目详情
lcm_describe --id="sum_xxx"
```

---

### Layer 3: Custom KB (结构化知识)

**手动整理**：
- 从 Layer 1 和 Layer 2 提取重要知识
- 结构化存储到 `kb/` 目录

**搜索命令**：
```powershell
# 跨库搜索 (Memory + KB)
memory_search --query="关键词" --corpus="all"

# 读取KB文件
read --path="kb/tech/ai-breakthrough.md"
```

---

## 🔄 知识流转工作流

### 每日自动流程
```
用户对话
  ↓
[自动捕获] → memory/YYYY-MM-DD.md (每日日志)
  ↓
[重要信息] → memory/people/*.md (人物)
  ↓
[项目进展] → memory/projects/*.md (项目)
  ↓
[技术笔记] → memory/tech/*.md (技术)
  ↓
[决策记录] → memory/decisions/*.md (决策)
```

### 每周整理流程 (周一执行)
```
memory/*.md (日常记录)
  ↓
[提取重要知识] → kb/*.md (结构化知识)
  ↓
[更新索引] → MEMORY.md (核心索引)
  ↓
[搜索验证] → memory_search(corpus: "all")
```

### 搜索流程
```
用户提问: "张三负责什么项目?"
  ↓
[Layer 1] memory_search --query="张三"
  ↓ (未找到)
[Layer 2] lcm_grep --pattern="张三"
  ↓ (未找到)
[Layer 3] memory_search --query="张三" --corpus="all"
  ↓
返回结果 → 综合回答
```

---

## 📝 模板文件

### kb/people/模板.md
```markdown
# 人物姓名

## 基本信息
- 职位: 
- 公司: 
- 联系方式: 

## 项目经历
- 项目名称: 
  - 角色: 
  - 时间: 
  - 贡献: 

## 技术栈
- 

## 备注
-
```

### kb/projects/模板.md
```markdown
# 项目名称

## 项目信息
- 开始时间: 
- 结束时间: 
- 状态: 进行中/已完成/已暂停

## 团队成员
- 负责人: 
- 成员: 

## 技术栈
- 

## 重要决策
- YYYY-MM-DD: 决策内容

## 备注
-
```

### kb/tech/模板.md
```markdown
# 技术名称

## 技术概述

## 使用场景

## 代码示例

## 参考资源
- 

## 备注
-
```

---

## 🚀 快速开始

### 1. 创建目录结构
```powershell
cd D:\QClawX\data\workspace-ua58rsb93veqtxl7
New-Item -ItemType Directory -Path "kb\people", "kb\projects", "kb\tech", "kb\ai-breakthrough", "kb\decisions"
New-Item -ItemType Directory -Path "memory\people", "memory\projects", "memory\tech", "memory\decisions"
```

### 2. 创建模板文件
```powershell
# 复制本文件中的模板内容到对应文件
```

### 3. 更新 MEMORY.md
在 MEMORY.md 中添加知识库索引章节

### 4. 测试搜索
```powershell
memory_search --query="测试"
```

---

## 🔗 相关工具

| 工具 | 用途 | 适用层级 |
|------|------|----------|
| `memory_search` | 语义搜索 | Layer 1 + 3 |
| `memory_get` | 精确读取 | Layer 1 + 3 |
| `lcm_grep` | 搜索对话历史 | Layer 2 |
| `lcm_expand` | 扩展压缩摘要 | Layer 2 |
| `lcm_describe` | 查看LCM条目 | Layer 2 |
| `read` | 读取文件 | Layer 1 + 3 |
| `write` | 写入文件 | Layer 1 + 3 |
| `edit` | 编辑文件 | Layer 1 + 3 |

---

## ✅ 实施清单

- [ ] 创建目录结构
- [ ] 创建模板文件
- [ ] 更新 MEMORY.md 索引
- [ ] 配置自动捕获规则
- [ ] 测试搜索功能
- [ ] 编写每周整理脚本
- [ ] 文档化工作流程

---

**创建时间**: 2026-06-01  
**版本**: v1.0  
**状态**: 实施中
