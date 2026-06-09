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

## 📋 自动任务时间限制规则 (2026-06-09 更新)

**规则内容**: 所有自动任务时间必须在周一至周六,10:20-18:00之间。

### 规则详情
1. **时间范围**: 周一至周六(工作日+周六)
2. **时间限制**: 必须在10:20-18:00之间执行
3. **禁止时间**: 禁止在周日执行
4. **间隔要求**: 任务间隔30分钟左右,任务过多时可适当压缩

### 执行标准
1. 所有Cron任务必须设置在周一至周六
2. 所有Cron任务必须在10:20-18:00之间执行
3. 检查现有任务,不符合的必须立即修改
4. 创建新任务时,必须遵循此时间限制和间隔要求

### 底层规则说明
- 这是底层规则,所有任务调度都必须遵循
- 在创建或修改Cron任务时,必须检查是否符合此规则
- 如果任务时间不符合,必须立即修改

### 当前15个任务时间表 (2026-06-09 13:20 合并后)
| 任务名称 | 执行时间 | 说明 |
|----------|---------|------|
| Memory Dreaming Promotion | 每日10:20 | 从03:00迁移 |
| 每日监控任务 | 每日10:30 | 从10:55调整 |
| 1688全面分析 | 每日11:00 | 从11:05微调 |
| 学术论文与知识库周度同步 | 周一11:10 | 原论文追踪+IMA同步合并 |
| QClaw智能清理 | 周一11:30 | 被合并任务包围 |
| QClaw自进化每周运行(含CPE) | 周一12:00 | Phase 4新增CPE退化检查 |
| QClaw知识库每周整理 | 周一12:30 | 从11:35调整 |
| 智能全景管理 | 周一13:00 | 从12:00调整 |
| tech-breakthrough-monitor | 每日13:30 | 不变 |
| 实时监控任务 | 每日14:00 | 从14:45提前 |
| OpenClaw违规检查 | 周一14:30 | 从16:05调整 |
| 商业智能周报 | 周五15:00 | 从16:00提前 |
| 每周任务执行分析 | 周一15:00 | 从16:35提前 |
| 每日任务监督 | 每日15:30 | 从16:00提前 |
| 自动同步任务文件到GitHub | 每日16:30 | 从17:50提前 |

### 验证结果
- ✅ 所有15个任务的执行时间都符合"周一至周六,10:20-18:00"的要求
- ✅ 所有任务delivery配置正确(mode="announce", channel="wechat-access", to="last")
- ✅ 合并后删除3个、新增1个，净减2个任务
- ✅ 周一密集度从14个时槽→11个时槽
- ✅ CPE退化监控已并入自进化每周运行(Phase 4)

---

*规则最后更新时间: 2026-06-09 13:20*
*规则变更: 合并学术论文+IMA同步→周度同步；CPE并入自进化周运行；总任务17→15*
*规则执行标准: 所有Cron任务必须遵循此时间限制*

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

