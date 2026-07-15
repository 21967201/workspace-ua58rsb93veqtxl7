# GitHub同步推送 工作流

## 概述
自动化同步文件到GitHub并推送的工作流。

**模式统计:**
- 出现次数: 13 次（2026-06-16 ~ 2026-07-13 历史 session 复扫确认，原记录 7 次）
- 置信度: 0.95
- 自动发现时间: 2026-07-02
- 最近更新: 2026-07-13（Distill 月检：频次 7→13，修复仍生效）

## ⚠️ 重要修正（来自 Distill 复扫实证）
本仓库默认分支为 **master**（非 main）。历史 7 次同步中 5 次 `git push` 因分支不匹配 / 网络抖动失败。
**必须用 `git rev-parse --abbrev-ref HEAD` 动态获取当前分支，禁止硬编码 `master` 或 `main`。**

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
# 示例：GitHub 同步推送（已修正分支 + 重试）
$repoPath = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"
Set-Location $repoPath

# 0. 动态获取当前分支（禁止硬编码 master/main）
$branch = (git rev-parse --abbrev-ref HEAD 2>$null)
if (-not $branch) { Write-Error "不是 Git 仓库"; exit 1 }

# 1. 检查状态
$gitStatus = (git status --porcelain 2>$null)
if ($gitStatus) {
    Write-Host "发现 $($gitStatus.Count) 项变更，开始同步..."

    # 2. 添加并提交
    git add .
    $commitMsg = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMsg | Out-Null

    # 3. 推送（带重试 + 网络失败兜底）
    $maxRetry = 3
    $pushed = $false
    for ($i = 1; $i -le $maxRetry; $i++) {
        $pushOut = (git push origin $branch 2>&1)
        if ($LASTEXITCODE -eq 0) { $pushed = $true; break }
        Write-Host "第 $i 次推送失败: $pushOut"
        if ($pushOut -match "Could not resolve|Empty reply|timed out|Connection refused") {
            # 网络类错误：等待后重试
            Start-Sleep -Seconds (10 * $i)
        } else {
            # 非网络错误（如 rejected）：先 pull --rebase 再重试一次
            git pull --rebase origin $branch 2>&1
        }
    }

    # 4. 生成报告
    $status = if ($pushed) { "成功" } else { "本地已提交，远程推送失败（网络/认证），需手动 `git push origin $branch`" }
    $report = @"
# GitHub 同步报告

## 执行时间
$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## 提交信息
- Commit: $commitMsg
- 分支: $branch
- 变更文件数: $($gitStatus.Count)

## 推送结果
$status
"@
    $report | Out-File -FilePath "GitHub同步报告_$(Get-Date -Format 'yyyyMMdd_HHmm').md" -Encoding UTF8
    Write-Host "推送结果: $status"
} else {
    Write-Host "无变更，跳过同步"
}
```

> **推送失败处理原则**：本地 `commit` 必须成功（不可因远程失败而回滚）；远程失败属网络/认证问题，记为待办并提示手动重试，不阻塞负一屏推送等后续步骤（历史 session 中负一屏推送 7/7 成功，与 GitHub 推送解耦）。

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
