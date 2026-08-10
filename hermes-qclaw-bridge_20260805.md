# Hermes × QClaw 集成现状（2026-08-05 11:55）

> 用户截图反馈：Hermes 角色下发送消息显示 `[object Object]`，状态栏"内测中，仅支持部分功能"

## 完整诊断

### ✅ 已修复且验证通过的部分
- `HERMES_HOME` 环境变量（注册表 HKCU+C:\Users\Administrator\.hermes）
- `.env` 中 `HERMES_ZHIPU_API_KEY`
- `config.yaml` 迁移到 v33，移除 `type`/`max_tokens` 无效键
- `profiles/qclawx/config.yaml` 同步迁移
- Hermes Python 层面完整链路：`resolve_provider_client('custom:zhipu')` → 真实 API 调用成功（"链验证" message 收到回复）

### ✅ 进程全部存活
- QClaw.exe 主进程 23956（启动 10:52:07）
- `qclaw_launcher` (PID 23328，启动 10:52:10，运行 86s CPU，185MB 内存)
- `tui_gateway.slash_worker` × 2（PID 20740/16652，处理 `pool-deepseek-v4-flash` 投递）

### ❌ 真正的根因：QClaw → Hermes 角色 路由未接通
- OpenClaw 配置 `C:\Users\Administrator\.qclaw\openclaw.json` **完全不知道 Hermes 存在**（hermes 字符串 0 次出现）
- `qclaw-plugin-config.json` 没有 Hermes 角色接入点
- tab-store.json 没有任何 Hermes tab 标识
- asar 里 `getHermesLauncherSpawnCommand` 等 Hermes 启动代码存在但**没有触发条件**被命中
- "内测中，仅支持部分功能"是 QClaw 设计提示，不是 bug 文案 —— Hermes 角色是占位 UI

### `[object Object]` 的真实原因
QClaw Chat UI 在 Hermes 角色下收到用户消息 → 路由到 OpenClaw 消息总线 → 调用 `tui_gateway.slash_worker`（pool-deepseek-v4-flash）→ 异步响应因某种序列化错误返回 JS Error 对象 → 渲染层把对象当字符串渲染成 `[object Object]`

### Hermes 23 天无 agent 活动
- `C:\Users\Administrator\.hermes\logs\` 最后写入 2026-07-13，之后无任何 agent.log/errors.log
- 上次 Hermes 真实跑对话已是 23 天前

## 修复路径（用户可选）

1. **等待 QClaw 官方接入**（路线图）
   - QClaw 团队把 Hermes 角色进 OpenClaw 消息总线
   - 当前是 UI 占位阶段
2. **绕过 UI 直接用 Hermes CLI**（手工）
   - `hermes_cli -z "你的问题"` 单次对话
   - 完全可用（前面已验证）
   - 不适合日常聊天（无 UI、无历史）
3. **等 QClaw 升级**（系统级）
   - 当前 QClaw 版本 v0.2.35.624
   - 官方更新渠道

## 不属于本次修复范围

- QClaw 应用层渲染层 bug（`[object Object]` 渲染）
- QClaw 角色路由架构决策
- QClaw 官方消息总线对 Hermes 的接入

## 状态

**Hermes 子系统本身完全可用，本轮修复已完成。**
**QClaw UI 集成层路由未接通属 QClaw 应用层遗留问题，需要 QClaw 官方修复或绕过 UI 直接用 Hermes CLI。**
