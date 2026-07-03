# 负一屏推送 工作流

## 概述
自动化推送消息到负一屏的工作流。

**模式统计:**
- 出现次数: 31 次
- 置信度: 0.9
- 自动发现时间: 2026-07-02

## 工作流步骤

### 1. 准备阶段
- 确定推送内容
- 准备数据/文件
- 检查负一屏系统状态

### 2. 执行阶段
- 生成消息内容
- 创建任务 JSON (如需要)
- 执行推送操作 (HTTP POST)

### 3. 验证阶段
- 检查推送结果 (HTTP 200)
- 记录执行日志
- 生成工件文件

## 使用示例

```powershell
# 示例：推送到负一屏
$message = "任务完成报告"
$jsonBody = @{
    message = $message
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    source = "auto-task"
} | ConvertTo-Json

# 推送到负一屏 API
Invoke-RestMethod -Uri "http://localhost:8080/api/push" -Method Post -Body $jsonBody -ContentType "application/json"
```

## 常见推送内容
- 任务完成通知
- 报告生成通知
- 系统状态更新
- 错误信息报警

## 注意事项
- 确保负一屏 API 可用
- 处理推送失败的重试逻辑 (建议最多3次)
- 消息长度限制 (建议≤1000字符)
- 记录推送历史以便追踪

## 相关 Skill
- cron-task-manager (定时任务管理)
- report-generator (报告生成)
- message-sender (消息发送)
