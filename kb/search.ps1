# QClaw 原生知识库 - 极简搜索
# 用法: .\search.ps1 "关键词"

param($Query)

$root = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"

Write-Host "🔍 搜索: $Query" -ForegroundColor Cyan
Write-Host ""

# 搜索 kb/ 目录
Write-Host "📂 搜索 kb/ 目录..." -ForegroundColor Yellow
Get-ChildItem -Path "$root\kb" -Filter "*.md" -Recurse | ForEach-Object {
    $file = $_
    Select-String -Path $file.FullName -Pattern $Query -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  ✅ $($file.FullName.Replace($root,'')) (行 $($_.LineNumber))" -ForegroundColor Green
        Write-Host "     $($_.Line.Trim())" -ForegroundColor Gray
        Write-Host ""
    }
}

# 搜索 memory/ 目录
Write-Host "📂 搜索 memory/ 目录..." -ForegroundColor Yellow
Get-ChildItem -Path "$root\memory" -Filter "*.md" -Recurse | ForEach-Object {
    $file = $_
    Select-String -Path $file.FullName -Pattern $Query -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  ✅ $($file.FullName.Replace($root,'')) (行 $($_.LineNumber))" -ForegroundColor Cyan
        Write-Host "     $($_.Line.Trim())" -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Host "✅ 搜索完成" -ForegroundColor Green
