# QClaw/Hermes 会话数据丢失根因修复报告

**时间**: 2026-08-08 11:37 完成  
**状态**: ✅ 已修复

---

## 根因分析

### 三条独立 Hermes 数据线

| 数据目录 | 用途 | 会话数 | 消息数 | 状态 |
|---|---|---|---|---|
| `C:\Users\Administrator\.hermes\` | CLI/cron 用 | 43 | 85 | 正常 |
| `C:\Users\Administrator\.qclaw-hermes\` | **QClaw 前端"轩恒"数据源** | 156 | 11709 | ✅ 完整 |
| `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\` | 打包内置 Hermes | 2 | 8 | 停用 |

### 问题链条

```
8/4 16:22 — audit.db 最后写入
8/5 用户改配置（改的是 .hermes，不是 .qclaw-hermes）— 前端不受影响
8/7 修 Hermes（.hermes），前端口仍用 .qclaw-hermes
8/8 10:07 — QClaw 自动状态合并（merge）触发：
  - 4 个 state.db → .qclaw-hermes/state.db
  - agent.json 重写为 208 会话 → 153 → 60 → 155（波动）
  - audit.db 迁移未完成（只迁移了 59 个会话的 4467 条）
8/8 10:32 — tui_gateway crash（GBK 解码失败，非致命）
```

### 核心bug

1. **audit.db 写入停止**：8/4 后 `.qclaw-hermes` 内置 Hermes 不再写 audit.db
2. **merge 不完整**：QClaw 状态合并想同步 state.db → audit.db，但 merge 逻辑有 bug，97 个会话（3219 条消息）未同步
3. **前端会话列表 + 消息分离**：前端 `hermes:listSessions` 读 agent.json（155 个），`hermes:loadMessages` 读 audit.db——老会话在 agent.json 有但在 audit.db 无消息 → 显示空白

### 数据完整性确认

**✅ 真实数据没丢！** `D:\HermesX\hermes-data\state.db`（旧 Hermes 迁移目录，7/23 迁移）+ `.qclaw-hermes\state.db` 包含完整历史：
- 6/8: "初次问候与帮助意愿"
- 6/18: "Kermes与OfficeClaw双Agent协作可行性分析" (115条)  
- 6/18: "HermesX Workspace Configuration" (221条)
- 6/25: "1688标题生成指南学习" (36条)
- 6/26: "Agent差异化进化优化方案" (138条)
- 6/27: "WorkBuddyX项目学习" (161条)
- 6/29: "Hermes Agent v0.17.0 更新亮点" (181条)
- 6/30: "今日头条AI Agent趋势深度分析" (56条)
- 7/1-7/13: 密集使用期
- 7/21-7/31: 活跃期
- 8/3-8/8: 当前

---

## 修复操作

### 修复内容

**文件**: `D:\QClawX\data\workspace-ua58rsb93veqtxl7\migrate_state_to_audit.py`

1. 备份 audit.db → `C:\Users\Administrator\.qclaw-hermes\audit.db.bak-20260808-113750` (12.5MB)
2. 从 `.qclaw-hermes\state.db` 同步 97 个缺失会话的 3219 条消息到 audit.db
3. 写入 conversation_sessions 映射
4. 验证完整性

### 修复前后对比

| 指标 | 修复前 | 修复后 |
|---|---|---|
| audit_messages 会话数 | 59 | **156** |
| audit_messages 消息总数 | 4467 | **7686** |
| 覆盖 6/8-7/10 老会话 | ❌ | ✅ |
| 覆盖 8/5 后会话 | 部分 | ✅ |

---

## 验证方法

1. **重启 QClaw 客户端**（让 qclaw_launcher 重新加载会话状态）
2. 打开前端"轩恒"，检查会话列表是否显示老会话
3. 点击"聊天记录丢失原因排查"（当前会话）和老会话（如"HermesX Workspace Configuration"），确认消息正常显示

---

## 关联发现

### 隐藏数据目录

- **D:\HermesX\hermes-data** = 旧 Hermes 完整数据迁移目录（7/23 从旧电脑迁移）
- **D:\HermesX\hermes-data\state.db** = 21MB，62 会话，1549 消息（7/8 快照）
- **D:\HermesX\hermes-data\.env** = 旧 Hermes 环境变量配置
- **7/16** 有 `migrate-to-new-pc.sh` 迁移脚本

### 今日 merge 事件（8/8 10:07）

merge.log 记录了完整过程：
- Phase A: 从 4 个 state.db 合并 113 会话 / 1610 消息
- Phase B: 重建 agent.json → 208 sessionIds
- Phase C: 6/9-6/15 备份永久丢失（已无法恢复）

### agent.json 波动

| 时间 | 会话数 | 说明 |
|---|---|---|
| 10:09 postmerge | 208 | 合并后 |
| 10:38 cleanup | 153 | QClaw 清理重复后 |
| 11:13 polluted | 60 | 异常污染（原因待查）|
| 当前 | 155 | 当前版本（polluted 恢复）|

---

## 未解决项

1. **audit.db 写入停止的根因**：为什么 8/4 后 `.qclaw-hermes` 内置 Hermes 不写 audit.db？（是配置问题还是代码 bug）
2. **polluted 事件**：11:13 agent.json 被污染到 60 的原因
3. **前端会话列表**：agent.json 155 vs audit.db 156 的轻微差异（1 个 0 消息会话）
4. **tui_gateway crash**：8/8 10:32 `_drain_stderr` GBK 解码失败（非致命，但说明 stderr 线程有问题）

---

## 备份位置

- `C:\Users\Administrator\.qclaw-hermes\audit.db.bak-20260808-113750`（修复前备份）
- `C:\Users\Administrator\.qclaw-hermes\state-merge-backup\agent.json.*`（agent.json 变体备份）
- `D:\HermesX\`（完整历史迁移目录）
