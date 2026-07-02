# 记忆归档脚本 - 每周自动执行

## 功能说明
每周一执行以下归档操作：
1. 压缩超过7天的日志文件
2. 清理超过30天的临时文件
3. 生成归档报告

## 执行逻辑

### 1. 日志压缩 (超过7天)
```powershell
$logsPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\logs"
$archivePath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\archive\logs"

# 创建归档目录
if (-not (Test-Path $archivePath)) {
    New-Item -Path $archivePath -ItemType Directory -Force | Out-Null
}

# 查找超过7天的日志文件
$oldLogs = Get-ChildItem -Path $logsPath -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) }

if ($oldLogs.Count -gt 0) {
    # 创建压缩包
    $archiveName = "logs-$(Get-Date -Format 'yyyy-MM-dd').zip"
    $archiveFile = Join-Path $archivePath $archiveName
    
    Compress-Archive -Path $oldLogs.FullName -DestinationPath $archiveFile -Force
    
    # 删除原始日志文件
    $oldLogs | Remove-Item -Force
    
    Write-Output "已压缩 $($oldLogs.Count) 个日志文件到: $archiveFile"
} else {
    Write-Output "没有超过7天的日志文件需要压缩"
}
```

### 2. 临时文件清理 (超过30天)
```powershell
$workspacePath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"

# 查找超过30天的临时文件
$tempFiles = Get-ChildItem -Path $workspacePath -Recurse -File -Include *.tmp, *.temp, ~* | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }

if ($tempFiles.Count -gt 0) {
    # 生成清理报告
    $report = @()
    $totalSize = 0
    
    foreach ($file in $tempFiles) {
        $fileSize = [math]::Round($file.Length / 1KB, 2)
        $totalSize += $fileSize
        $report += "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'),$($file.FullName),$fileSize KB,$($file.LastWriteTime)"
    }
    
    # 保存报告
    $reportFile = Join-Path $workspacePath "memory\cleanup-report-$(Get-Date -Format 'yyyy-MM-dd').csv"
    $report | Out-File -FilePath $reportFile -Encoding UTF8
    
    # 删除临时文件
    $tempFiles | Remove-Item -Force
    
    Write-Output "已清理 $($tempFiles.Count) 个临时文件，释放 $totalSize KB 空间"
    Write-Output "清理报告已保存到: $reportFile"
} else {
    Write-Output "没有超过30天的临时文件需要清理"
}
```

### 3. 生成归档报告
```powershell
$reportPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7\memory\archive-report-$(Get-Date -Format 'yyyy-MM-dd').md"

$reportContent = @"
# 归档报告 - $(Get-Date -Format 'yyyy年MM月dd日')

## 执行时间
$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## 日志压缩
- 压缩包位置: D:\QClawX\data\workspace-ua58rsb93veqtxl7\archive\logs\
- 压缩规则: 超过7天的日志文件

## 临时文件清理
- 清理规则: 超过30天的临时文件 (*.tmp, *.temp, ~*)
- 清理位置: $workspacePath

## 空间释放
[待执行后填写具体数值]

## 下一步
- 下周一将继续执行归档检查
- 归档报告保存在 memory/ 目录
"@

$reportContent | Out-File -FilePath $reportPath -Encoding UTF8
Write-Output "归档报告已生成: $reportPath"
```

## 定时执行设置

### 方案A: 通过 heartbeat (推荐)
在 `HEARTBEAT.md` 中添加：
```markdown
## 📦 每周记忆归档（周一 10:00）

**当收到心跳且当前是周一10:00-11:00时执行：**

1. 执行日志压缩 (超过7天)
2. 执行临时文件清理 (超过30天)
3. 生成归档报告
4. 更新 `memory/archive-status.md`
```

### 方案B: 通过 Cron
创建一个Cron任务，每周一10:00执行归档脚本。

## 手动执行
如果需要立即执行归档，运行：
```powershell
.\scripts\memory-archive.ps1
```

## 检查归档状态
```powershell
# 查看归档目录
Get-ChildItem "D:\QClawX\data\workspace-ua58rsb93veqtxl7\archive"

# 查看最近的归档报告
Get-ChildItem "D:\QClawX\data\workspace-ua58rsb93veqtxl7\memory\archive-report-*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

---

**创建日期**: 2026-06-29  
**最后更新**: 2026-06-29 10:14  
**执行频率**: 每周一自动执行
