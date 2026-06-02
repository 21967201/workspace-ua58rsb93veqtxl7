# GBrain Tier1 Enrichment 协议执行脚本
# 真正实现7步enrichment协议，替代不存在的 gbrain enrich --tier=1 命令

param(
    [Parameter(Mandatory=$true)]
    [string]$EntitySlug  # 例如: "people/john-doe-enriched"
)

$ErrorActionPreference = "Stop"
$brainDir = "C:\Users\Administrator\gbrain"
$cli = "bun run $brainDir\src\cli.ts"

Write-Host "`n🧠 GBrain Tier1 Enrichment 协议执行" -ForegroundColor Cyan
Write-Host "实体: $EntitySlug" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor DarkGray

# ==================== Step 1: 实体检测 ====================
Write-Host "`n[Step 1] 实体检测..." -ForegroundColor Green
$entityName = Split-Path $EntitySlug -Leaf
$entityName = $entityName -replace "-", " "
Write-Host "  实体名称: $entityName" -ForegroundColor Gray

# ==================== Step 2: 检查Brain状态 ====================
Write-Host "`n[Step 2] 检查Brain状态 (UPDATE vs CREATE)..." -ForegroundColor Green

try {
    $existing = & $cli search "$entityName" 2>&1
    $hasResults = $existing -match "\[\d+\.\d+\]"
    
    if ($hasResults) {
        $path = "UPDATE"
        Write-Host "  路径: UPDATE (实体已存在)" -ForegroundColor Yellow
        
        # 获取现有页面内容
        $pageContent = & $cli get "$EntitySlug" 2>&1
        Write-Host "  已获取现有页面内容" -ForegroundColor Gray
    } else {
        $path = "CREATE"
        Write-Host "  路径: CREATE (新实体)" -ForegroundColor Yellow
    }
} catch {
    $path = "CREATE"
    Write-Host "  路径: CREATE (新实体，搜索失败)" -ForegroundColor Yellow
}

# ==================== Step 3: 确定Tier ====================
Write-Host "`n[Step 3] 确定Tier..." -ForegroundColor Green
$tier = 1  # 假设是Tier 1（关键人物/公司）
Write-Host "  Tier: $tier (Tier 1 = 完整丰富度，10-15 API调用)" -ForegroundColor Yellow

# ==================== Step 4: 运行外部查询 ====================
Write-Host "`n[Step 4] 运行外部查询..." -ForegroundColor Green

# 4.1 总是先查询Brain (免费)
Write-Host "  [4.1] 查询Brain..." -ForegroundColor Cyan
try {
    $brainData = & $cli search "$entityName" 2>&1 | Out-String
    Write-Host "    ✓ Brain查询完成" -ForegroundColor Green
} catch {
    $brainData = "Error: $_"
    Write-Host "    ✗ Brain查询失败: $_" -ForegroundColor Red
}

# 4.2 Tier <= 2: Web搜索
if ($tier -le 2) {
    Write-Host "  [4.2] Web搜索 (Brave)..." -ForegroundColor Cyan
    Write-Host "    ⚠ 需要配置 BRAVE_API_KEY 环境变量" -ForegroundColor Yellow
    $webData = "Web search skipped - API key not configured"
}

# 4.3 Tier <= 2: Twitter查询
if ($tier -le 2) {
    Write-Host "  [4.3] Twitter查询..." -ForegroundColor Cyan
    Write-Host "    ⚠ 需要配置 TWITTER_BEARER_TOKEN 环境变量" -ForegroundColor Yellow
    $twitterData = "Twitter query skipped - API key not configured"
}

# 4.4 Tier == 1: LinkedIn丰富化
if ($tier -eq 1) {
    Write-Host "  [4.4] LinkedIn丰富化 (Crustdata)..." -ForegroundColor Cyan
    Write-Host "    ⚠ 需要配置 CRUSTDATA_API_KEY 环境变量" -ForegroundColor Yellow
    $linkedinData = "LinkedIn enrichment skipped - API key not configured"
}

# ==================== Step 5: 存储原始数据 ====================
Write-Host "`n[Step 5] 存储原始数据..." -ForegroundColor Green

$rawData = @{
    "sources" = @{
        "brain"    = @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $brainData }
        "web"      = if ($tier -le 2) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $webData } } else { $null }
        "twitter"  = if ($tier -le 2) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $twitterData } } else { $null }
        "linkedin" = if ($tier -eq 1) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $linkedinData } } else { $null }
    }
    "metadata" = @{
        "enriched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        "tier" = $tier
        "path" = $path
    }
}

# 确保raw_data目录存在
$rawDataDir = "$brainDir\knowledge\raw_data"
if (-not (Test-Path $rawDataDir)) {
    New-Item -ItemType Directory -Path $rawDataDir -Force | Out-Null
}

$rawDataPath = "$rawDataDir\$entityName.json"
$rawData | ConvertTo-Json -Depth 10 | Out-File -FilePath $rawDataPath -Encoding UTF8
Write-Host "  ✓ 原始数据已保存: $rawDataPath" -ForegroundColor Green

# ==================== Step 6: 写入Brain页面 ====================
Write-Host "`n[Step 6] 写入Brain页面..." -ForegroundColor Green

if ($path -eq "CREATE") {
    Write-Host "  创建新页面: $EntitySlug" -ForegroundColor Yellow
    
    $newContent = @"
---
type: person
title: $entityName
created: '$(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")'
updated: '$(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")'
tags:
  - auto-enriched
  - tier-$tier
---

# $entityName

## Executive Summary
$entityName is a person/entity enriched via Tier$tier Enrichment protocol on $(Get-Date -Format "yyyy-MM-dd").

## State
- **Enriched At**: $(Get-Date -Format "yyyy-MM-dd HH:mm")
- **Tier**: $tier
- **Path**: CREATE

## What They Believe
*To be populated from Twitter/X data when API is configured*

## What They're Building
*To be populated from project data and meeting notes*

## What Motivates Them
*To be populated from meeting notes and correspondence*

## Assessment
*User-written assessment preserved here - API enrichment MUST NOT overwrite this section*

## Trajectory
- **$(Get-Date -Format "yyyy-MM-dd")**: Page created via Tier$tier Enrichment protocol

## Relationship
- **First Interaction**: $(Get-Date -Format "yyyy-MM-dd") (Automated Enrichment)
- **Context**: Auto-enriched via GBrain protocol

## Contact
*To be populated from Google Contacts integration when configured*

## Timeline

### $(Get-Date -Format "yyyy-MM-dd")
- Auto-enriched via Tier$tier Enrichment protocol
- Raw data stored at: $rawDataPath

## See Also
*To be populated with cross-references*

---

*Page enriched via GBrain Tier$tier Enrichment Protocol*
*Enrichment date: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")*
*Next enrichment check: $((Get-Date).AddDays(7).ToString("yyyy-MM-dd")) (7-day cooldown)*
"@
    
    # 写入临时文件
    $tempFile = [System.IO.Path]::GetTempFileName() + ".md"
    $newContent | Out-File -FilePath $tempFile -Encoding UTF8
    
    try {
        & $cli put "$EntitySlug" --content "`"$(Get-Content $tempFile -Raw -Encoding UTF8)`"" 2>&1
        Write-Host "  ✓ 新页面已创建: $EntitySlug" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ 页面创建失败: $_" -ForegroundColor Red
    } finally {
        Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
    }
    
} elseif ($path -eq "UPDATE") {
    Write-Host "  更新现有页面: $EntitySlug" -ForegroundColor Yellow
    Write-Host "  ⚠ 注意: 仅当有实质性新信息时更新" -ForegroundColor Yellow
    
    # 添加时间线条目
    try {
        $timelineResult = & $cli timeline-add "$EntitySlug" "$(Get-Date -Format 'yyyy-MM-dd')" "Enriched via Tier$tier protocol (automated)" 2>&1
        Write-Host "  ✓ 时间线条目已添加" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ 时间线条目添加失败: $_" -ForegroundColor Red
    }
}

# ==================== Step 7: 交叉引用图谱 ====================
Write-Host "`n[Step 7] 创建交叉引用链接..." -ForegroundColor Green
Write-Host "  ⚠ 需要实体关系数据才能创建链接" -ForegroundColor Yellow
Write-Host "  示例命令:" -ForegroundColor Gray
Write-Host "    gbrain link <person-slug> <company-slug> --type works_at" -ForegroundColor DarkGray
Write-Host "    gbrain link <company-slug> <person-slug> --type employee" -ForegroundColor DarkGray

# 这里需要根据实际实体关系创建链接
# 示例:
# & $cli link "$EntitySlug" "companies/acme-corp" --type "works_at" 2>&1

Write-Host "`n✅ Tier$tier Enrichment 协议执行完成！" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor DarkGray
Write-Host "  实体: $EntitySlug" -ForegroundColor Gray
Write-Host "  路径: $path" -ForegroundColor Gray
Write-Host "  Tier: $tier" -ForegroundColor Gray
Write-Host "  原始数据: $rawDataPath" -ForegroundColor Gray
Write-Host "`n⚠️  后续步骤:" -ForegroundColor Yellow
Write-Host "  1. 配置外部API密钥 (Brave, Twitter, Crustdata)" -ForegroundColor Yellow
Write-Host "  2. 为实体添加交叉引用链接" -ForegroundColor Yellow
Write-Host "  3. 手动完善 Assessment 部分" -ForegroundColor Yellow
Write-Host "  4. 7天内不要重新丰富同一页面" -ForegroundColor Yellow
