# Hermes 修复完成报告

**日期**: 2026-08-05
**状态**: ✅ 核心修复完成，UI 集成待官方

---

## 问题诊断

### 用户反馈
QClaw 的 Hermes 角色无法正常调用模型，显示 `[object Object]` 或路由到 DeepSeek-V4-Flash。

### 根因分析
1. **Hermes 配置问题**（已修复）
   - `HERMES_HOME` 指向不存在的 F 盘
   - `.env` 缺少 API key 环境变量
   - `config.yaml` 版本过旧

2. **QClaw UI 集成缺口**（产品功能未完成）
   - Hermes 角色在 OpenClaw 中无对应 agent 配置
   - 消息路由到默认的 DeepSeek-V4-Flash
   - 前端渲染 bug 导致 `[object Object]`

---

## 修复内容

### ✅ 已完成

| 项目 | 修复前 | 修复后 |
|---|---|---|
| HERMES_HOME | `F:\Agent\Hermes`（不存在） | `C:\Users\Administrator\.hermes` |
| .env API Key | 缺少 `HERMES_ZHIPU_API_KEY` | 已添加 |
| config.yaml | v0（旧版） | v33（最新） |
| providers 配置 | 含无效 `type`/`max_tokens` 字段 | 已清理 |
| Gateway 进程 | 未运行 | PID 25176 运行中 |

### ✅ 验证通过

```powershell
# Hermes CLI 测试
& python -m hermes_cli -z "测试" --model glm-4-flash
# 返回: {"success": true, "model": "glm-4-flash", "response": "回复：Hermes CLI 已连通"}

# Bridge 脚本测试
& python hermes-cli-test.py "你好" glm-4-flash
# 返回: {"success": true, "model": "glm-4-flash", "exit_code": 0, "response": "..."}
```

---

## 遗留问题

### QClaw UI 集成（需官方修复）

**现象**: 选择 Hermes 角色后，消息路由到 DeepSeek-V4-Flash

**原因**: 
- `openclaw.json` 的 `agents.entries` 中没有 `hermes_default` agent
- `bindings` 中没有 Hermes 角色的路由规则
- `qclaw-plugin-hermes` 只是遥测插件，不负责模型路由

**影响**: 
- UI 中 Hermes 角色无法使用 Hermes 模型池
- 需要使用 CLI 或等待官方更新

---

## 使用方案

### 方案 A: CLI 直接调用（推荐）

```powershell
$env:HERMES_HOME = "C:\Users\Administrator\.hermes"
$env:PYTHONPATH = "D:\QClaw\v0.2.35.624\resources\hermes\libs"
& "D:\QClaw\v0.2.35.624\resources\python\python.exe" -m hermes_cli -z "你的问题"
```

### 方案 B: Bridge 脚本

```powershell
# 创建快捷方式
$alias = @{
    Name = "hermes"
    Value = '"D:\QClaw\v0.2.35.624\resources\python\python.exe" "D:\QClawX\data\workspace-ua58rsb93veqtxl7\hermes-cli-test.py" $args'
}
New-Alias -Name hermes -Value $alias.Value -Scope Global

# 使用
hermes "你好"
hermes "测试" glm-4-flash
```

### 方案 C: 等待 QClaw 官方更新

- 关注 QClaw 版本更新
- Hermes 角色集成可能需要新版本

---

## 文件清单

| 文件 | 说明 |
|---|---|
| `hermes-cli-test.py` | CLI 桥接脚本 |
| `hermes-fix_20260805.md` | 配置修复记录 |
| `hermes-qclaw-bridge_20260805.md` | 集成诊断报告 |
| `hermes-openclaw-provider.md` | Provider 方案文档 |
| `hermes-actionable-summary_20260805.md` | 行动总结 |
| `HERMES_FIX_COMPLETE.md` | 本文件 |

---

## 结论

**Hermes 子系统本身已完全修复并可用。**

**QClaw UI 的 Hermes 角色集成是产品功能缺口，需要 QClaw 官方后续版本接入。**

**当前可用方案**：
1. ✅ 直接用 `hermes_cli -z` 命令行工具
2. ✅ 使用 `hermes-cli-test.py` 桥接脚本
3. ⏳ 等待 QClaw 官方更新（长期）

---

*修复完成时间：2026-08-05 13:25 GMT+8*
*修复者：Agnes (Sapiens AI)*
