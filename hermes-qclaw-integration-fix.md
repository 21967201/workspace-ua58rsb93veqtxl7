# QClaw Hermes 集成修复（最终版本）

## 问题诊断

**真正根因**：QClaw 捆绑了自己的 Hermes 安装，但配置目录缺少关键文件。

### 目录结构

```
QClaw 捆绑 Hermes:
  D:\QClaw\v0.2.35.624\resources\hermes\
    ├── .hermes\              ← 配置目录（原来只有 plugins，缺少 config.yaml 和 .env）
    ├── libs\                 ← Python 库（完整）
    ├── plugins\              ← 插件目录
    └── skills\               ← 技能目录

独立安装的 Hermes:
  C:\Users\Administrator\.hermes\
    ├── config.yaml           ← 有配置
    ├── .env                  ← 有 API key
    └── profiles\             ← 有 profile
```

## 修复操作

### 已执行

1. **备份原配置目录**
   ```
   D:\QClaw\v0.2.35.624\resources\hermes\.hermes.backup.20260805-135640
   ```

2. **复制配置文件**
   - `config.yaml` → `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\`
   - `.env` → `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\`
   - `profiles\` → `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\`

### 验证结果

- ✅ Hermes 状态检查正常
- ✅ 模型调用测试正常（glm-4-flash）

## 下一步

1. **重启 QClaw**（完全退出再打开）
2. 选择 Hermes 角色，发送消息
3. 检查是否还有 `[object Object]` 错误

## 文件位置

| 路径 | 用途 |
|---|---|
| `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\` | QClaw Hermes 配置目录（已修复） |
| `C:\Users\Administrator\.hermes\` | 独立安装的 Hermes（已修复） |

## 注意事项

- QClaw 的 Hermes 集成现在使用捆绑的 Hermes，配置已复制
- 如果 QClaw 有自动更新，可能需要重新复制配置
- 建议将配置同步脚本添加到 QClaw 启动流程
