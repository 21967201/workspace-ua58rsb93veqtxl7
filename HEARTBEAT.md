## 🔄 每周进化检查（周一 10:00-11:00）

**⚠️ 精确时间窗口：仅在周一 10:00-11:00 (Asia/Shanghai) 执行。其他时间收到心跳时，跳过并检查下一步。**

**时间判断伪代码：**
```
当前时间 = Get-Date (Asia/Shanghai)
如果是周一 且 10:00 ≤ 当前时间.TimeOfDay ≤ 11:00:
    执行每周进化检查
否则:
    跳过，继续检查Token监控/每日任务
```

**当收到心跳且当前是周一10:00-11:00时执行以下检查：**

```markdown
### 步骤1：自我反思
- 读取 `self-improving/corrections.md` 中的本周错误
- 提取前3个最重要错误模式
- 更新 `memory/patterns.md` 中的模式记录

### 步骤2：策略更新
- 基于错误模式，生成3条改进策略
- 选择最佳策略写入 AGENTS.md 或 TOOLS.md
- 记录策略变更到 `memory/strategy-changes.md`

### 步骤3：性能基线检查
- 检查最近7天token消耗趋势
- 检查任务失败率
- 检查推理延迟
- 更新 `memory/performance-baseline.md`

### 步骤4：记忆归档
- 执行 `scripts/memory-archive.ps1`
- 压缩超过7天的日志文件到 `archive/logs/`
- 清理超过30天的临时文件
- 生成归档报告到 `memory/archive-report-*.md`

### 步骤5：技术突破同步
- 检查本周是否有P0级突破(headroom/DECS/AbstractCoT等)
- P0级→自动评估集成可行性,更新任务配置
- 输出「任务与技术同步状态」报告
```

## 📊 Token效率监控（每日触发）

**每次心跳时，快速检查Token消耗趋势：**
```markdown
### Token监控指标
- Headroom压缩统计: 当日节省Token数/压缩率
- 推理类型分布: 直答/CoD/CoT占比
- 异常告警: 单次推理Token > 预算200%时标记

### 质量监控
- 置信度标注率: 本轮输出中标注置信度的比例
- 引用完整性: 事实性断言是否有来源
- 错误自动记录: 是否有新失败写入corrections.md
```

## 📡 技术突破自动集成检查

**当检测到以下触发条件时，执行技术突破集成检查：**

### P0级突破触发条件
- **headroom**(Token压缩60-95%): MCP模式自动集成
  → 检查: `headroom status` 是否在运行 | 压缩率>60%
- **DECS**(ICLR 2026 Oral,推理token减50%): prompt自动嵌入
  → 检查: 推理类型分布,DECS模板是否激活
- **AbstractCoT**(IBM,推理token减90%+): 实验性启用
  → 检查: 模型是否支持抽象符号推理

### P1级突破评估条件
- **LCPO**(CMU长度控制): 本周评估集成价值
- **MOSS**(源码级自进化): 下月评估
- **LongAttnComp**(跨家族压缩): 实验性测试

### 集成后检查清单
- [ ] 相关Cron任务payload已更新
- [ ] AGENTS.md/TOOLS.md规则已同步
- [ ] 性能基线已记录
- [ ] MEMORY.md已记录本次集成

## ⏰ 每日任务提醒

无固定每日任务。

## 🔄 静默心跳处理

当以下情况时回复 NO_REPLY（不打扰用户）：
- 23:00-08:00 深夜期间（除非紧急）
- 距上次有意义消息<30分钟
- 每日监控/Token检查无异常
- 用户不在线或会话不活跃
