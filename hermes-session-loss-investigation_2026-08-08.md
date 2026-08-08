# Hermes 会话数据排查报告（2026-08-08）

## 用户问题
用户反馈"hermes角色又不问题了"→"会话数据丢失"。

## 核心发现

### 1. 两套 Hermes 数据源共存

| 路径 | 大小 | 会话数 | 最后更新 | 用途 |
|------|------|--------|----------|------|
| `C:\Users\Administrator\.hermes\` | 13.31 MB | 43 会话 / 85 消息 | 8/7 16:46 | 用户级 HERMES_HOME（我昨天修的） |
| `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\` | 13.72 MB | 2 会话 / 8 消息 | 8/5 13:59 | QClaw 内置 Hermes |

**关键差异**：
- 用户级 .hermes 的 43 个会话**全是 8/7 我测试的 CLI 会话**（"只回复数字N"）
- QClaw 内置 .hermes 的 2 个会话**是 8/5 的集成测试**（"测试QClaw集成"）
- **两个库里都没有真实对话历史**（用户和"轩恒"的聊天记录）

### 2. 进程架构（8/8 11:20 状态）

```
QClaw.exe (PID 17216)
├── qclaw_launcher (PID 17440, python.exe -m qclaw_launcher) 监听 8642
├── tui_gateway.slash_worker (PID 17080, 会话 20260808_095320)
└── ...（其他子进程）

独立进程:
hermes_cli.main gateway run (PID 15888, pythonw.exe) -- 标准Hermes Gateway，9:44 启动
```

**关键洞察**：
- 8642 端口由 **qclaw_launcher** 监听，不是标准 Hermes gateway
- qclaw_launcher 是 QClaw 自己的启动器，**可能用内置 .hermes 作为数据源**
- 标准 Hermes gateway (PID 15888) 我昨天已修复（计划任务自启、api_server 禁用、fallback 加 503）

### 3. QClaw 前端会话来源假设

**假设 A**：QClaw 前端 → qclaw_launcher (8642) → **内置 .hermes 的 state.db**（2 个测试会话）
- 这解释了为什么用户看到"会话丢失"——内置库本来就是空的/只有测试数据

**假设 B**：QClaw 前端 → qclaw_launcher (8642) → 远程 API（腾讯后端）
- 会话存在云端，本地 state.db 只是缓存/测试

**假设 C**：QClaw 前端有**独立的会话存储**（IndexedDB / 自有数据库）
- 与 Hermes state.db 完全无关

### 4. 已排查但未找到的数据位置

- ❌ QClaw IndexedDB (`Roaming\QClaw\IndexedDB`) —— 2.5MB 遥测数据，无聊天记录
- ❌ QClaw qclaw.db (`Roaming\QClaw\qclaw.db`) —— 审计日志，6326 条，无会话
- ❌ Roaming\hermes (11.88MB) —— Electron 壳，无 state.db
- ❌ F:\Agent\Hermes —— 整个 F 盘不存在（旧 HERMES_HOME 已删）
- ❌ D:\HermesData / AppData\Local\hermes —— PATH 残留路径，目录不存在
- ❌ .enc 加密日志 (`Roaming\QClaw\logs\hermes\`) —— 遥测日志，解密后无会话数据

### 5. qclaw-plugin-hermes 插件分析

路径：`D:\QClaw\v0.2.35.624\resources\hermes\.hermes\plugins\qclaw-plugin-hermes\`

功能：**遥测上行插件**（session_audit、trace_reporter、queue_guard、qclaw_reporter）
- 采集 Hermes 事件（会话开始/结束、LLM调用、工具调用）
- HTTP 回调 → auth-gateway → galileo-otel 上报
- **不是会话存储层**（只上报，不持久化会话列表）

### 6. 两套 state.db 详情

#### 用户级 (`C:\Users\Administrator\.hermes\state.db`)

```sql
-- 43 会话，全部 cli 来源
SELECT id, source, title FROM sessions;
-- 全是 "只回复数字N" 测试
-- 最新: 20260807_164307 (18h ago)
```

#### 内置 (`D:\QClaw\v0.2.35.624\resources\hermes\.hermes\state.db`)

```sql
-- 2 会话，qclaw 来源
1. "测试QClaw集成" (20260805_135839)
2. "QClaw Hermes 集成测试成功" (20260805_135952)
-- 最新: 8/5 13:59
```

**两者均无真实对话历史**。

## 根因链（当前最佳解释）

1. QClaw 客户端"轩恒"角色启动时，通过 `qclaw_launcher` 创建 Hermes 会话
2. `qclaw_launcher` **可能使用内置 .hermes 作为数据目录**（而非用户级）
3. 内置 state.db 只有 8/5 的测试数据 → 用户看到"无会话"
4. 用户的真实历史对话**可能从未持久化**（或存在未发现的位置，或云端）

## 待确认事项

### 需要用户回答

1. **"会话数据丢失"具体在哪看到？**
   - QClaw 客户端里"轩恒"的会话列表页面？
   - Hermes CLI 的 `hermes sessions list` 输出？
   - 其他位置？

2. **最后一次和轩恒正常对话是什么时候？**
   - 时间点有助于定位数据迁移/丢失节点

3. **之前是否有明确操作过 Hermes 配置迁移？**
   - 如设置 HERMES_HOME、迁移目录等

### 需要技术确认

1. **qclaw_launcher 的 HERMES_HOME 指向哪里？**
   - 需要读取 qclaw_launcher 代码或启动参数
   - 路径：`D:\QClaw\v0.2.35.624\resources\python\Lib\site-packages\qclaw_launcher\`（假设存在）

2. **QClaw 客户端前端调什么 API 获取会话列表？**
   - 需要解包 app.asar 或抓包前端请求

3. **会话是否可能存在云端？**
   - QClaw 可能有云端会话存储（类似微信聊天记录云端同步）

## 已修复项（8/7）

1. ✅ Hermes Gateway 计划任务自启（重建指向正确路径）
2. ✅ api_server 禁用（消除 ERROR 刷屏）
3. ✅ fallback.on_errors 加 503
4. ✅ email 插件改名消除标准库冲突
5. ✅ 误装 cryptography 已回滚
6. ✅ qclawx profile provider 修正（custom:zhipu → custom:agnes）

## 未决问题

- zhipu-glm 别名在 qclawx profile 下失败（503）
- siliconflow 403（需实名认证）
- **会话数据丢失根因未定位**

## 下一步建议

### 给用户

**请明确告知**：
1. 会话丢失在哪个界面看到（截图/描述位置）
2. 最后正常对话的时间点
3. 是否需要恢复历史数据（还是只是想知道为什么丢失）

### 技术排查方向

1. **确认 qclaw_launcher 用哪个 .hermes**
   - 解包 `qclaw_launcher` 模块代码
   - 检查启动参数和环境变量

2. **抓包 QClaw 前端请求**
   - 用 Fiddler/Wireshark 抓 8642 端口请求
   - 看前端调什么 API 返回空会话列表

3. **检查是否有云端存储**
   - QClaw 账号登录态 → 可能同步云端会话
   - 需要用户确认是否有过登录/登出操作

## 环境信息

- OS: Windows 10.0.19045 (x64)
- QClaw: v0.2.35.624 (2026-07-28 编译)
- Hermes: 内核 0.19.0（libs 版本）
- OpenClaw: 2026.6.5
- Python: 3.11 (QClaw 自带)
- Node: v22.22.3 (QClaw 自带)

## 文件清单

```
用户级 Hermes:
  C:\Users\Administrator\.hermes\config.yaml (已修改)
  C:\Users\Administrator\.hermes\state.db (43 测试会话)
  C:\Users\Administrator\.hermes\sessions\ (会话数据目录)

QClaw 内置 Hermes:
  D:\QClaw\v0.2.35.624\resources\hermes\.hermes\state.db (2 测试会话)
  D:\QClaw\v0.2.35.624\resources\hermes\.hermes\plugins\qclaw-plugin-hermes\ (遥测插件)

QClaw 前端数据:
  C:\Users\Administrator\AppData\Roaming\QClaw\IndexedDB\ (遥测)
  C:\Users\Administrator\AppData\Roaming\QClaw\qclaw.db (审计日志)
  C:\Users\Administrator\AppData\Roaming\QClaw\logs\hermes\*.enc (加密遥测日志)
```

---

**报告时间**: 2026-08-08 11:30
**排查人**: OpenClaw Agent
**状态**: 等待用户确认会话丢失具体场景
