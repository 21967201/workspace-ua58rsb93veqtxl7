# Hermes 深度模拟测试报告 — 2026-08-07 16:05

## 测试范围
在初诊（Gateway 停止）基础上，对 Hermes/Gateway 做完整链路压测，覆盖：全模型可用性、路由机制、fallback 配置、provider 语法、自启动可靠性、cryptography 依赖。

---

## 发现的问题（严重程度排序）

### 🔴 P0：Provider 路由错误 — glm-4-flash / Qwen3-8B 实际不可用

**问题描述**：
`--model glm-4-flash`（不带 `--provider`）时，请求被错误路由到 agnes 网关（`apihub.agnes-ai.cn`），而非配置里指定的 zhipu 官方（`open.bigmodel.cn`）。agnes 网关没有 glm-4-flash 模型 → HTTP 503。

**实测验证**（request_dump 铁证）：
| 模型 | 不带 --provider | 实际请求 URL | 结果 |
|------|----------------|-------------|------|
| agnes-2.5-flash | ✅ 默认 Agnes | `apihub.agnes-ai.cn` | 正常 |
| glm-4-flash | ❌ 走 Agnes | `apihub.agnes-ai.cn` | 503 |
| agnes-2.0-flash | ✅ 默认 Agnes | `apihub.agnes-ai.cn` | 正常 |
| Qwen/Qwen3-8B | ❌ 走 Agnes | `apihub.agnes-ai.cn` | 503 |

**根因代码**：
- `main.py:2982`：`effective_provider = config.get("model").get("provider")` — 只读**顶层** `model.provider`（= `custom:agnes`）
- `models[]` 列表里的 `provider: custom:zhipu` / `provider: custom:siliconflow`**只是展示元数据，不参与调用路由**
- 无 provider 时所有模型默认走 Agnes 网关

**Workaround（验证有效）**：
```
hermes -z "..." --model glm-4-flash --provider custom:zhipu  ✅ 返回正确结果
```
分开传 `--provider` 参数才生效。

**`provider:model` 合并语法验证（均失败）**：
```
--model custom:zhipu/glm-4-flash    ❌ 原样发给 agnes（custom:zhipu/glm-4-flash 当模型名）
--model custom:zhipu:glm-4-flash    ❌ 同上
```
合并语法在 `-z` 单行模式里没有被解析，原样透传给 agnes 网关。

**业务影响**：用户不指定 provider 时，glm-4-flash / Qwen3-8B 不可用。这与"模型调用老有问题"直接相关。

---

### 🔴 P0：Qwen3-8B 自身不可用（独立问题）

**实测**：`--model Qwen/Qwen3-8B --provider custom:siliconflow` → HTTP 403 "please complete identity verification"

**分析**：siliconflow API key 被风控，需要实名认证。不是 Hermes 配置问题，是 key 本身不可用（8/5 请求历史 dump 显示之前也发到 agnes，从未真正打到 siliconflow）。

**影响**：Qwen3-8B 在当前 key 状态下**完全不可用**，无论哪种调用方式。

---

### 🔴 P1：Gateway 自启动机制完全失效

**问题**：`Hermes_Gateway` 计划任务指向失效路径 `F:\Agent\Hermes\gateway-service\Hermes_Gateway.vbs`（旧安装目录），实际 HERMES_HOME 已迁移到 `C:\Users\Administrator\.hermes`。

**证据**：
- `LastRunResult = 1`（失败）
- `Enabled = False`（系统自动禁用）
- 创建者 = N/A（说明是通过 `gateway start --register-task` 注册的，未指定 Program 参数，使用了旧路径）

**后果**：Gateway 停止后不会自动拉起 → 模型调用永久失败，直到手动 `hermes gateway start`。

**修复**：重新注册计划任务，指向正确路径：
```
schtasks /change /tn "Hermes_Gateway" /enable
schtasks /change /tr "...正确路径..." /tn "Hermes_Gateway"
```
或用 `hermes gateway start` 重新注册（需确认参数）。

---

### 🟡 P2：计划任务路径来源分析

8/5 16:50 修改 HERMES_HOME 后，`hermes gateway start` 重新注册计划任务时仍使用了旧的 Hermes 安装路径 `F:\Agent\Hermes`（可能是 `hermes gateway start` 读取的路径来自硬编码或环境残留）。

需确认：当前运行的 Gateway（PID 21668）是从哪个路径启动的，以及 `hermes gateway start` 在注册计划任务时如何确定 Hermes 本体路径。

---

### 🟡 P2：Fallback on_errors 不含 503

**配置**：
- `config.yaml model.fallback.on_errors` = [timeout, 529, 429, ReadTimeout, ECONNRESET, length]
- **不含 503**

**影响**：如果 glm-4-flash 设为主模型、zhipu 上游报 503（无通道），fallback 机制不会触发（503 不在白名单），直接报错退出。

**修复**：在 `config.yaml model.fallback.on_errors` 加入 `"503"`。

---

### 🟡 P2：cryptography 模块缺失

**`hermes doctor` 警告**：`Failed to load plugin 'wecom-platform': No module named 'cryptography'`

**实测**：`python -c "import cryptography"` → `ModuleNotFoundError`

**影响**：企业微信插件（wecom-platform）无法加载，微信平台接入能力丧失。微信 Bot 其他部分正常（QClaw 层面的微信服务号 ON/OK）。

**修复**：`pip install cryptography`（用 hermes 的 python：`python.exe -m pip install cryptography`）

---

### 🟢 P3：api_server ERROR 日志刷屏

**现象**：每次 Gateway 启动刷 33 条 `API_SERVER_KEY is required` ERROR。

**根因**：`config.yaml platforms.api_server.enabled: true` + `key: ''`（空）→ api_server 平台拒绝启动，但 Hermes 反复重试。

**确认**：端口 8642 实际无监听、无任何消费者。**该平台当前完全未使用**。

**修复**：将 `platforms.api_server.enabled` 改为 `false`（彻底禁用），或设置一个非空 key。禁用后不再刷 ERROR 日志。

---

### 🟢 P4：4 个孤儿 profile 别名

**`hermes doctor` 报告**：`aoxuanheng`、`test-profile-23720.bat`、`test-profile-24888.bat`、`test-profile-5620.bat`（均指向已删除 profile）

**影响**：无功能影响，仅诊断噪声。

**修复**：删除 `profiles/` 下对应别名文件。

---

## 验证完成项（✅）

| 验证项 | 结果 |
|--------|------|
| agnes-2.5-flash 不带 provider | ✅ 正常 |
| agnes-2.0-flash 不带 provider | ✅ 正常 |
| glm-4-flash 显式 --provider custom:zhipu | ✅ 正常 |
| siliconflow API key 有效性 | ❌ 403（key 被风控）|
| cryptography 模块 | ❌ 缺失 |
| Gateway 当前运行状态 | ✅ PID 21668 |
| 计划任务自启 | ❌ Disabled（失效路径）|
| fallback on_errors 含 503 | ❌ 不含 |
| api_server ERROR 日志 | ❌ 每次启动刷 33 条 |
| `models[].provider` 是否参与路由 | ❌ 不参与（仅元数据）|

---

## 待确认：为什么 8/5 后所有请求都打到 agnes

历史 dump 显示：
- **8/5**：所有请求正常打到各 provider 官方 URL（bigmodel.cn / siliconflow.cn）
- **8/7**：所有请求统一打到 `apihub.agnes-ai.cn`（agnes 网关）

说明 8/5 16:44 profile qclawx/config.yaml 修改（`model.provider: custom:zhipu`）之后，Hermes 的路由行为发生了根本性变化——从此所有不带 provider 的模型都被发往 agnes 网关。

**需要确认**：这一变化是 Hermes 行为变更，还是某次配置写入引入了全局 provider 覆盖逻辑。检查 8/5 到 8/7 之间 config.yaml 的变更历史（文件 mtime 显示 8/5 16:50）。

---

## 完整根因链

```
问题: "Hermes 角色模型调用老有问题"

第1层: Hermes Gateway 停止 → 模型调用全挂
  根因: Hermes_Gateway 计划任务指向旧路径 F:\Agent\Hermes\...
       → 8/5 后 LastRunResult=1 → 被系统 Disabled
       → Gateway 停后不会自动拉起

第2层: Gateway 停止后手动重启正常, 但 glm-4-flash/Qwen3-8B 仍 503
  根因: Hermes provider 路由只看顶层 model.provider (custom:agnes)
       models[].provider 仅是元数据,不参与路由
       → 所有不带 --provider 的调用走 agnes 网关
       → agnes 网关无 glm-4-flash / Qwen3-8B → 503

第3层: 503 不触发 fallback
  根因: model.fallback.on_errors 白名单不含 "503"

第4层: siliconflow Qwen3-8B 独立不可用
  根因: siliconflow API key 被风控 (HTTP 403)
```

---

## 修复优先级建议

| 优先级 | 操作 | 风险 |
|--------|------|------|
| P0-1 | 重新注册 Hermes_Gateway 计划任务（正确路径） | 低 |
| P0-2 | 用户培训/文档：glm-4-flash 必须加 `--provider custom:zhipu` | 无 |
| P1 | 补 fallback.on_errors 加 `"503"` | 低 |
| P1 | `pip install cryptography` | 低 |
| P2 | 禁用 `platforms.api_server.enabled: false` | 低 |
| P2 | 确认 siliconflow key 状态（联系 siliconflow） | 中 |
| P3 | 清理 4 个孤儿 profile 别名 | 极低 |

---

*测试时间: 2026-08-07 15:28-16:05 (Asia/Shanghai)*
*验证方法: 真实 API 调用 + request_dump 抓包 + 代码逻辑追踪*
