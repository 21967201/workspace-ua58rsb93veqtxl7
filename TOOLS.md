# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics - the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 📋 自动任务时间限制规则 (2026-06-22 更新)

**规则内容**: 所有自动任务时间必须在周一至周六,10:30-18:00之间，间隔40分钟以上。

### 规则详情
1. **时间范围**: 周一至周六(工作日+周六)
2. **时间限制**: 必须在10:30-18:00之间执行
3. **禁止时间**: 禁止在周日执行
4. **间隔要求**: 任务间隔至少40分钟以上

### 执行标准
1. 所有Cron任务必须设置在周一至周六
2. 所有Cron任务必须在10:20-18:00之间执行
3. 检查现有任务,不符合的必须立即修改
4. 创建新任务时,必须遵循此时间限制和间隔要求

### 底层规则说明
- 这是底层规则,所有任务调度都必须遵循
- 在创建或修改Cron任务时,必须检查是否符合此规则
- 如果任务时间不符合,必须立即修改

### 当前12个任务时间表 (2026-06-22 调整)
**每天（周一至周六）**:
| 时间 | 任务名称 | 说明 |
|------|---------|------|
| 10:30 | 每日监控任务 | 每日执行 |
| 11:10 | Memory Dreaming Promotion | 每日执行（从03:39调整）|
| 11:50 | tech-breakthrough-monitor | 每日执行（从13:30调整）|
| 12:30 | 自动同步任务文件到GitHub | 每日执行（从16:30调整）|
| 13:10 | 月度报告任务 | 每日执行（从17:15调整）|

**周一额外任务**:
| 时间 | 任务名称 | 说明 |
|------|---------|------|
| 14:00 | 周一知识管理综合任务 | 每周一执行（从13:00调整）|
| 14:40 | 周一综合检查任务 | 每周一执行（从14:30调整）|
| 15:20 | AI系统自动进化任务 | 每周一执行（从16:00调整）|
| 16:00 | Dream 记忆整理 | 每周一执行（从周日03:00调整）|
| 16:40 | QClaw智能清理 | 每周一执行（从17:00调整）|
| 17:20 | Distill 工作流发现 | 每月第一个周一（从03:00调整）|

**周五额外任务**:
| 时间 | 任务名称 | 说明 |
|------|---------|------|
| 15:00 | 商业智能周报 | 每周五执行（从15:50调整）|

### 验证结果
- ✅ 所有12个任务的执行时间都符合"周一至周六,10:30-18:00"的要求
- ✅ 所有任务间隔都≥40分钟
- ✅ 所有任务都不在周日执行
- ✅ 所有任务delivery配置正确(mode="announce", channel="wechat-access", to="last")
- ✅ Dream 记忆整理从周日调整到周一
- ✅ Distill 工作流发现从每月1日调整到每月第一个周一

---

*规则最后更新时间: 2026-06-22 11:30*
*规则变更: 调整时段为10:30-18:00，间隔≥40分钟，总任务12个*
*规则执行标准: 所有Cron任务必须遵循此时段和间隔要求*

## 📋 Token与推理效率规则(2026-06-09 新增v2)

### 推理Token预算表
| 任务类型 | Token预算 | 策略 | 判断标准 |
|----------|-----------|------|---------|
| 简单查询 | 0推理token | **直答** | 事实性查询,无需推理 |
| 中等推理 | ≤7.6%原始CoT | **CoD草稿链** | 需要多步但不需深度推理 |
| 复杂推理 | ≤15%原始CoT | **精简推理+TokenSkip** | 跨Agent/多步骤/代码生成 |
| 关键决策 | ≤15%原始CoT | **多视角验证+精简推理** | 涉及资金/数据/权限/对外发布 |

### 推理优先级
1. 先评估复杂度 → 选择最省token推理策略
2. 简单任务直答,不触发任何推理链
3. 中等任务用3-5步草稿链
4. 关键决策用reasoning-personas切换2+视角验证
5. 每个结论标注置信度(🔴高/🟡中/🟢低)

### 技术突破自动集成规则
**P0级**(兼容≥7+收益≥7+成本≤3)→自动集成,24h内完成
- headroom: Token压缩60-95%,97%精度,CCR可逆压缩,MCP模式集成
- DECS(ICLR 2026 Oral): 推理token减50%,prompt工程嵌入
- AbstractCoT(IBM): 推理token减90%+,抽象符号推理,需模型支持

**P1级**(收益≥6)→本周评估
- LCPO(CMU): 长度控制策略优化
- MOSS: 源码级自我进化
- Self-Evolving Survey: 理论框架
- LongAttnComp: 跨家族上下文压缩

**P2级**→月度汇总
- CoT熵动力学: 智能推理截断
- BadThink(AAAI 2026): 推理安全防御

### 执行标准
1. 每次技术突破监控发现P0/P1突破后,必须检查相关自动任务是否需要更新
2. 新技术兼容≥7+收益≥7+成本≤3→自动更新相关任务配置
3. 每周一自进化报告必须包含「任务与技术同步状态」
4. 创建新自动任务前,必须搜索当前最新技术方案

---

*规则添加时间: 2026-06-09 v2*
*规则集成来源: ICLR 2026 Oral(DECS) + Headroom(v2) + IBM(AbstractCoT) + CMU(LCPO) + SambaNova(LongAttnComp)*

---

## 📋 自动任务与技术突破同步规则（2026-06-09 新增）

**核心原则**: 所有自动任务必须与网络技术更新、突破保持同步更新。

### 执行标准
1. **技术突破→任务更新**：每次技术突破监控发现P0/P1级突破后，必须检查是否有相关自动任务需要更新
2. **自动评估**：新技术的兼容性(≥7) + 收益(≥7) + 成本(≤3) → 自动更新相关任务配置
3. **每周同步**：每周一自进化报告必须包含「任务与技术同步状态」
4. **新任务创建**：创建新自动任务前，必须搜索当前最新技术方案而非使用过时方案

### 同步触发条件
| 触发源 | 同步动作 | 频次 |
|--------|----------|------|
| 技术突破监控(P0) | 立即更新相关任务payload/配置 | 监控到即执行 |
| 技术突破监控(P1高收益) | 24小时内评估并更新 | 日检 |
| 每周自进化 | 生成任务同步报告 | 每周一 |
| 用户主动指令 | 即时执行 | 按需 |

### 同步检查清单
每次触发任务同步时，检查以下维度：
- □ 任务使用的工具/API版本是否最新？
- □ 任务prompt中的技术方案是否被新突破替代？
- □ 任务调度策略是否有更优方案？
- □ 任务输出格式是否需适配新标准？

---

*规则添加时间: 2026-06-09*
*规则添加原因: 用户要求自动任务必须和网络技术更新突破保持同步*

---

## 📋 sessions_spawn 标准参数模板 (2026-06-29 新增)

**规则内容**: 所有 `sessions_spawn` 调用必须遵循标准参数模板，防止Token预算超时。

### 标准模板

```json
{
  "task": "<任务描述>"
  // 必填: 清晰、具体的任务描述
  
  "token_budget": 100000,
  // 必填: Token预算，默认100000（约10万token）
  // 简单任务: 50000
  // 中等任务: 100000
  // 复杂任务: 200000
  
  "runtime": "subagent",
  // 必填: 必须使用subagent运行时
  
  "context": "isolated",
  // 推荐: 默认isolated（干净环境）
  // 特殊情况: 需要当前对话上下文时才用"fork"
  
  "cleanup": "delete",
  // 推荐: 任务完成后自动删除会话，节省资源
  
  "label": "<task-name>",
  // 可选: 任务标签，便于后续查询
  
  "thinking": null,
  // 可选: 覆盖默认thinking配置
  
  "model": null,
  // 可选: 覆盖默认model配置
}
```

### 参数说明

#### 1. token_budget (必填)
- **默认值**: 100000
- **简单任务** (单一操作，如文件读取): 50000
- **中等任务** (多步骤，如代码生成+测试): 100000
- **复杂任务** (跨多个系统，如全栈部署): 200000
- **禁止**: 不设置token_budget参数（会导致默认值可能不足）

#### 2. context (推荐明确设置)
- **isolated**: 默认推荐，干净环境，无历史包袱
- **fork**: 仅当子任务**必须**访问当前对话历史时才使用
- **风险**: fork会继承当前session的所有历史和token消耗

#### 3. cleanup (推荐"delete")
- **delete**: 任务完成后自动删除会话，节省资源
- **keep**: 需要调试或查看详细过程时保留

#### 4. 任务拆分原则
- 如果task描述超过3个步骤 → 拆分为多个sessions_spawn
- 如果每个步骤都可能超过50000 token → 必须拆分
- 拆分后，每个子任务应该≤3个明确步骤

### 错误示例与修正

#### ❌ 错误示例1: 缺少token_budget
```json
{
  "task": "分析整个代码库的架构模式",
  "runtime": "subagent"
}
```
**问题**: 复杂任务可能超过默认token预算
**修正**: 添加 `"token_budget": 200000`

#### ❌ 错误示例2: context使用fork但无必要
```json
{
  "task": "计算1+1",
  "context": "fork",
  "token_budget": 50000
}
```
**问题**: 简单任务不需要继承对话历史，浪费token
**修正**: 改为 `"context": "isolated"`

#### ❌ 错误示例3: 任务过于复杂未拆分
```json
{
  "task": "1. 分析代码库 2. 生成架构图 3. 写文档 4. 部署到服务器",
  "token_budget": 100000
}
```
**问题**: 4个步骤可能超过预算，且难以调试
**修正**: 拆分为4个独立的sessions_spawn调用

### 正确示例

#### ✅ 简单任务
```json
{
  "task": "读取 package.json 并提取所有依赖",
  "token_budget": 50000,
  "runtime": "subagent",
  "context": "isolated",
  "cleanup": "delete"
}
```

#### ✅ 中等任务
```json
{
  "task": "为 openclaw-evolution-researcher 技能生成技术突破监控报告",
  "token_budget": 100000,
  "runtime": "subagent",
  "context": "isolated",
  "cleanup": "delete",
  "label": "tech-breakthrough-report"
}
```

#### ✅ 复杂任务（拆分为多个）
```json
// 任务1: 数据分析
{
  "task": "分析 logs/ 目录下所有日志文件，提取错误模式",
  "token_budget": 100000,
  "runtime": "subagent",
  "context": "isolated",
  "cleanup": "delete",
  "label": "log-analysis"
}

// 任务2: 报告生成（等待任务1完成）
{
  "task": "基于错误模式分析，生成改进建议报告",
  "token_budget": 100000,
  "runtime": "subagent",
  "context": "isolated",
  "cleanup": "delete",
  "label": "improvement-report"
}
```

### 实施检查清单

每次调用 `sessions_spawn` 前，检查：
- [ ] token_budget 参数已设置（推荐100000）
- [ ] context 明确设置为 "isolated" 或 "fork"（后者仅在必要时）
- [ ] cleanup 设置为 "delete"（除非需要调试）
- [ ] 任务描述≤3个步骤（否则拆分）
- [ ] 如果任务可能超过50000 token，已增加token_budget

### 违规处理

- **轻度违规**: 未设置token_budget但任务成功 → 记录到 `memory/failures/` 作为警告
- **重度违规**: 未设置token_budget导致任务超时 → 记录到 `self-improving/corrections.md` 并更新 `memory/patterns.md`

**违反此规则 = 严重失职。**

---

*规则添加时间: 2026-06-29*
*规则添加原因: 防止子任务Token预算超时，提高任务完成率*

