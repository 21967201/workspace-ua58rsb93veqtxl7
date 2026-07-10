# 每日技术突破监控（轻量循环）

## 概述
每日定时执行的**轻量级**前沿技术突破监控循环。与 `openclaw-evolution-researcher`（按需触发、生成 10 份深度研究文档）不同，本 skill 专注于**每日快速巡检**：搜索 → 评估 → 静默更新记忆 → 仅当发现 P0/P1 时推送通知。

**模式来源（Distill 复扫实证）：**
- 历史 session 复扫出现 **5 次**（2026-06-17 ~ 2026-07-04），`技术突破监控` / `技术监控` 标题
- 置信度：0.92（高频、步骤清晰、通用、不绑定特定项目）

## 适用场景
- Cron 每日定时（如 06:00）自动巡检 arXiv / GitHub / 技术社区
- 需要持续跟踪一组**固定监控对象**（竞品/依赖库）的更新
- 与重型研究 skill 配合：本 skill 做日常雷达，发现重要目标再触发 `openclaw-evolution-researcher` 深度研究

## 监控对象（可在 frontmatter 或调用时覆盖）
- 论文源：arXiv（关键词如 Self-Evolving Agents、Token Compression、Agent Orchestration）
- 项目源：OpenClaw、Goose Agent、Hermes、Lean-ctx 等
- 社区源：美团觅游 Agent 社区、华为 ArkAF、技术博客

## 工作流步骤

### 1. 三阶段搜索
- **阶段A**：arXiv 论文搜索（按固定关键词集合，检查新提交/引用）
- **阶段B**：GitHub 项目状态检查（star/commit/release/issue 变动）
- **阶段C**：技术社区/博客扫描

### 2. 评估（51 指标评估体系）
- 对每个发现按 **P0 / P1 / P2** 分级：
  - **P0**（兼容≥7 + 收益≥7 + 成本≤3）：立即推送通知，24h 内评估集成
  - **P1**（收益≥6）：记入待办，本周评估
  - **P2**：仅静默入库记忆，不推送
- 综合评分 0-10（兼容性 / 收益 / 成本反向）

### 3. 静默更新记忆系统
- 无 P0/P1 时：写入 `memory/YYYY-MM-DD.md`（当日发现摘要），更新 MEMORY.md 相关条目，**不触发推送**
- 连续 7 天无突破：建议调整监控关键词

### 4. 报告与推送
- 生成工件文件：`tech-breakthrough-monitor_YYYY-MM-DD-HHmm.md`
- 仅当发现 P0/P1 时推送负一屏 / 通知；否则静默完成

## 使用示例

```powershell
# 由 Cron 每日 06:00 触发，无需人工干预
# 伪流程（实际由 Agent 执行搜索+评估）：
#   search -> score(P0/P1/P2) -> if P0/P1: push_notice else silent_memory_update
#   产物: tech-breakthrough-monitor_<date>.md + memory/<date>.md
```

## 与 openclaw-evolution-researcher 的关系
| 维度 | 本 skill（每日监控） | openclaw-evolution-researcher |
|------|----------------------|-------------------------------|
| 触发 | Cron 每日自动 | 按需（人工/发现 P0 后触发） |
| 产出 | 1 份巡检报告 + 记忆更新 | 10 份深度研究文档套件 |
| 目标 | 早发现、持续跟踪 | 深分析、定方案、立项 |

## 注意事项
- 网络搜索失败时应静默重试，不阻塞记忆更新
- 推送配置（负一屏）若未就绪，跳过推送但保留报告文件
- 监控关键词每 30 天由 Distill 任务复盘一次，避免陈旧

## 相关 Skill
- `openclaw-evolution-researcher`（深度研究，P0 触发）
- `memory-writer` / `smart-memory`（记忆静默更新）
- `GitHub同步推送-workflow`（报告归档同步）
