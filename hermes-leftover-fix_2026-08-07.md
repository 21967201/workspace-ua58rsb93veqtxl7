# 遗留问题修复记录 — 2026-08-07 16:30-17:00

## 背景
用户要求"遗漏问题有修复下"，针对上一轮修复（计划任务/api_server/fallback 503/email 插件/cryptography 回滚）后遗留的 3 个问题深入排查。

## 遗留问题排查结果

### ✅ 已修复：qclawx profile provider 配置打架（真正根因）

**发现**：Hermes 角色「轩恒」实际使用的 profile `C:\Users\Administrator\.hermes\profiles\qclawx\config.yaml` 中：
```yaml
model:
  default: agnes-2.5-flash   # 默认模型 = agnes
  provider: custom:zhipu     # 但全局 provider = zhipu ⚡ 打架！
```

**代码级确认**（cli.py:3909-3914）：
```python
self.requested_provider = (
    provider                                  # CLI 参数
    or CLI_CONFIG["model"].get("provider")    # ← config.yaml model.provider
    or os.getenv("HERMES_INFERENCE_PROVIDER")
    or "auto"
)
```
**`models[].provider` 字段从不参与路由**——只是展示元数据。agent 模式 provider 只看顶层 `model.provider`。

**影响**：agnes-2.5-flash 默认模型被路由到 zhipu（bigmodel.cn），zhipu 不认识 agnes 模型 → 各种 503/异常 → 「模型调用老有问题」的真实体验。request_dump 铁证：8/7 大量请求打 `apihub.agnes-ai.cn` 带 `custom:zhipu/glm-4-flash` 模型名（透传错误）。

**修复**：`provider: custom:zhipu` → `custom:agnes`（备份 `config.yaml.bak-fix-20260807-*`）

**验证**：
- `-p qclawx -z` 默认模型 → 返回 6 ✅
- `-p qclawx chat --query "hi"`（agent 主循环）→ **正常回复「您好，有什么要处理的？」** ✅
- Gateway 运行中（PID 30236），日志无 ERROR 刷屏 ✅

### ⚠️ 确认产品行为（非 bug，已文档化）：glm-4-flash 需显式 provider

- `model_aliases` 的 DirectAlias 在 `-z`/profile 组合下**不生效**（别名当模型名透传）
- `-m glm-4-flash --provider custom:zhipu`（分开传）→ 正常 ✅
- `custom:zhipu/glm-4-flash` 合并语法 → 不解析，透传报 503 ❌
- 结论：多 provider 场景下必须显式 `--provider`，这是 Hermes 设计

### ⚠️ 无法代修（需用户操作）：siliconflow 未实名

- 直接 curl 验证：`Access denied: please complete identity verification`
- key 有效，账号未实名认证 → 所有 API 被拒
- **需用户登录 cloud.siliconflow.cn 完成实名认证**（Qwen3-8B 才能用）

### ✅ 已确认无需处理：孤儿 profile 别名

- `profiles/` 目录只有 `qclawx`，无 aoxuanheng/test-profile-* 残留
- 之前 doctor 报告的孤儿别名已不存在（可能已自动清理）

## 测试过程发现

- `-q` 参数在 main.py 顶层不存在（需 `chat` 子命令），`chat "msg"` 也报错，正确用法 `chat --query "msg"`
- PowerShell 下 Hermes 的 UTF-8 输出显示为乱码（cp936 vs UTF-8），功能不受影响
- `UnicodeDecodeError: 'gbk' codec` 是 stderr reader 编码问题，非功能故障

## 最终状态
- **Hermes 角色（qclawx）模型调用正常**（agnes-2.5-flash 走 agnes 网关）
- 3 个模型：agnes-2.5-flash ✅ / agnes-2.0-flash ✅ / glm-4-flash（+--provider）✅
- Qwen3-8B：待用户实名 siliconflow
- Gateway 稳定，日志干净，计划任务就绪
