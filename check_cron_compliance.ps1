# 检查cron任务是否符合规则
# 规则：周一至周六, 10:30-18:10

$tasks = @(
  @{name="tech-breakthrough-monitor"; expr="30 13 * * 1-6"},
  @{name="实时监控任务"; expr="0 14 * * 1-6"},
  @{name="每日任务监督", expr="30 15 * * 1-6"},
  @{name="自动同步任务文件到GitHub", expr="30 16 * * 1-6"},
  @{name="Memory Dreaming Promotion", expr="39 3 * * *"},
  @{name="每日监控任务", expr="30 10 * * 1-6"},
  @{name="季度评审任务", expr="35 10 * * 1-6"},
  @{name="月度报告任务", expr="45 10 * * 1-6"},
  @{name="1688全面分析（全景+竞品）", expr="0 11 * * 1-6"},
  @{name="商业智能周报", expr="0 15 * * 5"},
  @{name="学术论文与知识库周度同步", expr="10 11 * * 1"},
  @{name="QClaw智能清理（周度+月度合并）", expr="40 11 * * 1"},
  @{name="智能全景管理（含GBrain + 记忆管理）", expr="10 12 * * 1"},
  @{name="OpenClaw违规检查（7天一次）", expr="30 14 * * 1"},
  @{name="每周任务执行分析与错误预防检查", expr="0 15 * * 1"}
)

$compliant = 0
$nonCompliant = 0
$violations = @()

foreach ($task in $tasks) {
  $name = $task.name
  $expr = $task.expr
  
  Write-Host "`n检查: $name" -NoNewline
  Write-Host " ($expr)" -ForegroundColor Gray
  
  $parts = $expr.Split(" ")
  $minute = $parts[0]
  $hour = $parts[1]
  $dayOfWeek = $parts[4]
  
  $isCompliant = $true
  $reason = ""
  
  # 检查1：不能在周日执行
  if ($dayOfWeek -eq "*") {
    $isCompliant = $false
    $reason = "包括周日执行（day_of_week=*）"
  }
  elseif ($dayOfWeek -match "0") {
    $isCompliant = $false
    $reason = "在周日执行（day_of_week包含0）"
  }
  
  # 检查2：时间必须在10:30-18:10
  if ($isCompliant) {
    $hourInt = [int]$hour
    $minuteInt = [int]$minute
    
    if ($hourInt -lt 10 -or $hourInt -gt 18) {
      $isCompliant = $false
      $reason = "执行时间不在10:30-18:10范围内（小时=$hourInt）"
    }
    elseif ($hourInt -eq 10 -and $minuteInt -lt 30) {
      $isCompliant = $false
      $reason = "执行时间早于10:30（$minuteInt 分）"
    }
    elseif ($hourInt -eq 18 -and $minuteInt -gt 10) {
      $isCompliant = $false
      $reason = "执行时间晚于18:10（$minuteInt 分）"
    }
  }
  
  if ($isCompliant) {
    Write-Host "  ✅ 符合规则" -ForegroundColor Green
    $compliant++
  }
  else {
    Write-Host "  ❌ 不符合规则: $reason" -ForegroundColor Red
    $nonCompliant++
    $violations += @{name=$name; expr=$expr; reason=$reason}
  }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "监督结果：" -ForegroundColor Cyan
Write-Host "  总任务数: $($tasks.Count)" -ForegroundColor White
Write-Host "  符合规则: $compliant" -ForegroundColor Green
Write-Host "  不符合规则: $nonCompliant" -ForegroundColor $(if ($nonCompliant -gt 0) { "Red" } else { "Green" })

if ($violations.Count -gt 0) {
  Write-Host "`n违规任务详情：" -ForegroundColor Red
  foreach ($v in $violations) {
    Write-Host "  - $($v.name)" -ForegroundColor Yellow
    Write-Host "    Cron: $($v.expr)" -ForegroundColor Gray
    Write-Host "    原因: $($v.reason)" -ForegroundColor Red
  }
}

# 生成报告
$report = @{
  monitor_time = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  total_tasks = $tasks.Count
  compliant_count = $compliant
  non_compliant_count = $nonCompliant
  compliance_rate = "$($compliant / $tasks.Count * 100 -f '0.0')%"
  violations = $violations
}

$reportFile = "rule_enforcement_report_$(Get-Date -Format 'yyyyMMdd-HHmm').json"
$report | ConvertTo-Json -Depth 10 | Out-File -FilePath $reportFile -Encoding UTF8
Write-Host "`n报告已保存: $reportFile" -ForegroundColor Cyan
