# QClaw Skills清理脚本
# 执行前请确保已备份: D:\QClawX\data\.qclaw\skills-backup-full

Write-Host "=== QClaw Performance Optimization ===" -ForegroundColor Green
Write-Host "开始时间: $(Get-Date)" -ForegroundColor Gray

# 1. 定义核心Skills (保留这30个)
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

# 2. 获取所有Skills
$skillsPath = "D:\QClawX\data\.qclaw\skills"
$allSkills = Get-ChildItem $skillsPath -Directory

Write-Host "`n当前Skills总数: $($allSkills.Count)" -ForegroundColor Cyan
Write-Host "核心Skills数量: $($coreSkills.Count)" -ForegroundColor Green
Write-Host "可清理Skills数量: $($allSkills.Count - $coreSkills.Count)`n" -ForegroundColor Red

# 3. 显示将要清理的Skills
$toRemove = $allSkills | Where-Object { $coreSkills -notcontains $_.Name }
Write-Host "--- 将要清理的Skills (共 $($toRemove.Count) 个) ---" -ForegroundColor Yellow
foreach ($skill in $toRemove) {
    $days = [math]::Round((Get-Date) - $skill.LastWriteTime).TotalDays)
    Write-Host "  [×] $($skill.Name) ($([math]::Round($skill.LastWriteTime)) 天未修改)" -ForegroundColor Red
}

# 4. 确认执行
Write-Host "`n是否执行清理? (Y/N)" -ForegroundColor Yellow
$confirm = Read-Host
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "已取消清理操作" -ForegroundColor Gray
    exit
}

# 5. 执行清理
$backupPath = "D:\QClawX\data\.qclaw\skills-backup-$(Get-Date -Format 'yyyyMMdd-HHmm')"
Write-Host "`n创建额外备份: $backupPath" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

$removedCount = 0
foreach ($skill in $toRemove) {
    # 备份到时间戳目录
    Copy-Item $skill.FullName "$backupPath\" -Recurse -Force
    
    # 删除
    Remove-Item $skill.FullName -Recurse -Force
    
    Write-Host "  ✓ 已移除: $($skill.Name)" -ForegroundColor Green
    $removedCount++
}

# 6. 显示结果
Write-Host "`n=== 清理完成 ===" -ForegroundColor Green
Write-Host "移除Skills数量: $removedCount" -ForegroundColor Cyan
Write-Host "保留Skills数量: $((Get-ChildItem $skillsPath -Directory).Count)" -ForegroundColor Green
Write-Host "备份位置: $backupPath" -ForegroundColor Gray
Write-Host "`n建议下一步:" -ForegroundColor Yellow
Write-Host "1. 重启QClaw" -ForegroundColor Yellow
Write-Host "2. 观察性能是否提升" -ForegroundColor Yellow
Write-Host "3. 如需要,可从备份恢复: $backupPath" -ForegroundColor Yellow

Write-Host "`n完成时间: $(Get-Date)" -ForegroundColor Gray
