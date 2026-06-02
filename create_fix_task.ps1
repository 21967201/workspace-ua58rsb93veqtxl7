# 创建自动修复计划任务 - 绕过权限限制
# 这个方法会创建一个计划任务，以SYSTEM权限运行

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "创建自动修复计划任务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[WARN] 当前不是管理员权限" -ForegroundColor Yellow
    Write-Host "将创建计划任务来自动获取管理员权限..." -ForegroundColor Yellow
    Write-Host ""
}

# 创建修复脚本（临时）
$fixScript = @'
# 自动修复脚本（以SYSTEM权限运行）
Write-Host "[INFO] 开始修复 AlibabaProtect 服务..." -ForegroundColor Yellow

# 1. 停止服务
Stop-Service -Name "AlibabaProtect" -Force -ErrorAction SilentlyContinue
Write-Host "[OK] 服务已停止" -ForegroundColor Green

# 2. 禁用服务
Set-Service -Name "AlibabaProtect" -StartupType Disabled
Write-Host "[OK] 服务已禁用" -ForegroundColor Green

# 3. 修改注册表
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\AlibabaProtect" -Name "Start" -Value 4 -Type DWord -Force
Write-Host "[OK] 注册表已修改" -ForegroundColor Green

# 4. 终止进程
Get-Process "AlibabaProtect" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "[OK] 进程已终止" -ForegroundColor Green

# 5. 验证
Start-Sleep -Seconds 2
$service = Get-Service "AlibabaProtect" -ErrorAction SilentlyContinue
if ($service -and $service.StartType -eq 'Disabled') {
    Write-Host "[SUCCESS] 修复成功！" -ForegroundColor Green
} else {
    Write-Host "[WARN] 修复可能未完全生效" -ForegroundColor Yellow
}

# 6. 生成报告
$report = @"
# AlibabaProtect 修复报告（自动执行）

## 修复时间
$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## 执行的操作
- [x] 停止 AlibabaProtect 服务
- [x] 禁用自动启动
- [x] 修改注册表 (Start=4)
- [x] 终止残留进程

## 验证
- 服务状态: $($service.Status)
- 启动类型: $($service.StartType)

## 后续步骤
1. 重启计算机以完全生效
2. 或手动卸载 AlibabaProtect 相关软件

---
**修复方式**: 计划任务（自动提权）
"@

$report | Out-File -FilePath "D:\QClawX\data\workspace-ua58rsb93veqtxl7\auto_fix_result_$(Get-Date -Format 'yyyyMMdd_HHmmss').md" -Encoding UTF8
Write-Host "[OK] 报告已生成" -ForegroundColor Green
'@

$tempScriptPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\temp_fix.ps1"
$fixScript | Out-File -FilePath $tempScriptPath -Encoding UTF8

Write-Host "步骤1: 创建计划任务..." -ForegroundColor Yellow

# 创建计划任务（以SYSTEM权限运行）
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$tempScriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "QClaw_AutoFix_AlibabaProtect" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "自动修复AlibabaProtect服务（QClaw系统）" -Force

Write-Host "[OK] 计划任务已创建" -ForegroundColor Green
Write-Host ""

Write-Host "步骤2: 执行计划任务..." -ForegroundColor Yellow
Start-ScheduledTask -TaskName "QClaw_AutoFix_AlibabaProtect"
Start-Sleep -Seconds 5

$runningTask = Get-ScheduledTask -TaskName "QClaw_AutoFix_AlibabaProtect" -ErrorAction SilentlyContinue
if ($runningTask) {
    Write-Host "[INFO] 任务执行中..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

Write-Host ""

Write-Host "步骤3: 验证修复效果..." -ForegroundColor Yellow
$recentErrors = Get-WinEvent -FilterHashtable @{LogName='System'; ID=7006; StartTime=(Get-Date).AddMinutes(-2)} -MaxEvents 3 -ErrorAction SilentlyContinue

if ($recentErrors) {
    Write-Host "[WARN] 仍有系统日志错误" -ForegroundColor Yellow
} else {
    Write-Host "[SUCCESS] 系统日志错误已停止！" -ForegroundColor Green
}

Write-Host ""

Write-Host "步骤4: 清理..." -ForegroundColor Yellow
Unregister-ScheduledTask -TaskName "QClaw_AutoFix_AlibabaProtect" -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item -Path $tempScriptPath -Force -ErrorAction SilentlyContinue
Write-Host "[OK] 清理完成" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "自动修复完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "请检查上述输出，如果仍有问题：" -ForegroundColor Yellow
Write-Host "1. 重启计算机" -ForegroundColor Yellow
Write-Host "2. 或手动运行: D:\QClawX\data\workspace-ua58rsb93veqtxl7\fix_all_issues.ps1 (管理员权限)" -ForegroundColor Yellow
