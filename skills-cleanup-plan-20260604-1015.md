# Skills清理计划

## 当前状态
- 总skills: 124个 (严重超标)
- 建议保留: 20-30个
- 需清理: 约90-100个

## 清理原则
1. 保留30天内使用过的
2. 保留核心功能相关的
3. 保留经常使用的
4. 其他可以备份后删除

## 建议保留的Skills (30个)

### 核心工具 (10个)
1. 1688相关 (5个)
   - 1688-sourcing-agent
   - 1688-product-search
   - 1688-product-analysis
   - search-1688-supplier
   - inquiry-1688

2. 腾讯文档 (3个)
   - tencent-docs
   - mcporter
   - ima

3. 系统工具 (2个)
   - skillhub-install
   - qclaw-env

### 常用功能 (15个)
4. 文件处理
   - pdf
   - docx
   - xlsx
   - pptx

5. 网络搜索
   - online-search
   - multi-search-engine
   - brave-search

6. 开发工具
   - ai-engineer
   - playwright
   - mcp-builder

7. 优化工具
   - token-optimization
   - context-compression
   - memory-system

### 其他常用 (5个)
8. 通讯工具
   - email-skill
   - imap-smtp-email

9. 实用工具
   - file-manager
   - web-fetch
   - browser

## 可以清理的Skills (示例)

### 不常用或重复功能
1. 多个1688变体 (保留核心5个即可)
2. 多个搜索工具 (保留2-3个)
3. 多个文档工具 (保留核心的)
4. 测试或临时skills
5. 长期未更新的skills

## 执行步骤

### 第一步: 创建备份
```powershell
# 创建备份目录
New-Item -ItemType Directory -Path "D:\QClawX\data\.qclaw\skills-backup" -Force

# 备份所有skills
Copy-Item "D:\QClawX\data\.qclaw\skills\*" "D:\QClawX\data\.qclaw\skills-backup\" -Recurse -Force
```

### 第二步: 分批清理
1. 先移除明显不用的 (约30个)
2. 重启QClaw测试
3. 再移除不常用的 (约30个)
4. 重启测试
5. 重复直到保留20-30个

### 第三步: 验证性能
- 启动速度
- 响应速度
- 内存占用

## 自动化清理脚本

```powershell
# 自动识别可清理的skills
$skillsPath = "D:\QClawX\data\.qclaw\skills"
$backupPath = "D:\QClawX\data\.qclaw\skills-backup"

# 获取所有skills
$allSkills = Get-ChildItem $skillsPath -Directory

# 按最后写入时间排序
$sortedSkills = $allSkills | Sort-Object LastWriteTime

# 建议清理最后20个(最久未使用)
$toRemove = $sortedSkills | Select-Object -First 20

# 显示将要清理的skills
$toRemove | Select-Object Name, LastWriteTime | Format-Table

# 执行备份和删除
foreach ($skill in $toRemove) {
    # 备份
    Copy-Item $skill.FullName $backupPath -Recurse -Force
    # 删除
    Remove-Item $skill.FullName -Recurse -Force
    Write-Host "已移除: $($skill.Name)"
}
```

## 下一步

请告诉我:
1. 是否自动执行上述清理计划?
2. 或者你想手动选择要保留的skills?
3. 还是先升级内存硬件?
