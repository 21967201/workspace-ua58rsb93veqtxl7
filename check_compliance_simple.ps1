# Check cron task compliance with rules
# Rules: Monday-Saturday, 10:30-18:10

Write-Host "=== Rule Enforcement Supervision ===" -ForegroundColor Cyan

# Get all tasks
$json = (openclaw cron list --json --all 2>&1) | Out-String
$data = $json | ConvertFrom-Json

$compliant = 0
$nonCompliant = 0
$violations = @()

foreach ($task in $data.jobs) {
    $name = $task.name
    $expr = $task.schedule.expr
    
    Write-Host "`nChecking: $name" -NoNewline
    Write-Host " ($expr)" -ForegroundColor Gray
    
    $parts = $expr.Split(" ")
    $minute = $parts[0]
    $hour = $parts[1]
    $dayOfWeek = $parts[4]
    
    $isValid = $true
    $reason = ""
    
    # Check 1: Must not run on Sunday (day_of_week cannot be "*" or contain "0")
    if ($dayOfWeek -eq "*") {
        $isValid = $false
        $reason = "Runs every day (including Sunday)"
    }
    elseif ($dayOfWeek -match "0") {
        $isValid = $false
        $reason = "Runs on Sunday (day_of_week contains 0)"
    }
    
    # Check 2: Must run between 10:30-18:10
    if ($isValid) {
        $hourInt = [int]$hour
        $minuteInt = [int]$minute
        
        if ($hourInt -lt 10 -or $hourInt -gt 18) {
            $isValid = $false
            $reason = "Hour $hourInt outside range 10-18"
        }
        elseif ($hourInt -eq 10 -and $minuteInt -lt 30) {
            $isValid = $false
            $reason = "Time before 10:30 ($minuteInt min)"
        }
        elseif ($hourInt -eq 18 -and $minuteInt -gt 10) {
            $isValid = $false
            $reason = "Time after 18:10 ($minuteInt min)"
        }
    }
    
    if ($isValid) {
        Write-Host "  ✅ COMPLIANT" -ForegroundColor Green
        $compliant++
    }
    else {
        Write-Host "  ❌ NON-COMPLIANT: $reason" -ForegroundColor Red
        $nonCompliant++
        $violations += @{
            task_id = $task.id
            name = $name
            expr = $expr
            reason = $reason
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Supervision Results:" -ForegroundColor Cyan
Write-Host "  Total tasks: $($data.total)" -ForegroundColor White
Write-Host "  Compliant: $compliant" -ForegroundColor Green
Write-Host "  Non-compliant: $nonCompliant" -ForegroundColor $(if ($nonCompliant -gt 0) { "Red" } else { "Green" })

if ($violations.Count -gt 0) {
    Write-Host "`nViolations found:" -ForegroundColor Red
    foreach ($v in $violations) {
        Write-Host "  - $($v.name)" -ForegroundColor Yellow
        Write-Host "    ID: $($v.task_id)" -ForegroundColor Gray
        Write-Host "    Cron: $($v.expr)" -ForegroundColor Gray
        Write-Host "    Reason: $($v.reason)" -ForegroundColor Red
    }
    
    # Generate alert
    Write-Host "`n⚠️ ALERT: $nonCompliant task(s) violate rules!" -ForegroundColor Red
    Write-Host "Need to fix these tasks to comply with Monday-Saturday, 10:30-18:10 rule." -ForegroundColor Yellow
}
else {
    Write-Host "`n✅ All tasks comply with the rules!" -ForegroundColor Green
}

# Save report
$report = @{
    monitor_time = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    total_tasks = $data.total
    compliant_count = $compliant
    non_compliant_count = $nonCompliant
    compliance_rate = "$($compliant / $data.total * 100 -f '0.0')%"
    violations = $violations
}

$reportFile = "rule_supervision_report_$(Get-Date -Format 'yyyyMMdd-HHmm').json"
$report | ConvertTo-Json -Depth 10 | Out-File -FilePath $reportFile -Encoding UTF8
Write-Host "`nReport saved: $reportFile" -ForegroundColor Cyan
