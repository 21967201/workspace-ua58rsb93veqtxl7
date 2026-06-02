#!/usr/bin/env pwsh
# GBrain 全景管理任务 - 2026-06-01 (周一)
# 执行所有6个步骤并生成报告

$ErrorActionPreference = "Stop"
$date = Get-Date -Format "yyyy-MM-dd"
$reportDir = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
$reports = @()

Write-Host "=== GBrain 全景管理任务开始 - $date ===" -ForegroundColor Green

# 步骤1：GBrain Auto Import
Write-Host "`n[步骤1/6] 执行 GBrain Auto Import..." -ForegroundColor Cyan
try {
    $importResult = & gbrain import --auto 2>&1
    $importReport = "gbrain_auto_import_$date.md"
    $importContent = "# GBrain Auto Import 报告 - $date`n`n## 执行结果`n`n```````n$importResult`n```````n"
    $importContent | Out-File -FilePath (Join-Path $reportDir $importReport) -Encoding UTF8
    $reports += "✅ 步骤1完成: $importReport"
    Write-Host "完成: $importReport" -ForegroundColor Green
} catch {
    $reports += "❌ 步骤1失败: $_"
    Write-Host "失败: $_" -ForegroundColor Red
}

# 步骤2：GBrain Tier1 Enrichment
Write-Host "`n[步骤2/6] 执行 GBrain Tier1 Enrichment..." -ForegroundColor Cyan
try {
    $tier1Result = & gbrain enrich --tier=1 2>&1
    $tier1Report = "gbrain_tier1_report_$date.md"
    $tier1Content = "# GBrain Tier1 Enrichment 报告 - $date`n`n## 执行结果`n`n```````n$tier1Result`n```````n"
    $tier1Content | Out-File -FilePath (Join-Path $reportDir $tier1Report) -Encoding UTF8
    $reports += "✅ 步骤2完成: $tier1Report"
    Write-Host "完成: $tier1Report" -ForegroundColor Green
} catch {
    $reports += "❌ 步骤2失败: $_"
    Write-Host "失败: $_" -ForegroundColor Red
}

# 步骤3：Memory Dreaming Promotion
Write-Host "`n[步骤3/6] 执行 Memory Dreaming Promotion..." -ForegroundColor Cyan
try {
    $dreamResult = & gbrain dream --promotion 2>&1
    $dreamReport = "gbrain_dream_report_$date.md"
    $dreamContent = "# Memory Dreaming Promotion 报告 - $date`n`n## 执行结果`n`n```````n$dreamResult`n```````n"
    $dreamContent | Out-File -FilePath (Join-Path $reportDir $dreamReport) -Encoding UTF8
    $reports += "✅ 步骤3完成: $dreamReport"
    Write-Host "完成: $dreamReport" -ForegroundColor Green
} catch {
    $reports += "❌ 步骤3失败: $_"
    Write-Host "失败: $_" -ForegroundColor Red
}

# 步骤4：GBrain Dream Cycle
Write-Host "`n[步骤4/6] 执行 GBrain Dream Cycle..." -ForegroundColor Cyan
try {
    $cycleResult = & gbrain cycle --dream 2>&1
    $cycleReport = "gbrain_cycle_report_$date.md"
    $cycleContent = "# GBrain Dream Cycle 报告 - $date`n`n## 执行结果`n`n```````n$cycleResult`n```````n"
    $cycleContent | Out-File -FilePath (Join-Path $reportDir $cycleReport) -Encoding UTF8
    $reports += "✅ 步骤4完成: $cycleReport"
    Write-Host "完成: $cycleReport" -ForegroundColor Green
} catch {
    $reports += "❌ 步骤4失败: $_"
    Write-Host "失败: $_" -ForegroundColor Red
}

# 步骤5：GBrain Tier2 Enrichment（仅周一执行）
$isMonday = (Get-Date).DayOfWeek -eq "Monday"
if ($isMonday) {
    Write-Host "`n[步骤5/6] 执行 GBrain Tier2 Enrichment (周一)..." -ForegroundColor Cyan
    try {
        $tier2Result = & gbrain enrich --tier=2 2>&1
        $tier2Report = "gbrain_tier2_report_$date.md"
        $tier2Content = "# GBrain Tier2 Enrichment 报告 - $date (周一)`n`n## 执行结果`n`n```````n$tier2Result`n```````n"
        $tier2Content | Out-File -FilePath (Join-Path $reportDir $tier2Report) -Encoding UTF8
        $reports += "✅ 步骤5完成: $tier2Report (周一)"
        Write-Host "完成: $tier2Report" -ForegroundColor Green
    } catch {
        $reports += "❌ 步骤5失败: $_"
        Write-Host "失败: $_" -ForegroundColor Red
    }
} else {
    $reports += "⏭️ 步骤5跳过: 今天不是周一"
    Write-Host "跳过: 今天不是周一" -ForegroundColor Yellow
}

# 步骤6：AI技术突破信息每周更新（仅周一执行）
if ($isMonday) {
    Write-Host "`n[步骤6/6] 执行 AI技术突破信息更新 (周一)..." -ForegroundColor Cyan
    
    # 这里需要调用在线搜索，但 exec 工具不能直接调用 message 工具
    # 所以先创建一个占位符，稍后手动执行搜索
    $aiReport = "ai-tech-breakthrough_$date.md"
    $aiContent = "# AI技术突破信息 - $date (周一)`n`n## 待完成`n`n需要执行以下搜索：`n1. '2026年6月 AI 大模型 技术突破 最新进展' (freshness=30d)`n2. '2026年6月 AI Agent 技术突破 自主规划 多模态' (freshness=30d)`n`n请手动执行搜索并更新此文件。`n"
    $aiContent | Out-File -FilePath (Join-Path $reportDir $aiReport) -Encoding UTF8
    $reports += "⚠️ 步骤6部分完成: $aiReport (需要手动搜索)"
    Write-Host "部分完成: $aiReport (需要手动搜索)" -ForegroundColor Yellow
} else {
    $reports += "⏭️ 步骤6跳过: 今天不是周一"
    Write-Host "跳过: 今天不是周一" -ForegroundColor Yellow
}

# 生成合并报告
Write-Host "`n=== 生成合并报告 ===" -ForegroundColor Green
$combinedReport = "GBrain全景管理_$date.md"
$combinedContent = "# GBrain全景管理报告 - $date`n`n## 执行摘要`n`n"
$combinedContent += ($reports -join "`n`n") + "`n`n## 详细报告`n`n"

# 读取所有报告内容
Get-ChildItem -Path $reportDir -Filter "*$date.md" | ForEach-Object {
    $fileContent = Get-Content -Path $_.FullName -Raw -Encoding UTF8
    $combinedContent += "`n### $($_.Name)`n`n$fileContent`n`n---`n"
}

$combinedContent | Out-File -FilePath (Join-Path $reportDir $combinedReport) -Encoding UTF8

# 创建任务JSON文件
Write-Host "`n=== 创建任务JSON文件 ===" -ForegroundColor Green
$pythonScript = "D:\QClawX\data\workspace\skills\today-task\scripts\create_task_json.py"
$taskName = "GBrain全景管理"
$jsonFile = "GBrain全景管理_$date.json"

# 读取合并报告内容
$reportContent = Get-Content -Path (Join-Path $reportDir $combinedReport) -Raw -Encoding UTF8

# 调用Python脚本创建JSON
$pythonCmd = "python `"$pythonScript`" `"$taskName`" `"$reportContent`""
Invoke-Expression $pythonCmd | Out-Null

# 推送到负一屏
Write-Host "`n=== 推送到负一屏 ===" -ForegroundColor Green
$pushScript = "D:\QClawX\data\workspace\skills\today-task\scripts\task_push.py"
$pushCmd = "python `"$pushScript`" --data `"$jsonFile`""
Invoke-Expression $pushCmd

Write-Host "`n=== GBrain 全景管理任务完成 ===" -ForegroundColor Green
Write-Host "合并报告: $combinedReport" -ForegroundColor Cyan
if ($isMonday) {
    Write-Host "注意: 今天是周一，AI技术突破信息需要手动搜索更新" -ForegroundColor Yellow
}