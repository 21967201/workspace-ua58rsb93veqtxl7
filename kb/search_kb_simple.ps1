# QClaw 原生知识库 - 简化搜索脚本
# 功能: 同时搜索 memory/ 和 kb/ 目录

param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    
    [Parameter(Mandatory=$false)]
    [string]$Category = "all",
    
    [Parameter(Mandatory=$false)]
    [int]$MaxResults = 10
)

$workspaceRoot = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
$results = @()

Write-Host "🔍 搜索关键词: $Query" -ForegroundColor Cyan
Write-Host "📂 搜索范围: $Category" -ForegroundColor Gray
Write-Host ""

# ========== Layer 3: Custom KB (关键词搜索) ==========
Write-Host "[Layer 3] 搜索 Custom KB..." -ForegroundColor Yellow

$searchDirs = @()

switch ($Category) {
    "all" {
        $searchDirs = @(
            "$workspaceRoot\kb\people",
            "$workspaceRoot\kb\projects",
            "$workspaceRoot\kb\tech",
            "$workspaceRoot\kb\ai-breakthrough",
            "$workspaceRoot\kb\decisions"
        )
    }
    "people" { $searchDirs = @("$workspaceRoot\kb\people") }
    "projects" { $searchDirs = @("$workspaceRoot\kb\projects") }
    "tech" { $searchDirs = @("$workspaceRoot\kb\tech") }
    "decisions" { $searchDirs = @("$workspaceRoot\kb\decisions") }
    default {
        Write-Host "⚠️ 未知分类: $Category，搜索所有目录" -ForegroundColor Yellow
        $searchDirs = @(
            "$workspaceRoot\kb\people",
            "$workspaceRoot\kb\projects",
            "$workspaceRoot\kb\tech",
            "$workspaceRoot\kb\ai-breakthrough",
            "$workspaceRoot\kb\decisions"
        )
    }
}

foreach ($dir in $searchDirs) {
    if (Test-Path $dir) {
        Write-Host "  搜索: $dir" -ForegroundColor Gray
        
        $matches = Select-String -Path "$dir\*.md" -Pattern $Query -AllMatches -ErrorAction SilentlyContinue
        
        foreach ($match in $matches) {
            $result = [PSCustomObject]@{
                Source = "kb"
                File = $match.Filename
                Path = $match.Path
                Line = $match.LineNumber
                Content = $match.Line.Trim()
                Category = Split-Path $dir -Leaf
            }
            $results += $result
        }
    }
}

# ========== 结果展示 ==========
Write-Host ""
Write-Host "📊 搜索结果" -ForegroundColor Green
Write-Host "------------------------" -ForegroundColor Gray

if ($results.Count -eq 0) {
    Write-Host "❌ 未找到匹配结果" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 建议:" -ForegroundColor Yellow
    Write-Host "  1. 尝试不同的关键词" -ForegroundColor Gray
    Write-Host "  2. 使用 memory_search 工具进行语义搜索" -ForegroundColor Gray
    Write-Host "  3. 检查 kb/ 目录中是否有相关文件" -ForegroundColor Gray
} else {
    Write-Host "✅ 找到 $($results.Count) 个匹配结果" -ForegroundColor Green
    Write-Host ""
    
    $index = 1
    foreach ($result in $results) {
        Write-Host "[$index] $($result.File) (行 $($result.Line))" -ForegroundColor Cyan
        Write-Host "    分类: $($result.Category)" -ForegroundColor Gray
        Write-Host "    内容: $($result.Content)" -ForegroundColor White
        Write-Host ""
        $index++
        
        if ($index -gt $MaxResults) { break }
    }
}

# ========== 使用建议 ==========
Write-Host "------------------------" -ForegroundColor Gray
Write-Host "💡 使用建议:" -ForegroundColor Yellow
Write-Host "  1. 语义搜索 (推荐): 在 QClaw 对话中调用:" -ForegroundColor Gray
Write-Host "     memory_search --query=""$Query""" -ForegroundColor DarkCyan
Write-Host "  2. 跨库搜索: memory_search --query=""$Query"" --corpus=""all""" -ForegroundColor Gray
Write-Host "  3. 查看文件: read --path=""kb/people/xxx.md""" -ForegroundColor Gray
Write-Host ""

return $results
