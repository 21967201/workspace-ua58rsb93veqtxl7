# Hermes 修复行动总结（2026-08-05）

## 已完成

### 1. 配置修复 ✅
- `HERMES_HOME` 从 `F:\Agent\Hermes`（不存在）→ `C:\Users\Administrator\.hermes`
- `.env` 添加 `HERMES_ZHIPU_API_KEY`
- `config.yaml` 迁移 v0 → v33，移除无效字段

### 2. Hermes CLI 验证 ✅
- `glm-4-flash` 通过 zhipu API 正常响应
- Bridge 脚本 `hermes-cli-test.py` 工作正常

### 3. Gateway 启动 ✅
- PID 25176 运行中，但端口未监听（可能配置问题）

## 遗留问题

### QClaw UI 集成缺口（需官方修复）
- Hermes 角色消息被路由到 DeepSeek-V4-Flash
- `[object Object]` 是前端渲染 bug
- 这是产品功能未完成，非配置问题

## 立即使用方案

```powershell
# 方案 A: 直接 CLI
$env:HERMES_HOME = "C:\Users\Administrator\.hermes"
$env:PYTHONPATH = "D:\QClaw\v0.2.35.624\resources\hermes\libs"
& "D:\QClaw\v0.2.35.624\resources\python\python.exe" -m hermes_cli -z "你的问题"

# 方案 B: 使用桥接脚本
& "D:\QClaw\v0.2.35.624\resources\python\python.exe" "D:\QClawX\data\workspace-ua58rsb93veqtxl7\hermes-cli-test.py" "你的问题"
```

## 下一步建议

1. **短期**：用 CLI 方案满足需求
2. **长期**：联系 QClaw 官方集成 Hermes 角色到 OpenClaw 消息总线
