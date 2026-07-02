# Distill 工作流发现 - Session 分析脚本
# 目标: 扫描最近 30 天的 session 历史，识别重复模式并固化为可复用 skill

param(
    [int]$DaysBack = 30,
    [int]$MinRepetitions = 3,
    [double]$MinConfidence = 0.7
)

# 配置
$workspaceDir = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
$sessionDir = "D:\QClawX\data\.qclaw\agents\main\sessions"
$reportPath = "$workspaceDir\distill-report-$(Get-Date -Format 'yyyy-MM-dd').md"
$cutoffDate = (Get-Date).AddDays(-$DaysBack)

# 初始化数据结构
$sessionData = @()
$toolSequences = @{}
$taskPatterns = @()
$workflowPatterns = @()

Write-Host "=== Distill 工作流发现任务 ===" -ForegroundColor Cyan
Write-Host "扫描时间范围: $(Get-Date $cutoffDate -Format 'yyyy-MM-dd') 至 $(Get-Date -Format 'yyyy-MM-dd')" -ForegroundColor Yellow
Write-Host "最小重复次数: $MinRepetitions" -ForegroundColor Yellow
Write-Host "最小置信度: $MinConfidence" -ForegroundColor Yellow
Write-Host ""

# 步骤 1: 扫描 session 文件
Write-Host "步骤 1: 扫描 session 文件..." -ForegroundColor Green
$sessionFiles = Get-ChildItem -Path $sessionDir -Filter "*.jsonl" -File | 
    Where-Object { $_.LastWriteTime -gt $cutoffDate }

Write-Host "  找到 $($sessionFiles.Count) 个 session 文件" -ForegroundColor Gray

if ($sessionFiles.Count -eq 0) {
    Write-Host "  ⚠️ 未找到符合条件的 session 文件" -ForegroundColor Red
    Write-Host "  建议: 检查 session 目录或延长扫描时间范围" -ForegroundColor Yellow
    exit 1
}

# 步骤 2: 解析 session 数据
Write-Host "步骤 2: 解析 session 数据..." -ForegroundColor Green

$totalSessions = 0
$totalToolCalls = 0
$toolCallSequences = @()

foreach ($file in $sessionFiles) {
    $totalSessions++
    Write-Host "  处理: $($file.Name)" -ForegroundColor Gray
    
    try {
        # 读取 JSONL 文件
        $lines = Get-Content $file.FullName -ErrorAction Stop
        
        $sessionToolCalls = @()
        $sessionTasks = @()
        
        foreach ($line in $lines) {
            try {
                $data = $line | ConvertFrom-Json -ErrorAction Stop
                
                # 提取工具调用信息
                if ($data.type -eq "tool.call" -or $data.type -eq "tool.result") {
                    $toolName = $data.data.toolName
                    $toolCallSequences += $toolName
                    $sessionToolCalls += $toolName
                    $totalToolCalls++
                }
                
                # 提取任务描述（从消息或提示中）
                if ($data.type -eq "message" -and $data.data.role -eq "user") {
                    $taskText = $data.data.content
                    if ($taskText -match "(?i)(搜索|查找|分析|创建|更新|删除|读取|写入|执行|运行|检查|验证)") {
                        $sessionTasks += $matches[0]
                    }
                }
            }
            catch {
                # 跳过无法解析的行
                continue
            }
        }
        
        # 记录会话数据
        $sessionData += @{
            File = $file.Name
            ToolCalls = $sessionToolCalls
            Tasks = $sessionTasks
            ToolCallCount = $sessionToolCalls.Count
            TaskCount = $sessionTasks.Count
        }
        
        # 提取工具调用序列模式
        if ($sessionToolCalls.Count -ge 2) {
            for ($i = 0; $i -lt $sessionToolCalls.Count - 1; $i++) {
                $sequence = "$($sessionToolCalls[$i]) → $($sessionToolCalls[$i+1])"
                if (-not $toolSequences.ContainsKey($sequence)) {
                    $toolSequences[$sequence] = 0
                }
                $toolSequences[$sequence]++
            }
        }
    }
    catch {
        Write-Host "  ⚠️ 无法读取文件: $($file.Name)" -ForegroundColor Yellow
        continue
    }
}

Write-Host "  总共解析 $totalSessions 个 session" -ForegroundColor Gray
Write-Host "  总共提取 $totalToolCalls 个工具调用" -ForegroundColor Gray

# 步骤 3: 识别工作流模式
Write-Host "步骤 3: 识别工作流模式..." -ForegroundColor Green

# 3.1 识别常见的工具调用序列
Write-Host "  3.1 分析工具调用序列..." -ForegroundColor Gray
$commonSequences = $toolSequences.GetEnumerator() | 
    Where-Object { $_.Value -ge $MinRepetitions } | 
    Sort-Object Value -Descending

Write-Host "    找到 $($commonSequences.Count) 个重复序列" -ForegroundColor Gray

# 3.2 识别任务模式
Write-Host "  3.2 分析任务模式..." -ForegroundColor Gray
$allTasks = $sessionData | ForEach-Object { $_.Tasks } | Group-Object | 
    Where-Object { $_.Count -ge $MinRepetitions } | 
    Sort-Object Count -Descending

Write-Host "    找到 $($allTasks.Count) 个重复任务模式" -ForegroundColor Gray

# 3.3 识别完整工作流模式
Write-Host "  3.3 识别完整工作流模式..." -ForegroundColor Gray

# 定义常见的工作流模式
$workflowDefinitions = @(
    @{
        Name = "搜索-读取-总结-推送"
        Pattern = @("web_search", "web_fetch", "read", "message")
        Description = "搜索信息，读取内容，总结要点，推送结果"
    },
    @{
        Name = "文件读取-编辑-写入"
        Pattern = @("read", "edit", "write")
        Description = "读取文件，编辑内容，写回文件"
    },
    @{
        Name = "代码分析-修复-测试"
        Pattern = @("read", "exec", "edit", "exec")
        Description = "分析代码，执行修复，编辑文件，测试验证"
    },
    @{
        Name = "浏览器自动化流程"
        Pattern = @("browser", "browser", "browser")
        Description = "多步骤浏览器操作（登录、导航、数据提取）"
    },
    @{
        Name = "定时任务管理"
        Pattern = @("cron", "cron", "cron")
        Description = "创建、查看、管理定时任务"
    }
)

foreach ($workflow in $workflowDefinitions) {
    $matchCount = 0
    foreach ($session in $sessionData) {
        $toolCalls = $session.ToolCalls -join ","
        $patternStr = $workflow.Pattern -join ","
        
        if ($toolCalls -match [regex]::Escape($patternStr)) {
            $matchCount++
        }
    }
    
    if ($matchCount -ge $MinRepetitions) {
        $confidence = ($matchCount / $totalSessions) * 0.8 + 
                     (if ($workflow.Pattern.Count -ge 3) { 0.2 } else { 0.1 })
        
        $workflowPatterns += @{
            Name = $workflow.Name
            Pattern = $workflow.Pattern
            Description = $workflow.Description
            Repetitions = $matchCount
            Confidence = [math]::Min($confidence, 1.0)
            General = $true
        }
    }
}

Write-Host "    找到 $($workflowPatterns.Count) 个完整工作流模式" -ForegroundColor Gray

# 步骤 4: 评估模式价值
Write-Host "步骤 4: 评估模式价值..." -ForegroundColor Green

$highValuePatterns = @()

foreach ($pattern in $workflowPatterns) {
    if ($pattern.Confidence -ge $MinConfidence) {
        $highValuePatterns += $pattern
        Write-Host "  ✅ 高价值模式: $($pattern.Name) (置信度: $([math]::Round($pattern.Confidence, 2)))" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠️ 低价值模式: $($pattern.Name) (置信度: $([math]::Round($pattern.Confidence, 2)))" -ForegroundColor Yellow
    }
}

Write-Host "  高价值模式: $($highValuePatterns.Count) 个" -ForegroundColor Gray

# 步骤 5: 生成报告
Write-Host "步骤 5: 生成报告..." -ForegroundColor Green

$report = @"
# Distill 工作流发现报告

**生成时间**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**扫描时间范围**: $(Get-Date $cutoffDate -Format "yyyy-MM-dd") 至 $(Get-Date -Format "yyyy-MM-dd")  
**最小重复次数**: $MinRepetitions  
**最小置信度**: $MinConfidence

---

## 📊 执行摘要

| 指标 | 数值 |
|------|------|
| 扫描的 session 数量 | $totalSessions |
| 识别的模式数量 | $($workflowPatterns.Count) |
| 高价值模式数量 | $($highValuePatterns.Count) |
| 创建/提议的 skill | $($highValuePatterns.Count) |

---

## 🔍 详细分析结果

### 1. Session 扫描统计

- **Session 文件总数**: $totalSessions
- **工具调用总数**: $totalToolCalls
- **平均每个 session 工具调用数**: $([math]::Round($totalToolCalls / $totalSessions, 1))

### 2. 工具调用序列分析

常见的工具调用序列（重复次数 ≥ $MinRepetitions）:

"@

if ($commonSequences.Count -gt 0) {
    $report += "`n| 序列 | 重复次数 | 置信度 |"
    $report += "`n|------|----------|--------|"
    
    foreach ($seq in $commonSequences) {
        $confidence = ($seq.Value / $totalSessions) * 1.0
        $report += "`n| $($seq.Key) | $($seq.Value) | $([math]::Round($confidence, 2)) |"
    }
}
else {
    $report += "`n⚠️ 未找到重复的工具调用序列。"
}

$report += @"

### 3. 工作流模式识别

识别的完整工作流模式：

| 模式名称 | 重复次数 | 置信度 | 状态 |
|---------|----------|--------|------|

"@

foreach ($pattern in $workflowPatterns) {
    $status = if ($pattern.Confidence -ge $MinConfidence) { "✅ 高价值" } else { "⚠️ 低价值" }
    $report += "| $($pattern.Name) | $($pattern.Repetitions) | $([math]::Round($pattern.Confidence, 2)) | $status |`n"
}

$report += @"

### 4. 高价值模式详情

"@

foreach ($pattern in $highValuePatterns) {
    $report += @"
#### $($pattern.Name)

- **描述**: $($pattern.Description)
- **工具调用序列**: $($pattern.Pattern -join " → ")
- **重复次数**: $($pattern.Repetitions)
- **置信度**: $([math]::Round($pattern.Confidence, 2))
- **通用性**: $(if ($pattern.General) { "是" } else { "否" })

**建议**: 为这个模式创建 skill，以便复用。

"
}

$report += @"

---

## 📈 统计信息

### 工具使用频率

"@

# 计算工具使用频率
$toolUsage = @{}
foreach ($session in $sessionData) {
    foreach ($tool in $session.ToolCalls) {
        if (-not $toolUsage.ContainsKey($tool)) {
            $toolUsage[$tool] = 0
        }
        $toolUsage[$tool]++
    }
}

$report += "`n| 工具名称 | 使用次数 | 使用频率 |"
$report += "`n|---------|----------|----------|"

$toolUsageSorted = $toolUsage.GetEnumerator() | Sort-Object Value -Descending
foreach ($tool in $toolUsageSorted) {
    $frequency = ($tool.Value / $totalToolCalls) * 100
    $report += "`n| $($tool.Key) | $($tool.Value) | $([math]::Round($frequency, 1))% |"
}

$report += @"

---

## 🎯 后续行动建议

1. **为高价值模式创建 skill**
   - 使用 `skill_workshop` 工具的 `action=create` 创建提案
   - 生成 SKILL.md（包含：触发词、执行流程、工具调用、示例）

2. **优化现有工作流**
   - 根据识别的模式，优化重复的工作流
   - 减少手动操作，提高自动化程度

3. **监控新模式**
   - 定期运行此分析，发现新的工作流模式
   - 持续更新和优化 skill 库

---

## 📝 附录: 原始数据

### Session 列表

"@

foreach ($session in $sessionData) {
    $report += "`n- **$($session.File)**: $($session.ToolCallCount) 个工具调用, $($session.TaskCount) 个任务"
}

$report += @"

### 分析脚本

本分析使用的 PowerShell 脚本: \`distill-analyze.ps1\`

---

**报告结束**
"

# 保存报告
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "  报告已保存: $reportPath" -ForegroundColor Green

# 步骤 6: 为的高价值模式创建 skill 提案
Write-Host "步骤 6: 为高价值模式创建 skill 提案..." -ForegroundColor Green

if ($highValuePatterns.Count -gt 0) {
    # 检查是否已有类似 skill
    Write-Host "  检查现有 skill..." -ForegroundColor Gray
    
    foreach ($pattern in $highValuePatterns) {
        $skillName = "$($pattern.Name -replace ' ', '-')-workflow"
        $skillName = $skillName.ToLower()
        
        Write-Host "  为模式 '$($pattern.Name)' 创建 skill 提案..." -ForegroundColor Gray
        
        # 生成 SKILL.md 内容
        $skillContent = @"
# $($pattern.Name) 工作流

## 触发词
- $($pattern.Name)
- $($pattern.Description)

## 执行流程

$($pattern.Pattern -join " → ")

## 工具调用

$(foreach ($tool in $pattern.Pattern) { "- $tool`n" })

## 示例

**示例 1**: 
1. 用户请求: "$($pattern.Name)"
2. 执行: $($pattern.Pattern -join " → ")
3. 结果: 完成 $($pattern.Name)

## 注意事项

- 此工作流已从 session 历史中识别
- 重复次数: $($pattern.Repetitions)
- 置信度: $([math]::Round($pattern.Confidence, 2))
- 创建时间: $(Get-Date -Format "yyyy-MM-dd")
"@
        
        # 使用 skill_workshop 创建提案
        try {
            # 这里需要调用 skill_workshop，但由于我们是子任务，先生成提案文件
            $proposalPath = "$workspaceDir\skill-proposal-$($skillName).md"
            $skillContent | Out-File -FilePath $proposalPath -Encoding UTF8
            
            Write-Host "    ✅ 提案已生成: $proposalPath" -ForegroundColor Green
        }
        catch {
            Write-Host "    ⚠️ 无法创建提案: $_" -ForegroundColor Yellow
        }
    }
}
else {
    Write-Host "  ⚠️ 没有高价值模式可创建 skill" -ForegroundColor Yellow
}

# 完成
Write-Host ""
Write-Host "=== 任务完成 ===" -ForegroundColor Cyan
Write-Host "报告位置: $reportPath" -ForegroundColor Green
Write-Host "高价值模式: $($highValuePatterns.Count) 个" -ForegroundColor Green
Write-Host "Skill 提案: $($highValuePatterns.Count) 个" -ForegroundColor Green

# 返回结果摘要
return @{
    TotalSessions = $totalSessions
    TotalToolCalls = $totalToolCalls
    PatternsFound = $workflowPatterns.Count
    HighValuePatterns = $highValuePatterns.Count
    ReportPath = $reportPath
    SkillProposals = $highValuePatterns.Count
}
