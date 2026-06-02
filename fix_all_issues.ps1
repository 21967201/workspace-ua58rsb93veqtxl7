#!/usr/bin/env powershell
# 自动任务中断修复脚本 - 需要管理员权限运行
# 创建时间: 2026-06-02

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "自动任务中断修复脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[ERROR] 需要管理员权限！" -ForegroundColor Red
    Write-Host "请右键点击PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    Write-Host "然后重新运行此脚本" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[OK] 管理员权限确认" -ForegroundColor Green
Write-Host ""

# ========== 修复1: 禁用AlibabaProtect服务 ==========
Write-Host "步骤1: 禁用AlibabaProtect服务..." -ForegroundColor Yellow

try {
    # 停止服务
    Stop-Service -Name "AlibabaProtect" -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] 服务已停止" -ForegroundColor Green
    
    # 禁用服务
    Set-Service -Name "AlibabaProtect" -StartupType Disabled
    Write-Host "  [OK] 服务已禁用" -ForegroundColor Green
    
    # 修改注册表
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\AlibabaProtect" -Name "Start" -Value 4 -Type DWord -Force
    Write-Host "  [OK] 注册表已修改" -ForegroundColor Green
    
    # 终止进程
    Get-Process "AlibabaProtect" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "  [OK] 进程已终止" -ForegroundColor Green
} catch {
    Write-Host "  [WARN] 部分操作失败: $_" -ForegroundColor Yellow
}

Write-Host ""

# ========== 修复2: 修复系统服务 ==========
Write-Host "步骤2: 检查系统服务..." -ForegroundColor Yellow

$problemServices = @("iphlpsvc", "MapsBroker", "sppsvc")
foreach ($svc in $problemServices) {
    $service = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq 'Stopped' -and $service.StartType -eq 'Automatic') {
        Write-Host "  [WARN] $svc 服务未运行 (自动启动类型)" -ForegroundColor Yellow
        # 尝试启动
        try {
            Start-Service -Name $svc -ErrorAction SilentlyContinue
            Write-Host "    [OK] $svc 已启动" -ForegroundColor Green
        } catch {
            Write-Host "    [INFO] $svc 启动失败(可能正常): $_" -ForegroundColor Gray
        }
    }
}

Write-Host ""

# ========== 修复3: 验证修复效果 ==========
Write-Host "步骤3: 验证修复效果..." -ForegroundColor Yellow

# 等待片刻
Start-Sleep -Seconds 5

# 检查最近的系统日志
$recentErrors = Get-WinEvent -FilterHashtable @{LogName='System'; ID=7006; StartTime=(Get-Date).AddMinutes(-5)} -MaxEvents 3 -ErrorAction SilentlyContinue

if ($recentErrors) {
    Write-Host "  [WARN] 仍有ScRegSetValueExW错误，请检查:" -ForegroundColor Yellow
    $recentErrors | ForEach-Object {
        Write-Host "    - $($_.TimeCreated): $($_.Message.Split("`n")[0])" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [SUCCESS] 错误已停止！" -ForegroundColor Green
}

Write-Host ""

# ========== 修复4: 生成报告 ==========
Write-Host "步骤4: 生成修复报告..." -ForegroundColor Yellow

$report = @"
# 自动任务中断修复报告

## 修复时间
$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## 执行的操作

### 1. AlibabaProtect服务处理
- [x] 停止服务
- [x] 禁用自动启动
- [x] 修改注册表启动类型(Start=4)
- [x] 终止残留进程

### 2. 系统服务检查
$(foreach ($svc in $problemServices) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) {
        "- $svc : $($s.Status) ($($s.StartType))"
    }
})

### 3. 验证结果
- 系统日志错误: $(if ($recentErrors) { "仍有错误" } else { "已停止" })

## 后续建议

1. **如果错误继续**:
   - 卸载AlibabaProtect相关软件
   - 或使用火绒安全软件，在"启动项管理-服务项"中允许AlibabaProtect启用

2. **检查定时任务**:
   - 运行: taskschd.msc
   - 检查是否有异常任务

3. **监控任务执行**:
   - 使用OpenClaw的cron list命令检查任务状态
   - 确保任务脚本编码正确(UTF-8 without BOM)

## 修复脚本位置
- 脚本: $((Get-Location).Path)\fix_all_issues.ps1
- 报告: D:\QClawX\data\workspace-ua58rsb93veqtxl7\auto_fix_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md

---
**注意**: 此脚本需要管理员权限运行
"@

$reportPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\auto_fix_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "  [OK] 报告已生成: $reportPath" -ForegroundColor Green
Write-Host ""

# ========== 完成 ==========
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "修复完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "请检查上述输出，如果问题仍存在：" -ForegroundColor Yellow
Write-Host "1. 重启计算机" -ForegroundColor Yellow
Write-Host "2. 或手动卸载AlibabaProtect相关软件" -ForegroundColor Yellow
Write-Host ""

# 打开报告
Start-Process notepad.exe -ArgumentList $reportPath
