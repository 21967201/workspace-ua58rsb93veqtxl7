# QClaw 官方客户端更新通道查证 — 2026-08-07 15:23

## 用户指令
"(b) 走 QClaw 官方客户端更新通道升级内核"

## 查证过程（已验证）
1. **定位客户端更新机制**：
   - 客户端根目录 `D:\QClaw\v0.2.35.624` 含 `app-update.yml`
   - `app-update.yml` 内容：`provider: generic` / `url: https://placeholder.example.com` / `updaterCacheDirName: qclaw-updater`
   - 更新服务器是 **placeholder（占位符）** → 说明构建时未配置真实在线更新源

2. **内核打包方式**：
   - OpenClaw 内核以分卷 tar 打包：`resources/openclaw_0.tar / openclaw_1.tar / openclaw_2.tar` + `app.asar`
   - 外层 `resources/openclaw/package.json` 声明 `2026.4.21`，但运行中内核 `node_modules/openclaw` = `2026.6.5`
   - 内核由环境变量 `QCLAW_CLI_OPENCLAW_MJS` 锁定，无法被通用 `openclaw update` 触碰

3. **官方更新器实际状态**：
   - 更新缓存目录 `C:\Users\Administrator\AppData\Local\qclaw-updater\pending\` 已存在
   - 内含已下载安装包：`QClaw-Setup-0.2.35-5001-624_silent.exe`（565MB, 2026-07-28）
   - `update-info.json`：fileName = 同上，sha512 校验值完整，isAdminRightsRequired=false
   - **该包版本 = 0.2.35-5001-624，与当前安装版本 0.2.35.624 完全相同**（5001 = channel.json 中的渠道号）

4. **联网交叉验证**：
   - 官方下载站：`https://qclaw.qq.com`（全量公测，无需邀请码）
   - 第三方软件站最新公开版：`v0.2.31`（2026-07-04），**比你当前的 0.2.35 还旧**
   - GitHub Issue #70960：QClaw 覆盖安装存在"程序消失"严重 bug（安装器先卸载后安装，卸载逻辑误删刚装好的新版）

5. **运行中版本确认**：
   - 进程主模块：`D:\QClaw\v0.2.35.624\QClaw.exe`
   - `.qclaw-version` = `0.2.35.624`

## 结论（已验证）
**官方渠道当前没有比 0.2.35.624 更新的 QClaw 客户端。**
- 官方更新器已经把"最新版"下载到本地 pending，但它与当前安装版本**完全一致**。
- 因此没有更新的 OpenClaw 内核可供升级——`openclaw update` 显示的 "2026.7.1-2 deps missing" 是 OpenClaw npm 上游已发但**腾讯尚未打包进客户端**的版本，当前架构无法获取。
- 用户已处于官方最新状态。

## 风险评估
- 应用 pending 安装包 = 用完全相同的 0.2.35.624 重装一遍 → **零收益**，且按 #70960 有"程序消失"炸机风险（尤其当前安装在非标准路径 D:\QClaw...，风险更高）。
- 去第三方站下更旧的 0.2.31 = 降级 + 来源不可信 → 严禁。
- 硬改内核 = 破坏客户端完整性 → 严禁。

## 决策
**不执行任何安装/覆盖操作。** 系统维持当前已是最新的稳定态。
"deps missing" 为无害的待更新版本脏标记，非故障。

## 后续
若未来腾讯发布含更新 OpenClaw 内核的 QClaw 客户端（>0.2.35.624），官方更新器会自动下载到 `qclaw-updater/pending`，届时可评估安全应用（需先完整备份客户端目录，规避 #70960）。

## 当前健康状态
- QClaw 客户端：0.2.35.624（官方最新，pending 包同版本）
- OpenClaw 运行中内核：2026.6.5
- 13 个 cron 任务：全部正常
- node_modules：已清理，无 .jsonl 污染
- 依赖：openclaw/acpx/ws/express/undici 全部 OK
