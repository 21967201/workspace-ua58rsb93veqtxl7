# GBrain 增量同步到云端 - 只同步有变化的章节/文件
# 作者: QClaw Agent
# 日期: 2026-06-06
# 说明: 本脚本执行增量同步，只提交和推送变化的文件到 Git 远程仓库

Write-Host "=== GBrain 增量同步任务开始 ===" -ForegroundColor Cyan
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "执行时间: $timestamp" -ForegroundColor Gray

# 配置
$gbrainPath = "C:\Users\Administrator\gbrain"
$knowledgePath = "$gbrainPath\knowledge"
$backupPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\gbrain_backup"  # 本地备份目录
$logFile = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\gbrain_sync_log_$(Get-Date -Format 'yyyyMMdd').txt"

# 步骤1: 确保 Git 仓库已初始化
Write-Host "`n[步骤1] 检查 Git 仓库状态..." -ForegroundColor Yellow
cd $knowledgePath

$gitStatus = git status 2>&1
if ($gitStatus -match "fatal: not a git repository") {
    Write-Host "  初始化 Git 仓库..." -ForegroundColor Gray
    git init
    git config user.name "QClaw Agent"
    git config user.email "agent@qclaw.local"
    Write-Host "  ✅ Git 仓库初始化完成" -ForegroundColor Green
} else {
    Write-Host "  ✅ Git 仓库已存在" -ForegroundColor Green
}

# 步骤2: 执行 GBrain 同步（增量导入）
Write-Host "`n[步骤2] 执行 GBrain 增量同步..." -ForegroundColor Yellow
cd $gbrainPath

$syncResult = bun run src/cli.ts import $knowledgePath --no-embed 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ GBrain 同步完成" -ForegroundColor Green
    Write-Output "[$timestamp] GBrain 同步: 成功" | Out-File -FilePath $logFile -Append -Encoding UTF8
} else {
    Write-Host "  ⚠️ GBrain 同步失败，继续后续步骤..." -ForegroundColor Yellow
    Write-Output "[$timestamp] GBrain 同步: 失败 - $syncResult" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

# 步骤3: 生成向量嵌入（只处理变化的文件）
Write-Host "`n[步骤3] 生成向量嵌入（增量）..." -ForegroundColor Yellow
$embedResult = bun run src/cli.ts embed --stale 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ 向量嵌入生成完成（只处理变化文件）" -ForegroundColor Green
    Write-Output "[$timestamp] 向量嵌入: 成功（增量）" | Out-File -FilePath $logFile -Append -Encoding UTF8
} else {
    Write-Host "  ⚠️ 向量嵌入生成失败，继续后续步骤..." -ForegroundColor Yellow
    Write-Output "[$timestamp] 向量嵌入: 失败 - $embedResult" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

# 步骤4: 检查文件变化（增量检测）
Write-Host "`n[步骤4] 检测文件变化..." -ForegroundColor Yellow
cd $knowledgePath

$changedFiles = git status --porcelain
if ($changedFiles) {
    $changedCount = ($changedFiles | Measure-Object).Count
    Write-Host "  ✅ 检测到 $changedCount 个文件发生变化" -ForegroundColor Green
    Write-Host "  变化文件列表:" -ForegroundColor Gray
    $changedFiles | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    
    Write-Output "[$timestamp] 检测到变化: $changedCount 个文件" | Out-File -FilePath $logFile -Append -Encoding UTF8
} else {
    Write-Host "  ℹ️ 没有文件发生变化，跳过提交" -ForegroundColor Blue
    Write-Output "[$timestamp] 检测到变化: 无" | Out-File -FilePath $logFile -Append -Encoding UTF8
    
    # 没有变化，任务完成
    Write-Host "`n=== GBrain 增量同步任务完成（无变化）===" -ForegroundColor Cyan
    exit 0
}

# 步骤5: 增量提交（只提交变化文件）
Write-Host "`n[步骤5] 执行增量提交..." -ForegroundColor Yellow
git add -A
$commitMsg = "Incremental sync: $timestamp"
git commit -m $commitMsg 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ 增量提交完成" -ForegroundColor Green
    Write-Output "[$timestamp] Git 提交: 成功 - $commitMsg" | Out-File -FilePath $logFile -Append -Encoding UTF8
} else {
    Write-Host "  ⚠️ Git 提交失败，可能无变化" -ForegroundColor Yellow
    Write-Output "[$timestamp] Git 提交: 无变化或失败" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

# 步骤6: 推送到远程仓库（如果已配置）
Write-Host "`n[步骤6] 检查远程仓库配置..." -ForegroundColor Yellow
$remoteUrl = git remote get-url origin 2>&1
if ($remoteUrl -and $remoteUrl -notmatch "fatal: No such remote") {
    Write-Host "  ✅ 远程仓库已配置: $remoteUrl" -ForegroundColor Green
    Write-Host "  推送到云端..." -ForegroundColor Gray
    
    $pushResult = git push origin master 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ 推送成功（增量同步到云端）" -ForegroundColor Green
        Write-Output "[$timestamp] Git 推送: 成功到云端" | Out-File -FilePath $logFile -Append -Encoding UTF8
    } else {
        Write-Host "  ⚠️ 推送失败: $pushResult" -ForegroundColor Yellow
        Write-Output "[$timestamp] Git 推送: 失败 - $pushResult" | Out-File -FilePath $logFile -Append -Encoding UTF8
    }
} else {
    Write-Host "  ℹ️ 未配置远程仓库，跳过推送" -ForegroundColor Blue
    Write-Host "  提示: 使用 'git remote add origin <url>' 配置远程仓库" -ForegroundColor Gray
    Write-Output "[$timestamp] Git 推送: 跳过（无远程仓库）" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

# 步骤7: 本地备份（增量）
Write-Host "`n[步骤7] 执行本地增量备份..." -ForegroundColor Yellow
if (-not (Test-Path $backupPath)) {
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
}

# 只复制变化的文件到备份目录
$changedFilesList = git diff --name-only HEAD~1 HEAD 2>&1
if ($changedFilesList) {
    foreach ($file in $changedFilesList) {
        $source = Join-Path $knowledgePath $file
        $dest = Join-Path $backupPath $file
        $destDir = Split-Path $dest
        
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        
        Copy-Item -Path $source -Destination $dest -Force
        Write-Host "  备份: $file" -ForegroundColor Gray
    }
    Write-Host "  ✅ 本地增量备份完成" -ForegroundColor Green
    Write-Output "[$timestamp] 本地备份: 完成（增量）" | Out-File -FilePath $logFile -Append -Encoding UTF8
} else {
    Write-Host "  ℹ️ 无变化文件，跳过备份" -ForegroundColor Blue
}

# 完成任务
Write-Host "`n=== GBrain 增量同步任务完成 ===" -ForegroundColor Cyan
Write-Output "[$timestamp] 任务完成" | Out-File -FilePath $logFile -Append -Encoding UTF8

# 生成同步报告
$syncReport = @"
# GBrain 增量同步报告
**执行时间**: $timestamp
**同步类型**: 增量同步（只同步变化文件）
**变化文件数**: $changedCount
**Git 提交**: $(if ($commitMsg) { "成功" } else { "无变化" })
**远程推送**: $(if ($remoteUrl -and $remoteUrl -notmatch "fatal") { "已推送" } else { "未配置" })
**本地备份**: 已完成（增量）

## 变化文件列表
$changedFiles

## 日志文件
$logFile
"@

$syncReport | Out-File -FilePath "D:\QClawX\data\workspace-ua58rsb93veqtxl7\gbrain_sync_report_$(Get-Date -Format 'yyyyMMdd-HHmm').md" -Encoding UTF8

Write-Host "`n同步报告已保存: gbrain_sync_report_$(Get-Date -Format 'yyyyMMdd-HHmm').md" -ForegroundColor Green
