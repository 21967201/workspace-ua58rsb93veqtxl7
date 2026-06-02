# 修复验证脚本 - 运行此脚本检查修复效果
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "自动任务修复 - 验证脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查AlibabaProtect服务
Write-Host "1. 检查AlibabaProtect服务..." -ForegroundColor Yellow
$service = Get-Service "AlibabaProtect" -ErrorAction SilentlyContinue
if ($service) {
    Write-Host "   名称: $($service.Name)" -ForegroundColor Gray
    Write-Host "   状态: $($service.Status)" -ForegroundColor $(if ($service.Status -eq 'Stopped') { 'Green' } else { 'Yellow' })
    Write-Host "   启动类型: $($service.StartType)" -ForegroundColor $(if ($service.StartType -eq 'Disabled') { 'Green' } else { 'Yellow' })
} else {
    Write-Host "   [SUCCESS] 服务不存在（可能已卸载）" -ForegroundColor Green
}
Write-Host ""

# 2. 检查系统日志错误
Write-Host "2. 检查系统日志错误（最近10分钟）..." -ForegroundColor Yellow
$errors = Get-WinEvent -FilterHashtable @{LogName='System'; ID=7006; StartTime=(Get-Date).AddMinutes(-10)} -MaxEvents 5 -ErrorAction SilentlyContinue
if ($errors) {
    Write-Host "   [WARN] 仍有 $($errors.Count) 个错误" -ForegroundColor Yellow
    $errors | ForEach-Object { Write-Host "   - $($_.TimeCreated): $($_.Message.Split("`n")[0])" -ForegroundColor Yellow }
} else {
    Write-Host "   [SUCCESS] 无错误！修复成功！" -ForegroundColor Green
}
Write-Host ""

# 3. 检查cron任务状态
Write-Host "3. 检查cron任务状态..." -ForegroundColor Yellow
Write-Host "   （需要OpenClaw cron工具检查）" -ForegroundColor Gray
Write-Host ""

# 4. 提供建议
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "建议：" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 如果仍有错误，请以管理员身份运行：" -ForegroundColor Yellow
Write-Host "   D:\QClawX\data\workspace-ua58rsb93veqtxl7\fix_all_issues.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 或者手动禁用AlibabaProtect服务：" -ForegroundColor Yellow
Write-Host "   - 打开火绒安全软件" -ForegroundColor Gray
Write-Host "   - 启动项管理 -> 服务项" -ForegroundColor Gray
Write-Host "   - 允许启用 AlibabaProtect" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 检查JSON文件编码：" -ForegroundColor Yellow
Write-Host "   cd D:\QClawX\data\workspace\skills\today-task\scripts" -ForegroundColor Gray
Write-Host "   python fix_json_encoding.py --all" -ForegroundColor Gray
Write-Host ""
