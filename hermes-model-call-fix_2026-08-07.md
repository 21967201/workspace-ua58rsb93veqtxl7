# Hermes 角色模型调用问题诊断与修复 — 2026-08-07 15:28

## 用户指令
"软件的 hermes 角色模型调用老是有问题，是什么问题检查下？"

## 诊断过程（已验证）

### 1. 环境定位
- Hermes 本体路径：`D:\QClaw\v0.2.35.624\resources\hermes\libs\hermes_cli\main.py`（被 QClaw 客户端内嵌）
- 运行时：`D:\QClaw\v0.2.35.624\resources\python\python.exe` (3.11.10)
- 配置目录：`C:\Users\Administrator\.hermes\`
- HERMES_HOME：`C:\Users\Administrator\.hermes`（注册表 HKCU + 系统环境变量均已正确）

### 2. 核心问题定位
**`hermes status` 显示 `Gateway Service: stopped`** —— Hermes Gateway 未运行。
- Gateway 是承载「角色模型调用」的服务核心，停止 → 所有模型调用失败。
- `gateway-stdio.log` 有 33 条重复 ERROR：
  `Api_Server Refusing to start: API_SERVER_KEY is required for the API server, including loopback-only binds on 127.0.0.1.`
- 另有 WARNING：`No adapter could be created for any of the 1 configured platform(s)`。
- 根因：Gateway 之前异常退出/未启动，配置文件 `platforms.api_server.key: ''`（空）→ api_server 平台拒绝启动并反复重试刷错误日志。

### 3. 修复动作
- 执行 `hermes gateway start` → 成功启动（PID 21668），自动注册 Scheduled Task `Hermes_Gateway`。
- **真实场景测试**（非仅看进程）：`hermes -z "1+1等于几"` → 模型返回 `2` ✅ 调用链路恢复。
- 复检 `gateway status` → `Gateway process running (PID: 21668)` ✅

### 4. `hermes doctor` 全面体检结果（已验证）
✅ 健康项：
- Python 3.11.10 / SSL CA 证书有效
- 配置版本 v33（最新，无废弃键）
- API key 已配置（agnes-2.5-flash / custom:agnes）
- 依赖包全齐（OpenAI SDK / Rich / PyYAML / HTTPX 等）
- 工具可用性：file/terminal/memory/skills/cronjob/vision/tts 等核心工具全 OK
- 内置 memory provider 正常

⚠ 不阻断模型调用的待清理项：
- `platforms.api_server.key` 为空 → 每次重启刷 33 条 ERROR（端口 8642 实际无人监听，该平台未使用）
- 4 个孤儿 profile 别名（aoxuanheng / test-profile-23720.bat / test-profile-24888.bat / test-profile-5620.bat）
- 可选工具未配 key（web/x_search/discord/moa 等，与模型调用无关）

## 结论
**"模型调用老有问题"的根因 = Hermes Gateway 服务处于停止/崩溃态**，不是模型、API key 或配置损坏。重启 Gateway 后真实调用测试通过，问题已修复。

## 后续建议（未擅自修改）
1. **清除 api_server ERROR 日志刷屏**：在 `config.yaml` 中将 `platforms.api_server.enabled` 改 `false`（该平台当前未使用），或设置一个 `key`。可避免下次重启再刷 33 条 ERROR。
2. **清理 4 个孤儿 profile 别名**：删除 `profiles/` 下失效别名文件。
3. Gateway 已注册为 Scheduled Task `Hermes_Gateway`，后续开机/异常应由系统拉起；如仍频繁崩溃，需查 `gateway-exit-diag.log` 的退出原因。

## 验证清单
- [x] Gateway 已启动（PID 21668）
- [x] 真实模型调用测试通过（返回 "2"）
- [x] gateway status 显示 running
- [x] doctor 核心项全绿
- [ ] api_server ERROR 日志刷屏（待用户确认是否清理）
