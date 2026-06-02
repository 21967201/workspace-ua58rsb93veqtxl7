# QClaw 原生知识库 - 使用指南

## 🎯 快速开始

### 1. 写入知识

**方法A: 让 Agent 自动捕获**
```
你: "张三今天帮我解决了服务器问题"
Agent: [自动捕获到 memory/people/2026-06-01-张三.md]
```

**方法B: 手动创建文件**
```powershell
# 创建人物笔记
notepad kb\people\张三.md

# 创建项目文档
notepad kb\projects\GBrain全景管理.md

# 创建技术笔记
notepad kb\tech\AI技术突破.md
```

---

## 🔍 搜索知识

### 方法1: 语义搜索 (推荐)
在 QClaw 对话中：
```
你: "搜索张三负责的项目"
Agent: [调用 memory_search 工具]
```

### 方法2: 关键词搜索
```powershell
cd D:\QClawX\data\workspace-ua58rsb93veqtxl7\kb
.\search.ps1 "AI"
```

### 方法3: 直接读取文件
```
你: "读取 kb/tech/ai-test.md"
Agent: [调用 read 工具]
```

---

## 📂 目录结构说明

```
kb/               # 结构化知识库 (长期保存)
├── people\       # 人物档案
├── projects\     # 项目文档
├── tech\         # 技术文档
├── ai-breakthrough\  # AI技术突破记录
└── decisions\    # 重要决策记录

memory/           # 日常记忆 (临时工作区)
├── YYYY-MM-DD.md # 每日日志
├── people\       # 人物信息捕获
├── projects\     # 项目进展捕获
├── tech\        # 技术笔记捕获
└── decisions\   # 决策记录捕获
```

**使用原则**:
- `memory/` → 日常临时记录，每周整理到 `kb/`
- `kb/` → 结构化知识，长期保存

---

## 🔄 每周整理

### 自动整理 (已配置)
每周一自动执行：
1. 扫描 `memory/` 目录 (最近7天)
2. 提取重要知识 (人物/项目/技术/决策)
3. 生成整理报告 (`kb/weekly_organize_report_YYYY-MM-DD.md`)
4. 自动创建知识条目 (如 `kb/ai-breakthrough/YYYY-MM-DD.md`)

### 手动整理
```powershell
cd D:\QClawX\data\workspace-ua58rsb93veqtxl7\kb
python weekly_organize.py
```

---

## 📝 模板使用

### 创建新人物笔记
```powershell
# 复制模板
copy kb\people\模板.md kb\people\张三.md

# 编辑
notepad kb\people\张三.md
```

### 创建新项目文档
```powershell
copy kb\projects\模板.md kb\projects\GBrain全景管理.md
notepad kb\projects\GBrain全景管理.md
```

### 创建新技术笔记
```powershell
copy kb\tech\模板.md kb\tech\AI技术突破.md
notepad kb\tech\AI技术突破.md
```

---

## 🔗 跨库搜索

### 搜索范围
| 工具 | 搜索范围 | 搜索方式 |
|------|----------|----------|
| `memory_search` | `MEMORY.md`, `memory/*.md` | 语义搜索 |
| `search.ps1` | `kb/*.md` | 关键词搜索 |
| `read` | 所有文件 | 精确读取 |

### 最佳实践
1. **先用语义搜索** → `memory_search --query="关键词"`
2. **再用关键词搜索** → `.\search.ps1 "关键词"`
3. **最后精确读取** → `read --path="kb/tech/xxx.md"`

---

## 💡 使用技巧

### 1. 让 Agent 自动记录
```
你: "记住：张三的电话是13800138000"
Agent: [自动保存到 memory/people/张三.md]
```

### 2. 定期回顾知识库
```
你: "本周我学习了哪些技术？"
Agent: [搜索 memory/tech/ 和 kb/tech/]
```

### 3. 决策回顾
```
你: "上次关于知识库方案的决策是什么？"
Agent: [搜索 memory/decisions/ 和 kb/decisions/]
```

### 4. 项目状态查询
```
你: "GBrain全景管理项目进展如何？"
Agent: [搜索 memory/projects/ 和 kb/projects/]
```

---

## 🛠️ 高级功能

### 1. 配置自动捕获
编辑 `AGENTS.md`，添加：
```markdown
## 📝 自动捕获规则

每次对话中，主动检测并记录：
1. **人物信息** → `memory/people/YYYY-MM-DD-人物名.md`
2. **项目信息** → `memory/projects/YYYY-MM-DD-项目名.md`
3. **技术信息** → `memory/tech/YYYY-MM-DD-技术名.md`
4. **决策信息** → `memory/decisions/YYYY-MM-DD-决策主题.md`
```

### 2. 定时任务集成
```
你: "创建一个定时任务，每周一执行知识库整理"
Agent: [创建 cron 任务，调用 weekly_organize.py]
```

### 3. 自定义搜索脚本
编辑 `kb/search.ps1`，添加：
- 正则表达式搜索
- 多关键词组合搜索
- 日期范围过滤

---

## ❓ 常见问题

### Q1: 搜索找不到内容？
**A**: 
1. 检查文件是否在 `kb/` 或 `memory/` 目录
2. 尝试不同的关键词
3. 使用 `memory_search --corpus="all"` 跨库搜索

### Q2: 如何备份知识库？
**A**: 
```powershell
# 备份整个 workspace
xcopy D:\QClawX\data\workspace-ua58rsb93veqtxl7 D:\backup\workspace-backup\ /E /H /C /I
```

### Q3: 如何共享知识库？
**A**: 
- 将 `kb/` 目录同步到云盘 (OneDrive/Google Drive)
- 使用 Git 管理版本控制

---

## 📞 获取帮助

### 在 QClaw 中询问
```
你: "如何使用知识库搜索功能？"
Agent: [提供详细指导]
```

### 查看文档
```powershell
# 查看完整方案说明
notepad kb\README.md

# 查看搜索指南
notepad kb\search_kb_guide.md

# 查看自动捕获规则
notepad kb\auto_capture_rules.md
```

---

**版本**: v1.0  
**更新日期**: 2026-06-01  
**维护者**: QClaw Agent
