# 软件诊断与修复 — 2026-08-07

## 目标
用户报告"软件遇到问题"，要求排查并修复。

## 诊断过程（已验证）
1. `openclaw status` 显示两个红旗：`Update: npm … deps missing` + `Tasks: 18 issues / audit 1 error`。
2. 定位 OpenClaw 安装目录：`D:\QClaw\v0.2.35.624\resources\openclaw`。
3. `npm ls --depth=0 --omit=dev` 发现 `node_modules` 根目录被注入 **37 个会话日志 `.jsonl` 文件**（来自某清理脚本 cwd 配错，落点为 `D:\Cache\Temp\openclaw-workspace-summary\clean-workspace`），被 npm 判定为 `extraneous` 垃圾 → 这是 "deps missing / 依赖异常" 误报的直接来源。
4. 校验核心运行依赖：**openclaw / acpx / undici / ws / express 全部存在且完好** → 当前运行未被破坏。
5. `openclaw update status` 确认 "deps missing" 实指**待更新版本 2026.7.1-2 的依赖未就绪**（更新通道中间态），非当前损坏。
6. 任务系统 18 issues：逐个核对 cron（5c3f 分层归档 / a985 月报 / 97bf GitHub同步 / 68b7 tech-monitor / fd20 Dreaming / 5755 每日监控）均同时有 `succeeded`（带真实产出摘要）与 `failed / Running cron job.` 的陈旧/重复记录 → 判定为**历史脏数据**（与 MEMORY 记录的 cron list/SQLite 双源 ID 不一致陷阱吻合），当前 cron 实际正常成功运行。
7. `openclaw security audit`：0 critical / 3 warn / 2 info（trusted_proxies_missing、multi_user_heuristic）→ 非致命。

## 已执行修复（已验证）
- 将 37 个误入 `node_modules` 的 `.jsonl` 移出至 `D:\QClawX\data\quarantine-openclaw-node-jsonl`（用 Move 而非删除，可恢复，符合 trash>rm）。
- 复检：`node_modules` 根目录 `.jsonl` 残留 = **0**；`npm ls` 仅剩无害的 `undici-types@7.18.2 extraneous`（TS 类型包，运行时不需要）。
- Gateway 状态：local reachable 181ms / auth token 正常；QQ Bot、微信服务通道均 ON/OK。

## 结论
- 软件核心运行**正常**，本对话本身即证明 runtime 健康。
- **真实修复点**：清除了 node_modules 污染，消除 "deps missing / extraneous" 误报来源。
- **非故障项**（无需处理）：
  - `deps missing` = 有 2026.7.1-2 待更新版本，其依赖尚未安装（更新通道中间态）。
  - 18 issues = cron 历史陈旧/重复记录，当前 cron 正常成功。
  - security audit 3 warn = 非致命配置建议。

## 待用户决策（破坏性操作，未擅自执行）
若希望消除 "deps missing" 提示，需执行 `openclaw update`（2026.6.5 → 2026.7.1-2 跨版本升级）。该操作可能触动现有 13 个 cron 任务配置（MEMORY 记录过 cron 配置被平台保护、改动有陷阱），建议确认后再做。可随时执行。
