# QClaw Skills自动清理脚本 (无交互版)
# 用途: 自动清理不常用的skills以优化性能

$skillsPath = "D:\QClawX\data\.qclaw\skills"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = "D:\QClawX\data\.qclaw\skills-backup-$timestamp"

# 核心Skills - 必须保留
$coreSkills = @(
    "1688-sourcing-agent",
    "1688-product-search",
    "1688-product-analysis",
    "search-1688-supplier",
    "inquiry-1688",
    "tencent-docs",
    "mcporter",
    "ima",
    "pdf",
    "docx",
    "xlsx",
    "pptx",
    "online-search",
    "multi-search-engine",
    "skillhub-install",
    "qclaw-env",
    "email-skill",
    "imap-smtp-email",
    "file-manager",
    "web-fetch",
    "browser",
    "ai-engineer",
    "playwright",
    "mcp-builder",
    "token-optimization",
    "context-compression",
    "memory-system",
    "persona-switch",
    "openclaw-evolution-researcher"
)

Write-Host "=== QClaw Skills自动清理 ===" -ForegroundColor Green
Write-Host "开始时间: $(Get-Date)" -ForegroundColor Gray

# 获取所有Skills
$allSkills = Get-ChildItem $skillsPath -Directory
$totalSkills = $allSkills.Count
$coreCount = $coreSkills.Count

Write-Host "`n当前Skills总数: $totalSkills" -ForegroundColor Cyan
Write-Host "核心Skills数量: $coreCount" -ForegroundColor Green

# 找出需要清理的Skills
$skillsToRemove = @()
foreach ($skill in $allSkills) {
    if ($coreSkills -notcontains $skill.Name) {
        $skillsToRemove += $skill
    }
}

$removeCount = $skillsToRemove.Count
Write-Host "可清理Skills数量: $removeCount" -ForegroundColor Red

if ($removeCount -eq 0) {
    Write-Host "`n✓ 无需清理，已是最优状态" -ForegroundColor Green
    exit
}

# 创建备份目录
Write-Host "`n--- 步骤1: 创建备份 ---" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
Write-Host "✓ 备份目录已创建: $backupPath" -ForegroundColor Green

# 执行备份和清理
Write-Host "`n--- 步骤2: 备份并清理Skills ---" -ForegroundColor Yellow
$removed = 0

foreach ($skill in $skillsToRemove) {
    # 备份
    $destPath = Join-Path $backupPath $skill.Name
    Copy-Item $skill.FullName $destPath -Recurse -Force
    
    # 删除
    Remove-Item $skill.FullName -Recurse -Force
    
    $removed++
    Write-Host "  [$removed/$removeCount] 已移除: $($skill.Name)" -ForegroundColor Green
}

# 显示结果
Write-Host "`n=== 清理完成 ===" -ForegroundColor Green
Write-Host "移除Skills数量: $removed" -ForegroundColor Cyan
Write-Host "保留Skills数量: $((Get-ChildItem $skillsPath -Directory).Count)" -ForegroundColor Green
Write-Host "备份位置: $backupPath" -ForegroundColor Gray

Write-Host "`n--- 下一步操作建议 ---" -ForegroundColor Yellow
Write-Host "1. 重启QClaw使配置生效" -ForegroundColor Yellow
Write-Host "2. 观察性能是否提升 (预期提升50-70%)" -ForegroundColor Yellow
Write-Host "3. 如有问题，从备份恢复: $backupPath" -ForegroundColor Yellow

Write-Host "`n完成时间: $(Get-Date)" -ForegroundColor Gray
Write-Host "`n✓ 清理完成！请重启QClaw。" -ForegroundColor Green
