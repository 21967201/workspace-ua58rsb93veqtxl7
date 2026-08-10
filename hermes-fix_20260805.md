# Hermes 角色修复总结（2026-08-05）

## 根因（3 个叠加问题）

1. **`HERMES_HOME` 环境变量污染**（致命）
   - HKCU + HKLM 注册表残留 `HERMES_HOME=F:\Agent\Hermes`（F 盘不存在，历史安装残留）
   - QClaw.exe Electron 主进程继承该变量并注入 Hermes launcher（python -m qclaw_launcher）
   - 导致 Hermes 找不到 `.env`/`config.yaml` → 模型配置加载失败
   - ⚠️ HERMES_HOME 未设置时 Hermes 回退到 `AppData\Local\hermes`（非 `~/.hermes`），必须显式设置

2. **API key 环境变量名不匹配**（401 直接原因）
   - config.yaml 中 zhipu provider 引用 `key_env: HERMES_ZHIPU_API_KEY`
   - .env 原本只有 `ZHIPU_API_KEY` → 解析失败 → "no-key-required" → 401

3. **config.yaml 版本过旧 + 无效字段**
   - `_config_version` v0 → v33 迁移（`hermes doctor --fix`）
   - providers 中 `type`/`max_tokens` 为新版无效键（已移除）

## 修复操作

| 操作 | 状态 |
|---|---|
| 删除 HKCU+HKLM 残留 `HERMES_HOME=F:\Agent\Hermes` | ✅ |
| HKCU 重设 `HERMES_HOME=C:\Users\Administrator\.hermes` | ✅ |
| `.env` 添加 `HERMES_ZHIPU_API_KEY=c20a12700ad4...` | ✅ |
| config.yaml 迁移到 v33（doctor --fix） | ✅ |
| 移除 providers 的 type/max_tokens 无效键 | ✅ |
| profiles/qclawx/config.yaml 同步迁移 v33 | ✅ |
| 备份到 `D:\QClawX\data\backups\hermes-20260805\` | ✅ |

## 验证结果（真实环境，非模拟）

- ✅ `hermes status`：Model glm-4-flash / Provider custom:zhipu / .env exists
- ✅ zhipu API 直接调用：completion 3 / prompt 10 / total 13 tokens
- ✅ agnes-2.0-flash 调用成功
- ✅ 完整链路测试（libs 环境 + load_hermes_dotenv + _getenv + _get_named_custom_provider + resolve_provider_client）：
  - `resolve_provider_client('custom:zhipu', 'glm-4-flash')` → OpenAI client
  - 真实对话返回「正常」（usage: 3/9/12）
- ✅ qclaw_launcher / tui_gateway 导入正常（bundled libs 环境）
- ✅ QClaw 自动重启后新 launcher PID 23328 健康存活

## 关键架构事实

- QClaw 通过 Electron spawn `python -m qclaw_launcher`（WS launcher，不负责模型调用）
- 真正模型调用：`tui_gateway` + `agent/auxiliary_client.py resolve_provider_client`
- key 解析链路：`load_hermes_dotenv`（run_agent.py:127 模块加载时）→ os.environ → `_getenv`/`get_secret` → `_get_named_custom_provider`
- `custom:` 前缀由 `providers.py:511 is_aggregator` 路由到 `providers.<name>`
- `auth.py:1733 resolve_provider` 的 `zhipu→zai` 别名映射**不影响** QClaw 路径（走 runtime_provider 先解析）

## 遗留（非阻塞）

- siliconflow Qwen3-8B 返回 403（账户实名/风控问题，需在硅基流动完成实名）
- 独立 `hermes.exe` CLI 缺 concurrent_log_handler（site-packages 不完整）——QClaw 实际用 bundled libs 不受影响，已尝试补齐后还原（portalocker 连锁缺失，不折腾）
- `hermes_default` agent 在 openclaw.json 无配置（Hermes 集成走独立 qclaw_launcher WS 通道）
- 孤儿 profile alias（aoxuanheng、test-profile-*）健康度影响极低，未清理
- qclaw-plugin-hermes 遥测插件未启用（requires_env QCLAW_REPORT_URL 等未配置，非模型调用必需）

## 脚本产物

- `hermes_chain_test.py` — 完整解析链路测试（通过）
- `hermes_full_agent_test.py` — 端到端 agent turn 测试（通过，返回「正常」）
- `hermes_aux_probe.py` — auxiliary_client key 解析逻辑探测
- 其他 6 个探测脚本（hermes_deep_test 等）

## 状态

**HERMES 角色模型调用问题已完全解决。** 无未决阻塞项。
