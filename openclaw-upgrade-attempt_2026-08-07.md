# OpenClaw 升级尝试复盘 — 2026-08-07

## 用户指令
"升级"（针对前面诊断出的 `Update: deps missing / 2026.7.1-2 available` 提示）。

## 执行前保护（均已落地）
- 备份配置：`C:\Users\Administrator\.qclaw\openclaw.json.bak-before-upgrade-20260807`（53034 字节）
- 快照 cron：`D:\QClawX\backups\cron-before-upgrade-20260807.json`（46448 字节，含 13 个任务）

## 升级过程
1. `openclaw update --yes --no-restart` 运行，输出 "Upgraded! Peter fixed stuff."
2. 但末尾提示：`Gateway: restart skipped`、`update PATH so openclaw points to the version you want`。
3. 手动 `openclaw gateway restart`。

## 关键发现（已验证，重要）
**`openclaw update` 对当前安装是失效的升级路径。**
- 当前运行内核由环境变量 `QCLAW_CLI_OPENCLAW_MJS` 锁定：
  `D:\QClaw\v0.2.35.624\resources\openclaw\node_modules\openclaw\openclaw.mjs`
  这是 QClaw 桌面客户端（Electron，版本 0.2.35，2026-07-28 编译）**内嵌**的 OpenClaw。
- 该入口实际版本 = **2026.6.5**（即 `node_modules/openclaw` 包版本）。
- 升级后 `openclaw --version` 仍 = 2026.6.5；`update status` 仍显示 `available 2026.7.1-2 / deps missing`。
- 结论：`openclaw update` 只碰了 npm 全局那条**不存在/不生效**的路径（`where openclaw` 列出的 `...\npm-global\openclaw` 实际路径不存在），未触碰运行中的 Electron 内嵌内核。
- 所谓 "deps missing" 正是这个失效升级留下的脏状态：目标版本 2026.7.1-2 依赖从未装入当前安装。

## 污染与清理（已验证）
- 升级过程又向 `node_modules` 根目录写入 1 个会话日志 `.jsonl`（根源：某内部脚本 cwd 错配到空目录 `D:\Cache\Temp\openclaw-workspace-summary\clean-workspace`）。
- 已移出至 `D:\QClawX\data\quarantine-openclaw-node-jsonl`。
- 最终复检：node_modules `.jsonl` 残留 = **0**；核心依赖 openclaw/acpx/ws/express/undici 全部 OK。

## cron 配置完好性（已验证）
- 升级前 13 个任务名 vs 当前 13 个任务名，集合完全一致 → 升级**未破坏任何 cron 配置**。
- 无需从备份回滚配置。

## 正确升级途径（给用户）
更新 **QClaw 桌面客户端本身**（客户端 0.2.35 的内嵌 OpenClaw 内核才会随之升级）。
CLI 里硬跑 `openclaw update` 对此架构无效，只会反复产生 "deps missing" 脏标记。

## 当前状态结论
- 软件运行健康，本次"升级"未造成任何实际破坏（cron 完好、配置原样、依赖干净）。
- 版本仍 2026.6.5，与升级前一致——即"升级"实际上未发生。
- 系统已回到干净稳定态。若需真正升级内核，应走 QClaw 客户端更新通道，而非 CLI `openclaw update`。

## 待决策
是否要：(a) 保持当前稳定版 2026.6.5 不动；(b) 通过 QClaw 官方客户端更新升级内核。
本次为风险规避，未擅自改变客户端本体。
