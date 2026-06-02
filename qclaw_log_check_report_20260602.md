# QClaw 运行日志检查与修复方案
**检查时间**: 2026-06-02 10:44-11:30  
**状态**: ✅ 检查完成，方案已制定

---

## 执行摘要

已详细检查 QClaw 运行状态，发现 **4个主要问题** 导致任务中断和性能问题。以下是完整分析和修复方案。

---

## 🔴 严重问题1: Gateway 服务未运行

### 问题描述
```
Runtime: stopped (ERROR: The system cannot find the file specified.)
Service: Scheduled Task (missing)
Service not installed. Run: openclaw gateway install
```

### 根本原因
1. OpenClaw Gateway 计划任务不存在
2. Windows 上 `openclaw gateway install` 被禁用（显示 "Nix mode detected; service install is disabled"）
3. Gateway 无法以服务方式稳定运行

### 影响
- **这是导致"任务莫名其妙中断"的主要原因**
- Gateway 是 QClaw 的核心通信枢纽，未运行会导致：
  - 任务调度失败
  - 心跳检测失效
  - Agent 间通信中断

---

## 🔴 严重问题2: 多个 QClaw 进程冲突

### 问题描述
检测到 **6-7 个 QClaw.exe 进程** 同时运行，总内存占用约 2GB

### 进程列表（最近一次检查）
```
QClaw  8416  2026/6/2 10:58:13  725 MB
QClaw 24984 2026/6/2 9:51:56   571 MB
QClaw 25148 2026/6/2 9:51:56    56 MB
QClaw 25484 2026/6/2 9:52:37   118 MB
QClaw 26416 2026/6/2 10:58:06   139 MB
QClaw 28668 2026/6/2 10:58:06   471 MB
```

### 根本原因
- Gateway 未正常运行，导致每次启动新实例时创建新进程
- 缺少进程管理和去重机制
- 可能出现进程间资源竞争和文件锁冲突

### 影响
- 资源严重浪费（2GB 内存占用）
- 进程间冲突导致任务异常中断
- 文件锁冲突导致日志写入失败

---

## 🟡 中等问题3: 日志文件路径配置错误

### 问题描述
1. 配置中日志路径为相对路径: `\tmp\openclaw\openclaw-2026-06-02.log`
2. 实际路径不存在于：
   - `C:\tmp\openclaw\` ❌
   - `D:\Cache\Temp\tmp\openclaw\` ❌
   - `D:\QClawX\data\.qclaw\logs` (存在但是文件，不是目录) ❌

### 影响
- 无法追踪错误和异常
- 调试困难
- 问题排查受阻

---

## 🟢 轻微问题4: 配置文件编码问题

### 问题描述
`C:\Users\Administrator\.qclaw\openclaw.json` 中出现 UTF-8 编码显示异常
- `"鍒涗笟鍙互瀛?` 应为 `"创业可以学"`
- `"鐢靛晢鏂囨楝兼墠"` 应为 `"电商文案写作"`

### 影响
- Agent 名称显示异常
- 不影响核心功能但影响使用体验

---

## ✅ 修复方案（立即执行）

### 步骤1: 清理所有 QClaw 进程

**手动执行（PowerShell 管理员权限）**:
```powershell
# 停止所有 QClaw 进程
Get-Process QClaw | Stop-Process -Force

# 验证清理结果
Get-Process | Where-Object { $_.ProcessName -eq "QClaw" }
```

**预期结果**: 无输出（所有进程已停止）

---

### 步骤2: 手动创建 Gateway 计划任务

**手动执行（PowerShell 管理员权限）**:
```powershell
# 创建 Gateway 计划任务
$action = New-ScheduledTaskAction -Execute "D:\QClaw\v0.2.24.540\QClaw.exe" -Argument "gateway run"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "Administrator" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName "OpenClaw Gateway" -Action $action -Trigger $trigger -Principal $principal -Force

# 验证任务创建成功
schtasks /Query /TN "OpenClaw Gateway"
```

**预期结果**: 显示任务信息，状态为 "Ready"

---

### 步骤3: 启动 Gateway 服务

**手动执行**:
```powershell
# 启动 Gateway
schtasks /Run /TN "OpenClaw Gateway"

# 等待5秒后检查状态
Start-Sleep -Seconds 5
openclaw gateway status
```

**预期结果**:
```
Runtime: running
Connectivity probe: ok
Listening: 127.0.0.1:50857
```

---

### 步骤4: 修复日志路径配置

**编辑配置文件** `C:\Users\Administrator\.qclaw\openclaw.json`，添加日志配置：

```json
{
  "logging": {
    "path": "D:\\QClawX\\data\\.qclaw\\logs",
    "level": "info",
    "maxFiles": 7,
    "maxSize": "10m"
  }
}
```

**创建日志目录**:
```powershell
New-Item -ItemType Directory -Path "D:\QClawX\data\.qclaw\logs" -Force
```

---

### 步骤5: 修复配置文件编码

**手动执行**:
1. 用 VS Code 或 Notepad++ 打开 `C:\Users\Administrator\.qclaw\openclaw.json`
2. 选择 "File" → "Save with Encoding" → "UTF-8"
3. 保存文件
4. 重启 Gateway 服务

---

## 🔧 长期改进建议

### 1. 添加健康检查机制
创建定时任务，每5分钟检查 Gateway 和 Agent 状态：

```powershell
# 健康检查脚本
$gatewayStatus = openclaw gateway status 2>&1
if ($gatewayStatus -match "stopped|error") {
    Write-EventLog -LogName Application -Source "QClaw" -EntryType Error -EventId 1001 -Message "Gateway is down, attempting restart..."
    schtasks /Run /TN "OpenClaw Gateway"
}
```

### 2. 进程管理脚本
在启动新 Agent 前检查是否已有实例运行：

```powershell
$processes = Get-Process QClaw -ErrorAction SilentlyContinue
if ($processes.Count -gt 3) {
    Write-Output "警告: 检测到 $($processes.Count) 个 QClaw 进程，建议清理"
    $processes | Select-Object Name, Id, StartTime, @{Name="Memory(MB)";Expression={$_.WorkingSet / 1MB -as [int]}} | Format-Table
}
```

### 3. 统一日志管理
配置中央日志收集，便于问题排查：
- 所有 Agent 日志写入统一目录
- 配置日志轮转（保留7天）
- 错误日志实时告警

---

## ✅ 验证修复效果

执行上述修复后，运行以下命令验证：

```powershell
# 1. 检查 Gateway 状态
openclaw gateway status

# 2. 检查进程数量（应只有1-2个）
Get-Process QClaw | Measure-Object | Select-Object Count

# 3. 检查日志文件是否生成
Get-ChildItem -Path "D:\QClawX\data\.qclaw\logs" -File

# 4. 测试任务执行（创建一个测试任务）
openclaw cron add --name "test-task" --schedule "in 2 minutes" --message "Test task execution"
```

---

## 📊 问题优先级

| 问题 | 严重程度 | 影响 | 修复难度 |
|------|---------|------|---------|
| Gateway 未运行 | 🔴 高 | 任务中断 | 中 |
| 多进程冲突 | 🔴 高 | 资源浪费/冲突 | 低 |
| 日志路径错误 | 🟡 中 | 调试困难 | 低 |
| 配置编码问题 | 🟢 低 | 显示异常 | 低 |

---

## 下一步行动

1. ✅ **立即执行**: 按照上述步骤1-5手动执行修复
2. ⏳ **验证**: 执行验证命令确认修复效果
3. ⏳ **监控**: 观察24小时，确认任务不再中断
4. ⏳ **改进**: 实施长期改进建议

---

**报告完成时间**: 2026-06-02 11:30:00  
**估计修复时间**: 15-20分钟  
**预计效果**: 任务中断问题应完全解决
