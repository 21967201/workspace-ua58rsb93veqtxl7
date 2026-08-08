# 2026-08-08 会话数据丢失修复

## 事件
用户报 QClaw 前端"轩恒"会话数据丢失（8/5 后会话显示为空）。

## 根因（三阶段排查）
1. **三条 Hermes 数据线混淆**：`.hermes`（CLI/cron，8/5-8/7 修的）≠ `.qclaw-hermes`（QClaw 前端真正数据源）
2. **audit.db 写入停止**：8/4 16:22 后 `.qclaw-hermes` 内置 Hermes 不再写 audit.db
3. **8/8 10:07 QClaw 自动状态合并 bug**：merge 把 state.db → audit.db 只迁移了部分（59/156 会话），97 个会话 3219 条消息未同步；agent.json 从 208 → 153 → 60（polluted）→ 155 波动

## 关键发现
- **数据没丢**：`.qclaw-hermes\state.db` = 156 会话 / 11709 消息（完整历史 6/8-8/8）
- **隐藏目录**：`D:\HermesX\hermes-data` = 旧 Hermes 迁移目录（7/23），state.db 21MB/62 会话
- 老会话示例：HermesX Workspace Configuration (221条)、WorkBuddyX项目学习 (161条)、Hermes Agent v0.17.0 (181条)、今日头条AI Agent趋势 (56条) 全部完好

## 修复
- 备份 audit.db → `audit.db.bak-20260808-113750`
- 执行 `migrate_state_to_audit.py`：97 会话 / 3219 消息 从 state.db 同步到 audit.db
- 结果：audit_messages 59→156 会话，4467→7686 消息 ✅

## 验证
- 关键老会话消息数全部恢复
- agent.json (155) vs audit.db (156) 基本对齐
- 最新消息 8/8 11:38 正常写入（audit 恢复工作）

## 未决
- audit.db 8/4 停写的根因（配置 vs bug）
- agent.json polluted (60) 事件原因
- tui_gateway _drain_stderr GBK crash（非致命）

## 脚本
- `migrate_state_to_audit.py`（修复主脚本，可重复执行，幂等）
- 其他排查脚本：compare_agent_jsons.py / check_qclaw_hermes_state.py / check_state_db_detail.py / verify_audit_sync.py / check_agent_audit_match.py
- 报告：`hermes-session-loss-fix_2026-08-08.md`
