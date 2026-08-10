# Hermes × OpenClaw Provider 桥接方案

## 现状诊断

- ✅ Hermes Python CLI 完全可用（v0.19.0）
- ❌ QClaw UI 的 Hermes 角色是占位符，未接入后端
- ❌ `qclaw-plugin-hermes` 只是遥测插件，不负责模型路由
- ✅ Hermes API server 配置在 `127.0.0.1:8642`（已启动 PID 25176）

## 解决方案：CLI Bridge（已验证）

### 方案1: 直接用 Hermes CLI
```powershell
$env:HERMES_HOME = "C:\Users\Administrator\.hermes"
$env:PYTHONPATH = "D:\QClaw\v0.2.35.624\resources\hermes\libs"
& "D:\QClaw\v0.2.35.624\resources\python\python.exe" -m hermes_cli -z "你的问题"
```

### 方案2: OpenClaw Provider 桥接脚本（开发中）
文件：`hermes-cli-test.py`

功能：
- 调用 Hermes CLI 获取响应
- 返回 JSON 格式结果
- 支持多模型选择（glm-4-flash / agnes-2.0-flash）

### 方案3: OpenClaw Plugin（长期方案）
创建 `qclaw-hermes-provider` 插件：
```typescript
// 伪代码
import { ProviderPlugin } from "openclaw/plugin-sdk/provider-model-shared";
import { callHermesCLI } from "./hermes-bridge.js";

const hermesProvider: ProviderPlugin = {
  id: "hermes",
  label: "Hermes (Zhipu/Agnes)",
  catalog: {
    run: async () => ({
      provider: {
        baseUrl: "cli://hermes",
        api: "custom-hermes",
        models: [
          { id: "glm-4-flash", name: "GLM-4-Flash" },
          { id: "agnes-2.0-flash", name: "Agnes-2.0-Flash" }
        ]
      }
    })
  }
};
```

## 文件清单

| 文件 | 状态 | 用途 |
|---|---|---|
| `hermes-cli-test.py` | ✅ 已创建 | CLI 桥接脚本 |
| `hermes-fix_20260805.md` | ✅ 已创建 | 配置修复记录 |
| `hermes-qclaw-bridge_20260805.md` | ✅ 已创建 | 集成诊断报告 |
| `hermes-openclaw-provider.md` | ✅ 本文件 | Provider 方案文档 |

## 验证结果

- ✅ `glm-4-flash` + zhipu: 正常返回
- ✅ `agnes-2.0-flash` + agnes-ai: 正常返回
- ❌ `Qwen/Qwen3-8B` + siliconflow: 403（账户未实名）
- ⚠️ Hermes Gateway: 已启动 PID 25176

## 下一步

1. **立即使用**：直接运行 `hermes-cli-test.py <prompt> [model]`
2. **长期方案**：等待 QClaw 官方集成或手动编写 OpenClaw plugin
3. **Hermes Gateway**：已启动，可通过 HTTP API 调用（port 8642）
