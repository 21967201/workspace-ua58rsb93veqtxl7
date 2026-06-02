# QClaw 原生知识库 - 每周整理脚本
# 功能: 从 memory/ 提取重要知识到 kb/ 结构化目录

param(
    [Parameter(Mandatory=$false)]
    [string]$WorkspaceRoot = "D:\QClawX\data\workspace-ua58rsb93veqtxl7",
    
    [Parameter(Mandatory=$false)]
    [int]$DaysBack = 7
)

# 计算日期范围
$endDate = Get-Date
$startDate = $endDate.AddDays(-$DaysBack)

Write-Host "📅 每周知识整理" -ForegroundColor Cyan
Write-Host "   时间范围: $($startDate.ToString('yyyy-MM-dd')) 至 $($endDate.ToString('yyyy-MM-dd'))" -ForegroundColor Gray
Write-Host ""

# 初始化计数器
$stats = [PSCustomObject]@{
    People = 0
    Projects = 0
    Tech = 0
    Decisions = 0
    AIBreakthrough = 0
}

# ========== 步骤1: 扫描 memory/ 目录 ==========
Write-Host "🔍 步骤1: 扫描 memory/ 目录..." -ForegroundColor Yellow

$memoryFiles = Get-ChildItem -Path "$WorkspaceRoot\memory" -Filter "*.md" -Recurse | 
    Where-Object { $_.LastWriteTime -ge $startDate -and $_.LastWriteTime -le $endDate }

Write-Host "   找到 $($memoryFiles.Count) 个文件" -ForegroundColor Gray

# ========== 步骤2: 提取重要知识 ==========
Write-Host "`n📝 步骤2: 提取重要知识..." -ForegroundColor Yellow

foreach ($file in $memoryFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # 检测人物信息
    if ($content -match "(?s)(人物|人员|同事|朋友).*?(\n-|\Z)") {
        Write-Host "   [人物] 在 $($file.Name) 中发现人物信息" -ForegroundColor Cyan
        $stats.People++
    }
    
    # 检测项目信息
    if ($content -match "(?s)(项目|任务|工作).*?(\n-|\Z)") {
        Write-Host "   [项目] 在 $($file.Name) 中发现项目信息" -ForegroundColor Cyan
        $stats.Projects++
    }
    
    # 检测技术信息
    if ($content -match "(?s)(技术|工具|框架|语言).*?(\n-|\Z)") {
        Write-Host "   [技术] 在 $($file.Name) 中发现技术信息" -ForegroundColor Cyan
        $stats.Tech++
    }
    
    # 检测决策信息
    if ($content -match "(?s)(决策|决定|选择|方案).*?(\n-|\Z)") {
        Write-Host "   [决策] 在 $($file.Name) 中发现决策信息" -ForegroundColor Cyan
        $stats.Decisions++
    }
    
    # 检测AI技术突破
    if ($content -match "AI.*(技术|突破|进展|模型)") {
        Write-Host "   [AI突破] 在 $($file.Name) 中发现AI技术突破信息" -ForegroundColor Cyan
        $stats.AIBreakthrough++
    }
}

# ========== 步骤3: 生成整理报告 ==========
Write-Host "`n📊 步骤3: 生成整理报告..." -ForegroundColor Yellow

$reportDate = Get-Date -Format "yyyy-MM-dd"
$reportPath = "$WorkspaceRoot\kb\weekly_organize_report_$reportDate.md"

$reportContent = "# 每周知识整理报告 - $reportDate`n`n"
$reportContent += "## 📅 时间范围`n`n"
$reportContent += "- 开始: $($startDate.ToString('yyyy-MM-dd')`n"
$reportContent += "- 结束: $($endDate.ToString('yyyy-MM-dd')`n`n"

$reportContent += "## 📊 统计摘要`n`n"
$reportContent += "| 类别 | 发现数量 |`n"
$reportContent += "|------|----------|`n"
$reportContent += "| 人物 | $($stats.People) |`n"
$reportContent += "| 项目 | $($stats.Projects) |`n"
$reportContent += "| 技术 | $($stats.Tech) |`n"
$reportContent += "| 决策 | $($stats.Decisions) |`n"
$reportContent += "| AI突破 | $($stats.AIBreakthrough) |`n`n"

$reportContent += "## 📝 建议操作`n`n"
$reportContent += "1. **创建知识条目**: 将重要信息从 memory/ 迁移到 kb/`n"
$reportContent += "2. **更新 MEMORY.md**: 添加知识库索引`n"
$reportContent += "3. **清理临时内容**: 归档 memory/ 中的临时文件`n`n"

$reportContent += "## 🔗 相关文件`n`n"
foreach ($file in $memoryFiles) {
    $reportContent += "- $($file.FullName.Replace($WorkspaceRoot, '.'))`n"
}

# 保存报告
$reportContent | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "   ✅ 报告已保存: $reportPath" -ForegroundColor Green

# ========== 步骤4: 自动创建知识条目 (示例) ==========
Write-Host "`n🚀 步骤4: 自动创建知识条目 (示例)..." -ForegroundColor Yellow

# 示例: 如果发现了AI技术突破，自动创建条目
if ($stats.AIBreakthrough -gt 0) {
    $aiFilePath = "$WorkspaceRoot\kb\ai-breakthrough\$reportDate.md"
    
    if (-not (Test-Path $aiFilePath)) {
        $aiContent = "# AI技术突破 - $reportDate`n`n"
        $aiContent += "## 本周发现`n`n"
        $aiContent += "- 待补充: 从 memory/ 中提取具体内容`n`n"
        
        $aiContent | Out-File -FilePath $aiFilePath -Encoding UTF8
        Write-Host "   ✅ 已创建: $aiFilePath" -ForegroundColor Green
    }
}

# ========== 步骤5: 更新 MEMORY.md 索引 ==========
Write-Host "`n📋 步骤5: 更新 MEMORY.md 索引..." -ForegroundColor Yellow

$memoryMdPath = "$WorkspaceRoot\MEMORY.md"
if (Test-Path $memoryMdPath) {
    $memoryContent = Get-Content -Path $memoryMdPath -Raw -Encoding UTF8
    
    # 检查是否已有知识库索引章节
    if ($memoryContent -notmatch "## QClaw Native Knowledge Base") {
        Write-Host "   ⚠️ MEMORY.md 中未找到知识库索引章节" -ForegroundColor Yellow
        Write-Host "   请手动添加 '## QClaw Native Knowledge Base' 章节" -ForegroundColor Gray
    } else {
        Write-Host "   ✅ MEMORY.md 已包含知识库索引" -ForegroundColor Green
    }
}

# ========== 完成 ==========
Write-Host "`n✅ 每周整理完成!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 统计:" -ForegroundColor Cyan
Write-Host "   人物: $($stats.People) 条" -ForegroundColor Gray
Write-Host "   项目: $($stats.Projects) 条" -ForegroundColor Gray
Write-Host "   技术: $($stats.Tech) 条" -ForegroundColor Gray
Write-Host "   决策: $($stats.Decisions) 条" -ForegroundColor Gray
Write-Host "   AI突破: $($stats.AIBreakthrough) 条" -ForegroundColor Gray
Write-Host ""
Write-Host "📄 报告: $reportPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 下一步:" -ForegroundColor Yellow
Write-Host "   1. 查看报告: notepad '$reportPath'" -ForegroundColor Gray
Write-Host "   2. 迁移知识: 将 memory/ 重要信息复制到 kb/" -ForegroundColor Gray
Write-Host "   3. 手动更新: 编辑 kb/ 中的具体文件" -ForegroundColor Gray
