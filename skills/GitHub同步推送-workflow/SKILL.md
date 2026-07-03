# GitHub同步推送 工作流

## 概述
自动化同步文件到GitHub并推送的工作流。

**模式统计:**
- 出现次数: 3 次
- 置信度: 0.8
- 自动发现时间: 2026-07-02

## 工作流步骤

### 1. 检查阶段
- 检查 Git 仓库状态
- 识别未提交的文件变更
- 检查远程仓库连接

### 2. 提交阶段
- Git add (添加变更文件)
- Git commit (提交变更)
- 生成提交信息

### 3. 推送阶段
- Git push (推送到远程仓库)
- 处理推送冲突
- 验证推送结果

### 4. 报告阶段
- 生成同步报告
- 创建任务 JSON (如需要)
- 推送结果到负一屏

## 使用示例

```powershell
# 示例：GitHub 同步推送
$repoPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
Set-Location $repoPath

# 1. 检查状态
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "发现变更，开始同步..."
    
    # 2. 添加并提交
    git add .
    $commitMsg = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMsg
    
    # 3. 推送到远程
    $pushResult = git push origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "推送成功"
        
        # 4. 生成报告
        $report = @"
# GitHub 同步报告

## 执行时间
$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## 提交信息
- Commit: $commitMsg
- 变更文件数: $($gitStatus.Count)

## 推送结果
成功
"@
        $report | Out-File -FilePath "GitHub同步报告_$(Get-Date -Format 'yyyyMMdd_HHmm').md" -Encoding UTF8
    } else {
        Write-Host "推送失败: $pushResult"
    }
} else {
    Write-Host "无变更，跳过同步"
}
```

## 常见问题和解决方案

### 问题1: Git push 失败 (网络问题)
**解决方案:**
- 检查网络连接
- 配置代理 (如需要)
- 重试机制 (最多3次)

### 问题2: 合并冲突
**解决方案:**
- 先 git pull 拉取远程变更
- 解决冲突后重新提交

### 问题3: 认证失败
**解决方案:**
- 检查 Git 凭证配置
- 使用 SSH key 或 Personal Access Token

## 自动化建议
- 定时执行 (建议每天1-2次)
- 集成到 Cron 任务
- 推送失败时发送告警

## 注意事项
- 确保 .gitignore 配置正确
- 大文件使用 Git LFS
- 敏感信息不要提交到仓库

## 相关 Skill
- git-operations (Git 操作)
- cron-task-manager (定时任务)
- file-sync-workflow (文件同步)
