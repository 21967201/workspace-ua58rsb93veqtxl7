# 技术监控简单版本 - 语法正确
Write-Host "开始技术监控..." -ForegroundColor Green

# 配置
$workspaceDir = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
$today = Get-Date -Format "yyyy-MM-dd"
$logFile = "$workspaceDir\tech-monitor.log"
$memoryFile = "$workspaceDir\memory\$today.md"

# 创建目录
if (!(Test-Path "$workspaceDir\memory")) {
    New-Item -ItemType Directory -Path "$workspaceDir\memory" -Force | Out-Null
}

# 写日志函数
function Add-Log($message) {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$time] $message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
}

Add-Log "技术突破监控启动"

# 1. 测试网络连接
Add-Log "测试网络连接..."
try {
    $testConnection = Test-NetConnection -ComputerName "arxiv.org" -Port 80 -InformationLevel Quiet -ErrorAction Stop
    if ($testConnection) {
        Add-Log "网络连接正常"
    }
}
catch {
    Add-Log "网络连接有问题: $($_.Exception.Message)"
}

# 2. 简单arXiv查询
Add-Log "查询arXiv..."
try {
    $arxivUrl = "http://export.arxiv.org/api/query?search_query=all:AI&start=0&max_results=3"
    $response = Invoke-RestMethod -Uri $arxivUrl -TimeoutSec 30 -ErrorAction Stop
    Add-Log "arXiv查询成功"
}
catch {
    Add-Log "arXiv查询失败: $($_.Exception.Message)"
}

# 3. 简单GitHub查询
Add-Log "查询GitHub..."
try {
    $githubUrl = "https://api.github.com/repos/microsoft/autogen"
    $headers = @{ "User-Agent" = "PowerShell-Tech-Monitor" }
    $response = Invoke-RestMethod -Uri $githubUrl -Headers $headers -TimeoutSec 30 -ErrorAction Stop
    Add-Log "GitHub查询成功: $($response.name)"
}
catch {
    Add-Log "GitHub查询失败: $($_.Exception.Message)"
}

# 4. 生成报告
$reportContent = "# 技术监控报告`r`n`r`n"
$reportContent += "**日期**: $today`r`n"
$reportContent += "**状态**: 已完成基础监控`r`n`r`n"
$reportContent += "## 执行的任务`r`n`r`n"
$reportContent += "1. 网络连接测试`r`n"
$reportContent += "2. arXiv论文查询`r`n"
$reportContent += "3. GitHub项目查询`r`n`r`n"
$reportContent += "## 下一步`r`n`r`n"
$reportContent += "- 完善监控逻辑`r`n"
$reportContent += "- 添加技术评估`r`n"
$reportContent += "- 实现推送功能`r`n"

$reportFile = "$workspaceDir\tech-report-$today.md"
$reportContent | Out-File -FilePath $reportFile -Encoding UTF8
Add-Log "报告已保存: $reportFile"

# 5. 更新记忆
$memoryContent = "`r`n## 技术监控 - $today`r`n`r`n"
$memoryContent += "- 状态: 已完成`r`n"
$memoryContent += "- 报告: $reportFile`r`n"

Add-Content -Path $memoryFile -Value $memoryContent -Encoding UTF8
Add-Log "记忆已更新: $memoryFile"

Add-Log "技术监控完成"
Add-Log "任务结束"