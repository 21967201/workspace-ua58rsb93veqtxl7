# QClaw 原生知识库 - 自动捕获规则

## 🎯 目标

当用户对话中出现特定信息时，自动捕获到 `memory/` 对应目录。

---

## 📋 捕获规则

### 1. 人物信息捕获
**触发条件** (出现以下任一关键词):
- 人名（中文名、英文名）
- "同事"、"朋友"、"家人"、"团队成员"
- "联系"、"电话"、"邮箱"、"微信"

**捕获动作**:
```
保存到: memory/people/YYYY-MM-DD-人物名.md
内容格式:
- 姓名: 
- 关系: 同事/朋友/家人/其他
- 上下文: [对话摘要]
- 联系方式: (如有)
- 备注: 
```

**示例**:
```
用户: "张三今天帮我解决了服务器问题"
→ 捕获到 memory/people/2026-06-01-张三.md
```

---

### 2. 项目信息捕获
**触发条件**:
- "项目"、"任务"、"工作"、"需求"
- "开始"、"完成"、"交付"、"上线"
- "进度"、"里程碑"、"截止日期"

**捕获动作**:
```
保存到: memory/projects/YYYY-MM-DD-项目名.md
内容格式:
- 项目名称: 
- 状态: 进行中/已完成/已暂停
- 关键进展: [对话摘要]
- 相关人员: 
- 备注: 
```

**示例**:
```
用户: "GBrain全景管理项目今天完成了步骤1-3"
→ 捕获到 memory/projects/2026-06-01-gbrain全景管理.md
```

---

### 3. 技术信息捕获
**触发条件**:
- 技术名词（Python、React、AI、API等）
- "学习"、"研究"、"尝试"、"使用"
- "框架"、"工具"、"库"、"平台"

**捕获动作**:
```
保存到: memory/tech/YYYY-MM-DD-技术名.md
内容格式:
- 技术名称: 
- 使用场景: 
- 关键发现: [对话摘要]
- 参考资源: 
- 备注: 
```

**示例**:
```
用户: "今天学习了GBrain的知识库管理功能"
→ 捕获到 memory/tech/2026-06-01-gbrain.md
```

---

### 4. 决策信息捕获
**触发条件**:
- "决定"、"选择"、"方案"、"权衡"
- "放弃"、"采用"、"优化"、"改进"
- "原因"、"考虑"、"评估"

**捕获动作**:
```
保存到: memory/decisions/YYYY-MM-DD-决策主题.md
内容格式:
- 决策主题: 
- 可选方案: 
- 最终选择: 
- 决策原因: [对话摘要]
- 后续行动: 
```

**示例**:
```
用户: "决定采用QClaw原生知识库方案，而不是GBrain"
→ 捕获到 memory/decisions/2026-06-01-知识库方案选择.md
```

---

### 5. AI技术突破捕获 (每周一自动)
**触发条件**:
- 周一执行 AI技术突破信息更新 任务时
- 搜索结果中包含重要技术进展

**捕获动作**:
```
保存到: kb/ai-breakthrough/YYYY-MM-DD.md
内容格式: 参考 ai-tech-breakthrough-YYYYMMDD.md 模板
```

---

## 🔄 自动捕获工作流

```
用户对话
  ↓
[Agent 检测关键词]
  ↓
[匹配捕获规则]
  ↓
[生成结构化笔记]
  ↓
[保存到 memory/对应目录]
  ↓
[每周一整理到 kb/]
```

---

## 📝 实施方法

### 方法1: Agent 主动检测 (推荐)
在每次对话中，Agent 主动检测并写入：

```python
# 伪代码示例
def detect_and_capture(user_message):
    # 检测人物信息
    if contains_person_name(user_message):
        save_to_memory("people", extract_person_info(user_message))
    
    # 检测项目信息
    if contains_project_keywords(user_message):
        save_to_memory("projects", extract_project_info(user_message))
    
    # 检测技术信息
    if contains_tech_keywords(user_message):
        save_to_memory("tech", extract_tech_info(user_message))
    
    # 检测决策信息
    if contains_decision_keywords(user_message):
        save_to_memory("decisions", extract_decision_info(user_message))
```

### 方法2: 定时任务扫描
创建定时任务，每天扫描对话历史并提取：

```powershell
# 每天23:00执行
# 扫描今天的对话，提取重要信息到 memory/
```

---

## ⚙️ 配置示例

在 `AGENTS.md` 中添加：

```markdown
## 📝 自动捕获规则

每次对话中，主动检测并记录：
1. **人物信息** → `memory/people/YYYY-MM-DD-人物名.md`
2. **项目信息** → `memory/projects/YYYY-MM-DD-项目名.md`
3. **技术信息** → `memory/tech/YYYY-MM-DD-技术名.md`
4. **决策信息** → `memory/decisions/YYYY-MM-DD-决策主题.md`

**捕获时机**:
- 用户提到人名、项目名称、技术名词时立即捕获
- 每天23:00扫描今日对话，补充捕获遗漏信息
- 每周一将重要信息从 `memory/` 迁移到 `kb/`
```

---

## 🔗 相关文件

- 捕获规则配置: `kb/auto_capture_rules.md` (本文件)
- 每周整理脚本: `kb/weekly_organize.py`
- 搜索脚本: `kb/search.ps1`

---

**创建时间**: 2026-06-01  
**版本**: v1.0  
**状态**: 待集成到 Agent
