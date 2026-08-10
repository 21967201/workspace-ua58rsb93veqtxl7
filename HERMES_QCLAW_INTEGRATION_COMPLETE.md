# QClaw Hermes 集成修复完成

**日期**: 2026-08-05 13:57 GMT+8
**状态**: ✅ 配置已修复，等待用户重启 QClaw 验证

---

## 问题根因

QClaw 捆绑了自己的 Hermes 安装在 `D:\QClaw\v0.2.35.624\resources\hermes\`，但配置目录：
```
D:\QClaw\v0.2.35.624\resources\hermes\.hermes\
```
**只有 plugins，缺少 config.yaml 和 .env**。

这导致：
1. Hermes 无法解析 API key → 模型调用失败
2. QClaw 降级到默认的 DeepSeek-V4-Flash
3. 前端渲染 bug 显示 `[object Object]`

---

## 修复操作

### 1. 备份原配置
```
D:\QClaw\v0.2.35.624\resources\hermes\.hermes.backup.20260805-135640
```

### 2. 复制配置
- `config.yaml` → `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\`
- `.env` → `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\`
- `profiles\` → `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\`

### 3. 配置验证
- ✅ `glm-4-flash` + `custom:zhipu` 配置正确
- ✅ `HERMES_ZHIPU_API_KEY` 已设置
- ✅ API base_url 正确：`https://open.bigmodel.cn/api/paas/v4`

---

## 架构澄清

### 两个 Hermes 安装

| 路径 | 用途 | 配置 |
|---|---|---|
| `D:\QClaw\v0.2.35.624\resources\hermes\` | QClaw 捆绑版 | 已修复 ✅ |
| `C:\Users\Administrator\.hermes\` | 独立安装版 | 已修复 ✅ |

### QClaw 的 Hermes 集成

- QClaw 使用捆绑的 Hermes（`resources\hermes\`）
- 配置目录：`resources\hermes\.hermes\`
- Python 库：`resources\hermes\libs\`
- 插件：`resources\hermes\.hermes\plugins\`

---

## 下一步

### 用户操作
1. **完全退出 QClaw**（托盘图标右键 → 退出）
2. **重新打开 QClaw**
3. 选择 Hermes 角色，发送消息
4. 检查是否还有 `[object Object]` 错误

### 验证标准
- ✅ 消息正常回复（不是 `[object Object]`）
- ✅ 底部显示模型名：`glm-4-flash`（不是 `DeepSeek-V4-Flash`）
- ✅ 响应来自智谱 API

---

## 文件清单

| 文件 | 说明 |
|---|---|
| `hermes-qclaw-integration-fix.md` | 本文件 |
| `hermes-cli-test.py` | CLI 桥接脚本（备用） |
| `hermes-fix_20260805.md` | 之前的修复记录 |
| `D:\QClaw\v0.2.35.624\resources\hermes\.hermes.backup.*` | 备份目录 |

---

## 技术细节

### 修复命令
```powershell
# 备份
Rename-Item "D:\QClaw\v0.2.35.624\resources\hermes\.hermes" ".hermes.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# 创建目录
New-Item -ItemType Directory -Path "D:\QClaw\v0.2.35.624\resources\hermes\.hermes" -Force

# 复制配置
Copy-Item "C:\Users\Administrator\.hermes\config.yaml" "D:\QClaw\v0.2.35.624\resources\hermes\.hermes\config.yaml"
Copy-Item "C:\Users\Administrator\.hermes\.env" "D:\QClaw\v0.2.35.624\resources\hermes\.hermes\.env"
```

### 验证命令
```powershell
$env:HERMES_HOME = "D:\QClaw\v0.2.35.624\resources\hermes\.hermes"
$env:PYTHONPATH = "D:\QClaw\v0.2.35.624\resources\hermes\libs"
hermes_cli -z "测试" --model glm-4-flash
```

---

*修复者：Agnes (Sapiens AI)*
*修复时间：2026-08-05 13:57 GMT+8*
