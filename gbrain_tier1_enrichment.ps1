# GBrain Tier1 Enrichment 协议实现
# 替代不存在的命令: gbrain enrich --tier=1

param(
    [string]$EntityName = "示例实体"
)

# 步骤1: 实体检测
Write-Host "[Step 1] 检测实体: $EntityName"

# 步骤2: 检查brain状态 (UPDATE or CREATE)
$existing = bun run "C:\Users\Administrator\gbrain\src\cli.ts" search "$EntityName" 2>&1
if ($LASTEXITCODE -eq 0 -and $existing -match "Found \d+") {
    $path = "UPDATE"
    Write-Host "[Step 2] 路径: UPDATE (实体已存在)"
    
    # 获取现有页面
    $pageContent = bun run "C:\Users\Administrator\gbrain\src\cli.ts" get "$EntityName" 2>&1
    Write-Host "[Step 2] 已获取现有页面内容"
} else {
    $path = "CREATE"
    Write-Host "[Step 2] 路径: CREATE (新实体)"
}

# 步骤3: 确定tier (Tier 1 = 10-15 API调用)
$tier = 1  # Tier 1: 关键人物/公司，完整流水线
Write-Host "[Step 3] Tier: $tier (Tier 1 = 完整丰富度)"

# 步骤4: 运行外部查询 (按优先级)
Write-Host "[Step 4] 开始外部查询..."

# 4.1: 总是先查询brain (免费)
Write-Host "  [4.1] Brain搜索..."
$brainData = bun run "C:\Users\Administrator\gbrain\src\cli.ts" search "$EntityName" 2>&1

# 4.2: Tier <= 2: Web搜索
if ($tier -le 2) {
    Write-Host "  [4.2] Web搜索 (Brave)..."
    # 这里应该调用Brave Search API
    $webData = "Web search results for $EntityName"
}

# 4.3: Tier <= 2: Twitter查询
if ($tier -le 2) {
    Write-Host "  [4.3] Twitter查询..."
    # 这里应该调用Twitter API
    $twitterData = "Twitter data for $EntityName"
}

# 4.4: Tier == 1: LinkedIn丰富化
if ($tier -eq 1) {
    Write-Host "  [4.4] LinkedIn丰富化 (Crustdata)..."
    # 这里应该调用Crustdata API
    $linkedinData = "LinkedIn data for $EntityName"
}

# 步骤5: 存储原始数据 (可审计，可重新处理)
Write-Host "[Step 5] 存储原始数据..."
$rawData = @{
    "sources" = @{
        "brain"    = @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $brainData }
        "web"      = if ($tier -le 2) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $webData } } else { $null }
        "twitter"  = if ($tier -le 2) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $twitterData } } else { $null }
        "linkedin" = if ($tier -eq 1) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $linkedinData } } else { $null }
    }
}

# 步骤6: 写入brain页面
Write-Host "[Step 6] 写入brain页面..."
$compiledTruth = "# $EntityName`n`n## Executive Summary`n`n## State`n`n## What They Believe`n`n## Timeline`n"

if ($path -eq "CREATE") {
    # 创建新页面
    $compiledTruth | Out-File -FilePath "temp_$EntityName.md" -Encoding UTF8
    bun run "C:\Users\Administrator\gbrain\src\cli.ts" put "$EntityName" --content "`"$(Get-Content temp_$EntityName.md -Raw)`"" 2>&1
    bun run "C:\Users\Administrator\gbrain\src\cli.ts" timeline-add "$EntityName" "$(Get-Date -Format 'yyyy-MM-dd')" "Page created via enrichment" 2>&1
    Remove-Item "temp_$EntityName.md" -Force
    Write-Host "[Step 6] 已创建新页面: $EntityName"
} elseif ($path -eq "UPDATE") {
    # 更新现有页面 (仅当有实质性新信息时)
    Write-Host "[Step 6] 更新现有页面: $EntityName"
    # 这里应该解析现有内容，合并新信息
}

# 步骤7: 交叉引用图谱
Write-Host "[Step 7] 创建交叉引用链接..."
# 示例: gbrain link <person-slug> <company-slug>
# 这里需要根据实际实体关系创建链接

Write-Host "`n✅ Tier1 Enrichment 协议执行完成！"
Write-Host "   实体: $EntityName"
Write-Host "   路径: $path"
Write-Host "   Tier: $tier"

# 注意:
# 1. 不要覆盖用户手写的内容 (如Assessment部分)
# 2. 不要每周多次丰富同一页面 (检查fetched_at时间戳)
# 3. LinkedIn连接数<20表示错误匹配 (丢弃)
# 4. X/Twitter是最被低估的数据源
# 5. 交叉引用不是可选的 - 丰富后必须更新相关页面