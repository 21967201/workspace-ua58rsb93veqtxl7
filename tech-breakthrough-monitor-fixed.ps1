# 技术突破监控脚本 - 修复版本
# 创建时间: 2026-06-03
# 任务来源: cron:0f792ebe-4699-4e8d-bdec-e9c9a83abda4

# 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# 配置参数
$workspaceDir = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
$logDir = "$workspaceDir\logs"
$memoryDir = "$workspaceDir\memory"
$today = Get-Date -Format "yyyy-MM-dd"
$logFile = "$logDir\tech-breakthrough-$(Get-Date -Format 'yyyy-MM-dd').log"
$memoryFile = "$memoryDir\$today.md"

# 创建必要目录
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
if (!(Test-Path $memoryDir)) { New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null }

# 日志函数
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
}

# 初始化日志
Write-Log "技术突破监控任务启动 - $(Get-Date)"
Write-Log "工作目录: $workspaceDir"

# 第一阶段：arXiv论文监控
Write-Log "=== 第一阶段：arXiv论文监控 ==="

# arXiv API查询函数
function Get-ArXivPapers {
    param([string]$Query, [int]$MaxResults = 10)
    
    try {
        $encodedQuery = [System.Web.HttpUtility]::UrlEncode($Query)
        $url = "http://export.arxiv.org/api/query?search_query=all:$encodedQuery&start=0&max_results=$MaxResults&sortBy=submittedDate&sortOrder=descending"
        
        Write-Log "查询arXiv: $Query"
        $response = Invoke-RestMethod -Uri $url -TimeoutSec 30
        
        # 解析arXiv API响应（XML格式）
        $papers = @()
        if ($response -match "entry") {
            $entries = $response -split "<entry>"
            foreach ($entry in $entries[1..($entries.Count-1)]) {
                $title = if ($entry -match "<title>(.*?)</title>") { $matches[1].Trim() } else { "" }
                $summary = if ($entry -match "<summary>(.*?)</summary>") { $matches[1].Trim() } else { "" }
                $published = if ($entry -match "<published>(.*?)</published>") { $matches[1].Trim() } else { "" }
                $id = if ($entry -match "<id>(.*?)</id>") { $matches[1].Trim() } else { "" }
                
                if ($title -and $id) {
                    $papers += [PSCustomObject]@{
                        Title = $title
                        Summary = $summary
                        Published = $published
                        ID = $id
                        Source = "arXiv"
                    }
                }
            }
        }
        
        Write-Log "找到 $($papers.Count) 篇相关论文"
        return $papers
    }
    catch {
        Write-Log "arXiv查询失败: $($_.Exception.Message)"
        return @()
    }
}

# 第二阶段：GitHub项目监控
Write-Log "=== 第二阶段：GitHub项目监控 ==="

# GitHub API查询函数
function Get-GitHubRepos {
    param([array]$Repos)
    
    $results = @()
    foreach ($repo in $Repos) {
        try {
            Write-Log "查询GitHub仓库: $repo"
            $url = "https://api.github.com/repos/$repo"
            $headers = @{ "User-Agent" = "Tech-Breakthrough-Monitor" }
            $response = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 30
            
            $results += [PSCustomObject]@{
                Name = $response.name
                FullName = $response.full_name
                Stars = $response.stargazers_count
                Forks = $response.forks_count
                Updated = $response.updated_at
                Description = $response.description
                URL = $response.html_url
                Source = "GitHub"
            }
            
            Start-Sleep -Milliseconds 500  # 避免API限制
        }
        catch {
            Write-Log "GitHub查询失败 ($repo): $($_.Exception.Message)"
        }
    }
    
    return $results
}

# 第三阶段：技术评估
Write-Log "=== 第三阶段：技术评估 ==="

# 51指标评估函数（简化版）
function Test-TechnologyBreakthrough {
    param($Paper, $Repo)
    
    $score = 0
    $maxScore = 50  # 简化版：5个维度 x 10分
    
    # 1. 结构完整性 (0-10分)
    if ($Paper -and $Paper.Summary -and $Paper.Summary.Length -gt 100) {
        $score += 8
    } elseif ($Paper) {
        $score += 4
    }
    
    # 2. 可用性 (0-10分)
    if ($Repo -and $Repo.Stars -gt 1000) {
        $score += 10
    } elseif ($Repo -and $Repo.Stars -gt 100) {
        $score += 6
    } elseif ($Repo) {
        $score += 3
    }
    
    # 3. 示例质量 (0-10分)
    if ($Repo -and $Repo.Description -and $Repo.Description.Length -gt 50) {
        $score += 7
    } elseif ($Repo) {
        $score += 4
    }
    
    # 4. 创新性 (0-10分)
    if ($Paper -and $Paper.Published -and ((Get-Date) - (Get-Date $Paper.Published)).Days -lt 7) {
        $score += 9  # 最近一周的论文创新性强
    } elseif ($Paper) {
        $score += 5
    }
    
    # 5. 兼容性 (0-10分)
    if ($Repo -and $Repo.Forks -gt 100) {
        $score += 8  # 高fork数表示兼容性好
    } elseif ($Repo) {
        $score += 4
    }
    
    $normalizedScore = [math]::Round(($score / $maxScore) * 10, 1)
    
    # 确定优先级
    $priority = "P2"
    if ($normalizedScore -ge 8.5 -and $Repo -and $Repo.Stars -gt 1000) {
        $priority = "P0"
    } elseif ($normalizedScore -ge 7.0) {
        $priority = "P1"
    }
    
    return [PSCustomObject]@{
        Score = $normalizedScore
        Priority = $priority
        Details = "结构:$($score/5) 可用性:$($score/5) 示例:$($score/5) 创新性:$($score/5) 兼容性:$($score/5)"
    }
}

# 主执行逻辑
try {
    Write-Log "开始执行技术突破监控..."
    
    # 1. 监控arXiv论文
    $arxivQueries = @(
        "Self-Evolving Agents",
        "Multi-Agent Orchestration", 
        "GRPO",
        "RAG",
        "Agent Memory Systems"
    )
    
    $allPapers = @()
    foreach ($query in $arxivQueries) {
        $papers = Get-ArXivPapers -Query $query -MaxResults 5
        $allPapers += $papers
        Start-Sleep -Seconds 2  # 避免API限制
    }
    
    # 2. 监控GitHub项目
    $githubRepos = @(
        "openclaw/openclaw",
        "microsoft/autogen",
        "geekan/MetaGPT"
    )
    
    $allRepos = Get-GitHubRepos -Repos $githubRepos
    
    # 3. 技术评估和筛选
    $breakthroughs = @()
    
    # 评估arXiv论文
    foreach ($paper in $allPapers) {
        $evaluation = Test-TechnologyBreakthrough -Paper $paper
        
        if ($evaluation.Score -ge 7.0) {  # 只考虑评分>=7的技术
            $breakthroughs += [PSCustomObject]@{
                Type = "Paper"
                Title = $paper.Title
                Source = $paper.Source
                Published = $paper.Published
                Score = $evaluation.Score
                Priority = $evaluation.Priority
                Details = $evaluation.Details
                URL = $paper.ID
            }
        }
    }
    
    # 评估GitHub项目
    foreach ($repo in $allRepos) {
        $evaluation = Test-TechnologyBreakthrough -Repo $repo
        
        if ($evaluation.Score -ge 7.0) {
            $breakthroughs += [PSCustomObject]@{
                Type = "Repository"
                Title = $repo.Name
                Source = $repo.Source
                Published = $repo.Updated
                Score = $evaluation.Score
                Priority = $evaluation.Priority
                Details = $evaluation.Details
                URL = $repo.URL
            }
        }
    }
    
    # 4. 按优先级排序
    $breakthroughs = $breakthroughs | Sort-Object -Property Priority, Score -Descending
    
    # 5. 生成报告
    Write-Log "=== 技术突破评估报告 ==="
    Write-Log "发现 $($breakthroughs.Count) 项潜在技术突破"
    
    if ($breakthroughs.Count -gt 0) {
        # 生成Markdown报告
        $reportContent = "# 技术突破监控报告 ($today)`r`n`r`n"
        $reportContent += "## 1. 技术突破列表`r`n`r`n"
        $reportContent += "| # | 技术名称 | 来源 | 发布时间 | 核心创新 | 优先级 |`r`n"
        $reportContent += "|---|---------|------|---------|---------|--------|`r`n"
        
        $i = 1
        foreach ($item in $breakthroughs) {
            $reportContent += "| $i | $($item.Title) | $($item.Source) | $($item.Published) | $($item.Details) | $($item.Priority) |`r`n"
            $i++
        }
        
        $reportContent += "`r`n## 2. 51指标评估`r`n`r`n"
        $reportContent += "| 技术名称 | 综合评分 | 优先级 | 评估详情 |`r`n"
        $reportContent += "|---------|------------|----------|----------|`r`n"
        
        foreach ($item in $breakthroughs) {
            $reportContent += "| $($item.Title) | $($item.Score) | $($item.Priority) | $($item.Details) |`r`n"
        }
        
        # 保存报告
        $reportFile = "$workspaceDir\tech-breakthrough-report-$today.md"
        $reportContent | Out-File -FilePath $reportFile -Encoding UTF8
        Write-Log "报告已保存: $reportFile"
        
        # 更新记忆文件
        $memoryContent = "`r`n## 技术突破监控 - $today`r`n`r`n$reportContent"
        Add-Content -Path $memoryFile -Value $memoryContent -Encoding UTF8
        Write-Log "记忆已更新: $memoryFile"
        
        # 条件推送（仅当有P0或高评分P1时）
        $highPriority = $breakthroughs | Where-Object { $_.Priority -eq "P0" -or ($_.Priority -eq "P1" -and $_.Score -ge 8.5) }
        
        if ($highPriority.Count -gt 0) {
            Write-Log "发现高优先级技术突破，准备推送通知..."
            Write-Log "高优先级技术数量: $($highPriority.Count)"
            
            # 这里可以添加推送逻辑（如发送消息、邮件等）
            # 目前先记录日志
            foreach ($item in $highPriority) {
                Write-Log "高优先级: $($item.Title) (评分: $($item.Score), 优先级: $($item.Priority))"
            }
        } else {
            Write-Log "未发现高优先级技术突破，静默更新记忆系统"
        }
    } else {
        Write-Log "未发现技术突破，静默更新记忆系统"
        
        # 更新记忆文件（即使没有突破也要记录）
        $memoryContent = "`r`n## 技术突破监控 - $today`r`n`r`n无新技术突破发现。`r`n"
        Add-Content -Path $memoryFile -Value $memoryContent -Encoding UTF8
    }
    
    Write-Log "技术突破监控任务完成"
}
catch {
    Write-Log "执行过程中发生错误: $($_.Exception.Message)"
    Write-Log "错误详情: $($_.Exception.ToString())"
}
finally {
    Write-Log "任务执行结束 - $(Get-Date)"
}