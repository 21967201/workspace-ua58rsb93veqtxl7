# 添加数据位置检查到每日监控任务

## 任务
修改 `每日监控任务` 的Cron配置，在数据推送到负一屏之前，先执行 `D:\QClawX\scripts\check-data-location.ps1` 验证数据位置合规性。

## 执行步骤

### 1. 读取当前每日监控任务配置
需要读取 `openclaw.json` 中 `每日监控任务` 的 `task` 字段。

### 2. 修改任务配置
在 `task` 字段的PowerShell脚本开头添加：
```powershell
# 先检查数据位置合规性
$checkResult = & D:\QClawX\scripts\check-data-location.ps1 -HoursAgo 1
if ($checkResult.SuspectFiles) {
    Write-Host "WARNING: Data location violation detected!" -ForegroundColor Red
    $checkResult.SuspectFiles | ForEach-Object { Write-Host "  - $($_.FullName)" -ForegroundColor Yellow }
    # 继续推送，但在推送内容中注明违规
}
```

### 3. 更新Cron任务
使用 `sessions_spawn` 或 `openclaw` CLI 更新Cron任务配置。

## 验证
修改后，下次 `每日监控任务` 执行时（每日10:30），应该会：
1. 先运行 `check-data-location.ps1`
2. 如果发现违规，在推送内容中注明
3. 继续原来的监控流程

## 备注
- 此修改确保规则6（数据存储位置强制规则）被自动执行
- 违规检测不会影响任务执行，但会记录到推送内容中
- 可扩展：如果违规严重，可以配置为暂停推送并报警
