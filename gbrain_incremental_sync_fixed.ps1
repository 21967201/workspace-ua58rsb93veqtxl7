# GBrain 增量同步到云端 - 修复版
# 功能: 只同步有变化的文件到 Git 仓库

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\gbrain_sync_log_$(Get-Date -Format 'yyyyMMdd').txt"

Write-Host "=== GBrain 增量同步任务 ===" -ForegroundColor Cyan
Write-Host "执行时间: $timestamp" -ForegroundColor Gray

# 步骤1: 检查 Git 仓库
Write-Host "`n[步骤1] 检查 Git 仓库..." -ForegroundColor Yellow
cd "C:\Users\Administrator\gbrain\knowledge"

try {
    $null = git status 2>&1
    Write-Host "  ✅ Git 仓库已存在" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️ 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
    git config user.name "QClaw Agent"
    git config user.email "agent@qclaw.local"
    Write-Host "  ✅ Git 仓库初始化完成" -ForegroundColor Green
}

# 步骤2: 执行 GBrain 增量导入
Write-Host "`n[步骤2] 执行 GBrain 增量导入..." -ForegroundColor Yellow
cd "C:\Users\Administrator\gbrain"

$importResult = bun run src/cli.ts import "C:\Users\Administrator\gbrain\knowledge" --no-embed 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ GBrain 导入完成" -ForegroundColor Green
    Add-Content -Path $logFile -Value "[$timestamp] GBrain 导入: 成功" -Encoding UTF8
} else {
    Write-Host "  ⚠️ GBrain 导入失败，继续..." -ForegroundColor Yellow
    Add-Content -Path $logFile -Value "[$timestamp] GBrain 导入: 失败" -Encoding UTF8
}

# 步骤3: 增量生成向量嵌入
Write-Host "`n[步骤3] 增量生成向量嵌入..." -ForegroundColor Yellow
$embedResult = bun run src/cli.ts embed --stale 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ 向量嵌入生成完成（只处理变化文件）" -ForegroundColor Green
    Add-Content -Path $logFile -Value "[$timestamp] 向量嵌入: 成功（增量）" -Encoding UTF8
} else {
    Write-Host "  ⚠️ 向量嵌入生成失败，继续..." -ForegroundColor Yellow
    Add-Content -Path $logFile -Value "[$timestamp] 向量嵌入: 失败" -Encoding UTF8
}

# 步骤4: 检测变化文件
Write-Host "`n[步骤4] 检测变化文件..." -ForegroundColor Yellow
cd "C:\Users\Administrator\gbrain\knowledge"

$changedFiles = git status --porcelain
if ($changedFiles) {
    $changedCount = ($changedFiles | Measure-Object).Count
    Write-Host "  ✅ 检测到 $changedCount 个变化文件" -ForegroundColor Green
    Write-Host "  变化文件:" -ForegroundColor Gray
    $changedFiles | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    
    Add-Content -Path $logFile -Value "[$timestamp] 检测到变化: $changedCount 个文件" -Encoding UTF8
} else {
    Write-Host "  ℹ️ 没有文件变化，任务完成" -ForegroundColor Blue
    Add-Content -Path $logFile -Value "[$timestamp] 检测到变化: 无" -Encoding UTF8
    Write-Host "`n=== GBrain 增量同步任务完成（无变化）===" -ForegroundColor Cyan
    exit 0
}

# 步骤5: 增量提交
Write-Host "`n[步骤5] 执行增量提交..." -ForegroundColor Yellow
git add -A
$commitMsg = "Incremental sync: $timestamp"
git commit -m $commitMsg 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ 增量提交完成" -ForegroundColor Green
    Add-Content -Path $logFile -Value "[$timestamp] Git 提交: 成功 - $commitMsg" -Encoding UTF8
} else {
    Write-Host "  ⚠️ Git 提交失败（可能无变化）" -ForegroundColor Yellow
    Add-Content -Path $logFile -Value "[$timestamp] Git 提交: 无变化或失败" -Encoding UTF8
}

# 步骤6: 推送到远程仓库
Write-Host "`n[步骤6] 检查远程仓库..." -ForegroundColor Yellow
try {
    $remoteUrl = git remote get-url origin 2>&1
    if ($remoteUrl -and $remoteUrl -notmatch "fatal") {
        Write-Host "  ✅ 远程仓库已配置: $remoteUrl" -ForegroundColor Green
        Write-Host "  推送到云端..." -ForegroundColor Gray
        
        $pushResult = git push origin master 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ 推送成功（增量同步到云端）" -ForegroundColor Green
            Add-Content -Path $logFile -Value "[$timestamp] Git 推送: 成功到云端" -Encoding UTF8
        } else {
            Write-Host "  ⚠️ 推送失败: $pushResult" -ForegroundColor Yellow
            Add-Content -Path $logFile -Value "[$timestamp] Git 推送: 失败 - $pushResult" -Encoding UTF8
        }
    } else {
        Write-Host "  ℹ️ 未配置远程仓库，跳过推送" -ForegroundColor Blue
        Write-Host "  提示: 使用 'git remote add origin <url>' 配置远程仓库" -ForegroundColor Gray
        Add-Content -Path $logFile -Value "[$timestamp] Git 推送: 跳过（无远程仓库）" -Encoding UTF8
    }
} catch {
    Write-Host "  ℹ️ 未配置远程仓库，跳过推送" -ForegroundColor Blue
    Add-Content -Path $logFile -Value "[$timestamp] Git 推送: 跳过（无远程仓库）" -Encoding UTF8
}

# 步骤7: 生成同步报告
Write-Host "`n[步骤7] 生成同步报告..." -ForegroundColor Yellow

$reportContent = @"
# GBrain 增量同步报告
**执行时间**: $timestamp
**同步类型**: 增量同步（只同步变化文件）
**变化文件数**: $changedCount
**Git 提交**: 成功
**远程推送**: $(if ($remoteUrl -and $remoteUrl -notmatch "fatal") { "已推送" } else { "未配置" })

## 变化文件列表
$changedFiles

## 日志文件
$logFile

---
*增量同步任务自动生成*
"@

$reportFile = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\gbrain_sync_report_$(Get-Date -Format 'yyyyMMdd-HHmm').md"
$reportContent | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "  ✅ 同步报告已保存: $(Split-Path $reportFile -Leaf)" -ForegroundColor Green
Add-Content -Path $logFile -Value "[$timestamp] 任务完成，报告: $reportFile" -Encoding UTF8

Write-Host "`n=== GBrain 增量同步任务完成 ===" -ForegroundColor Cyan
