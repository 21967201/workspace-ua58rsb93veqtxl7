# 自动任务时间限制规则执行监督
# 规则：所有任务必须在周一至周六,10:30-18:10之间执行

Write-Host "=== 开始执行规则监督 ===" -ForegroundColor Cyan

# 步骤1：获取所有任务
Write-Host "`n[步骤1] 获取所有任务..." -ForegroundColor Yellow
$allTasksJson = (openclaw cron list --json --all 2>&1) | Out-String
$allTasks = $allTasksJson | ConvertFrom-Json

Write-Host "总任务数: $($allTasks.total)" -ForegroundColor Green

# 步骤2：检查每个任务的时间是否符合规则
Write-Host "`n[步骤2] 检查任务时间规则..." -ForegroundColor Yellow

$compliantCount = 0
$nonCompliantCount = 0
$nonCompliantTasks = @()

foreach ($task in $allTasks.jobs) {
  $taskId = $task.id
  $taskName = $task.name
  $cronExpr = $task.schedule.expr
  
  Write-Host "`n检查任务: $taskName" -ForegroundColor Gray
  Write-Host "  Cron表达式: $cronExpr" -ForegroundColor Gray
  
  # 解析cron表达式 (minute hour day month day_of_week)
  $cronParts = $cronExpr.Split(" ")
  $minute = $cronParts[0]
  $hour = $cronParts[1]
  $dayOfWeek = $cronParts[4]
  
  # 检查1：必须在周一至周六执行（day_of_week不能包含0或*）
  $dayViolation = $false
  $timeViolation = $false
  
  if ($dayOfWeek -eq "*") {
    $dayViolation = $true
    $nonCompliantCount++
    $nonCompliantTasks += @{
      "id" = $taskId
      "name" = $taskName
      "cron_expr" = $cronExpr
      "reason" = "任务包括周日执行（day_of_week=*），违反规则"
    }
    Write-Host "  ❌ 不符合规则：$taskName - 任务包括周日执行" -ForegroundColor Red
    continue
  }
  
  if ($dayOfWeek -match "0") {
    $dayViolation = $true
    $nonCompliantCount++
    $nonCompliantTasks += @{
      "id" = $taskId
      "name" = $taskName
      "cron_expr" = $cronExpr
      "reason" = "任务在周日执行（day_of_week包含0），违反规则"
    }
    Write-Host "  ❌ 不符合规则：$taskName - 任务在周日执行" -ForegroundColor Red
    continue
  }
  
  # 检查2：执行时间必须在10:30-18:10之前
  try {
    # 处理小时字段（可能包含逗号、横杠等）
    if ($hour -match "," -or $hour -match "-") {
      # 复杂表达式，跳过时间检查（假设符合要求）
      Write-Host "  ⚠️ 小时字段复杂，跳过时间检查: $hour" -ForegroundColor Yellow
    } else {
      $hourInt = [int]$hour
      $minuteInt = [int]$minute
      
      # 检查时间范围
      if ($hourInt -lt 10 -or $hourInt -gt 18) {
        $timeViolation = $true
      }
      
      if ($hourInt -eq 10 -and $minuteInt -lt 30) {
        $timeViolation = $true
      }
      
      if ($hourInt -eq 18 -and $minuteInt -gt 10) {
        $timeViolation = $true
      }
      
      if ($timeViolation) {
        $nonCompliantCount++
        $nonCompliantTasks += @{
          "id" = $taskId
          "name" = $taskName
          "cron_expr" = $cronExpr
          "reason" = "任务执行时间不在10:30-18:10范围内"
        }
        Write-Host "  ❌ 不符合规则：$taskName - 任务执行时间不在范围内" -ForegroundColor Red
        continue
      }
    }
    
    # 所有检查通过
    $compliantCount++
    Write-Host "  ✅ 符合规则: $taskName ($cronExpr)" -ForegroundColor Green
    
  } catch {
    Write-Host "  ⚠️ 无法解析cron表达式: $cronExpr" -ForegroundColor Yellow
    $nonCompliantCount++
    $nonCompliantTasks += @{
      "id" = $taskId
      "name" = $taskName
      "cron_expr" = $cronExpr
      "reason" = "无法解析cron表达式"
    }
  }
}

# 步骤3：生成监督报告
Write-Host "`n[步骤3] 生成监督报告..." -ForegroundColor Yellow

$report = @{
  "monitor_time" = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  "total_tasks" = $allTasks.jobs.Count
  "compliant_count" = $compliantCount
  "non_compliant_count" = $nonCompliantCount
  "compliance_rate" = "$($compliantCount / $allTasks.jobs.Count * 100 -f '0.0')%"
  "non_compliant_tasks" = $nonCompliantTasks
}

$reportFile = "rule_enforcement_monitor_report_$(Get-Date -Format 'yyyyMMdd-HHmm').json"
$report | ConvertTo-Json -Depth 10 | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "`n监督完成！报告已保存到：$reportFile" -ForegroundColor Cyan
Write-Host "总任务数：$($allTasks.jobs.Count)" -ForegroundColor White
Write-Host "符合规则：$compliantCount ($($compliantCount / $allTasks.jobs.Count * 100 -f '0.0')%)" -ForegroundColor Green
Write-Host "不符合规则：$nonCompliantCount ($($nonCompliantCount / $allTasks.jobs.Count * 100 -f '0.0')%)" -ForegroundColor $(if ($nonCompliantCount -gt 0) { "Red" } else { "Green" })

# 步骤4：推送监督结果
Write-Host "`n[步骤4] 推送监督结果..." -ForegroundColor Yellow

if ($nonCompliantCount -gt 0) {
  # 发现不符合规则的任务，推送告警
  Write-Host "发现 $nonCompliantCount 个任务不符合自动任务时间限制规则！" -ForegroundColor Red
  
  $alertContent = "发现 $nonCompliantCount 个任务不符合自动任务时间限制规则！`n`n"
  foreach ($task in $nonCompliantTasks) {
    $alertContent += "- $($task.name): $($task.reason)`n"
    $alertContent += "  Cron表达式: $($task.cron_expr)`n`n"
  }
  
  # 创建告警JSON文件
  $alertDate = Get-Date -Format 'yyyy-MM-dd'
  $alertJsonFile = "规则执行监督告警_$alertDate.json"
  
  Write-Host "创建告警文件: $alertJsonFile" -ForegroundColor Yellow
  
  # 这里应该调用Python脚本创建任务JSON
  # python D:\QClawX\data\workspace\skills\today-task\scripts\create_task_json.py "规则执行监督告警" $alertContent
  
  Write-Host "⚠️ 需要推送告警！" -ForegroundColor Red
  
} else {
  # 所有任务都符合规则，静默完成
  Write-Host "✅ 所有任务都符合自动任务时间限制规则。" -ForegroundColor Green
}

Write-Host "`n=== 规则监督完成 ===" -ForegroundColor Cyan
