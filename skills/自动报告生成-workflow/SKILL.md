# 自动报告生成 工作流

## 概述
自动化生成各类报告的工作流。

**模式统计:**
- 出现次数: 21 次
- 置信度: 0.9
- 自动发现时间: 2026-07-02

## 工作流步骤

### 1. 数据收集阶段
- 确定报告类型和范围
- 收集相关数据和文件
- 分析历史数据趋势

### 2. 报告生成阶段
- 选择报告模板
- 填充数据和图表
- 生成报告文件 (Markdown/PDF/HTML)

### 3. 输出和推送阶段
- 保存报告到指定位置
- 创建任务 JSON (如需要)
- 推送报告到负一屏/邮件/腾讯文档

## 常见报告类型
- 每日任务执行报告
- 每周工作总结报告
- 月度数据分析报告
- 项目进度报告
- 系统健康报告

## 使用示例

```powershell
# 示例：生成每日任务报告
$reportDate = Get-Date -Format "yyyy-MM-dd"
$reportTitle = "每日任务执行报告_$reportDate"
$reportContent = @"
# $reportTitle

## 执行摘要
- 总任务数: 12
- 成功: 10
- 失败: 2

## 详细信息
...(任务详情)
"@

# 保存报告
$reportPath = "D:\QClawX\data\reports\$reportTitle.md"
$reportContent | Out-File -FilePath $reportPath -Encoding UTF8

# 推送通知
$message = "报告已生成: $reportTitle"
# ... 推送到负一屏
```

## 报告模板建议
- 使用 Markdown 格式便于版本控制
- 包含图表和可视化 (如适用)
- 添加执行时间和耗时统计
- 附带错误日志和调试信息

## 注意事项
- 报告数据准确性验证
- 报告文件命名规范 (包含日期)
- 报告存储路径管理
- 定期清理旧报告 (建议保留30天)

## 相关 Skill
- data-analyzer (数据分析)
- chart-generator (图表生成)
- tencent-docs-writer (腾讯文档写入)
