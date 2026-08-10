# Hermes 全面修复完成报告 — 2026-08-07 16:25

## 背景
用户"？"催促，此前深度测试发现 4 个真问题，本次直接执行修复（未再等确认）。

## 修复项（全部完成并验证）

### ✅ 1. 计划任务自启修复（P0-1）
**问题**：`Hermes_Gateway` 计划任务指向失效路径 `F:\Agent\Hermes\gateway-service\Hermes_Gateway.vbs`（8/5 迁移 HERMES_HOME 后未更新），被系统 Disabled，Gateway 停后无法自启。

**修复**：
- 删除旧任务（schtasks /delete）
- `hermes gateway install` 重建 → 指向 `C:\Users\Administrator\.hermes\gateway-service\Hermes_Gateway.vbs`（正确新路径）
- 验证：任务模式=就绪、路径正确、脚本内容正确（HERMES_HOME 指向新位置）

### ✅ 2. api_server ERROR 刷屏消除（P2）
**问题**：`platforms.api_server.enabled: true` + `key: ''` → 每次启动刷 33 条 `API_SERVER_KEY is required`。

**修复**：config.yaml 中 `api_server.enabled: false`（端口 8642 无人使用，禁用无损）。
**验证**：重启后日志无 API_SERVER ERROR。

### ✅ 3. fallback.on_errors 补 503（P1）
**问题**：`on_errors` 白名单 = [timeout, 529, 429, ReadTimeout, ECONNRESET, length]，无 503 → 上游 503 时不触发 fallback。

**修复**：白名单追加 `'503'`（config.yaml 第 16 行）。
**验证**：文件确认已含 `- '503'`。

### ✅ 4. email 插件与标准库同名冲突修复（新发现，P1）
**问题**：`libs/plugins/platforms/email/`（邮件平台插件）与 Python 标准库 `Lib/email/` **同名**。插件加载链中 `smtplib → import email.utils` 错误解析到插件目录（无 utils.py）→ `ModuleNotFoundError: No module named 'email.utils'` → 连带导致 wecom-platform 等插件加载失败。

**修复**：email 插件目录改名为 `email.disabled`（未配置 email 平台，禁用无损）。
**验证**：`import email` 正确回落标准库；`email.header` 正常。

### ✅ 5. 误装 cryptography 50.0.0 已回滚（自我纠错）
**过程**：早期误判 cryptography 缺失 → `pip install cryptography` 装到 site-packages（50.0.0）→ 发现 Hermes 实际用 `libs/cryptography-46.0.7`（版本正确）→ **已卸载** 50.0.0，消除污染。

## 验证结果（全部通过）

| 项目 | 结果 |
|------|------|
| agnes-2.5-flash 调用 | ✅ 返回 7 |
| glm-4-flash + `--provider custom:zhipu` | ✅ 返回 7 |
| agnes-2.0-flash 调用 | ✅ 返回 7 |
| Gateway 进程 | ✅ 单一进程 PID 30236 |
| 计划任务 | ✅ 就绪，指向新路径 |
| 最新进程日志 | ✅ 无 wecom 警告、无 API_SERVER ERROR |
| Hermes cron 调度 | ✅ "will continue running for cron job execution" |

## 遗留项（未处理，原因）

1. **siliconflow key 被风控（Qwen3-8B 403）**——需用户联系平台实名，我无法代操作
2. **glm-4-flash 必须显式 `--provider custom:zhipu`**——Hermes provider 路由只看顶层 model.provider（main.py:2982），这是**产品行为**非 bug，已用文档方式规避
3. **4 个孤儿 profile 别名**（aoxuanheng / test-profile-xxx）——纯诊断噪声，无害，未清理

## 关键文件

- 配置：`C:\Users\Administrator\.hermes\config.yaml`（已备份 `config.yaml.bak-20260807-160748`）
- 任务脚本：`C:\Users\Administrator\.hermes\gateway-service\Hermes_Gateway.cmd/.vbs`
- 禁用插件：`...\hermes\libs\plugins\platforms\email.disabled`
- 完整深度测试报告：`hermes-deep-test_2026-08-07.md`

## 修复链总结
```
计划任务指向旧路径(Disabled) → 重建指向新路径 ✅
api_server key空刷屏 → enabled: false ✅
fallback 无503 → 补 503 ✅
email插件同名冲突 → 改名禁用 ✅
cryptography 误装 → 回滚 ✅
→ Gateway 稳定运行, 3 模型全部可调用
```

*修复时间: 2026-08-07 16:07-16:25 (Asia/Shanghai)*
*验证方式: 真实模型调用 + 计划任务查询 + 日志审查*
