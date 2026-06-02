# GBrain Tier1 Enrichment 协议实现指南

## 概述
**替代命令**: `gbrain enrich --tier=1` (不存在)
**实际实现**: 7-step协议，需要组合多个GBrain CLI命令和外部API

## 协议步骤

### Step 1: 实体检测
从输入信号中提取实体（人名、公司名、关联组织）

```powershell
# 示例：从文本中检测实体
$text = "与张三讨论了AI项目，联系了ABC公司"
# 使用NLP或规则提取：张三、ABC公司
```

### Step 2: 检查Brain状态 (UPDATE vs CREATE)
```powershell
# 对于每个检测到的实体
$entity = "张三"
$existing = bun run "C:\Users\Administrator\gbrain\src\cli.ts" search "$entity" 2>&1

if ($existing -match "Found \d+") {
    $path = "UPDATE"
    # 获取现有页面
    $page = bun run "C:\Users\Administrator\gbrain\src\cli.ts" get "$entity" 2>&1
} else {
    $path = "CREATE"
}
```

### Step 3: 确定Tier（重要性分级）
```powershell
# Tier 1: 关键人物/公司 (10-15 API调用)
# - 核心团队成员
# - 重要客户/合作伙伴
# - 投资组合公司

# Tier 2: 重要人物 (3-5 API调用)
# - 偶尔互动的人
# - 行业联系人

# Tier 3: 次要提及 (1-2 API调用)
# - 短暂提及的实体

$tier = 1  # 假设这是Tier 1实体
```

### Step 4: 运行外部查询（按优先级）

#### 4.1 总是先查询Brain (免费)
```powershell
$brainData = bun run "C:\Users\Administrator\gbrain\src\cli.ts" search "$entity" 2>&1
```

#### 4.2 Tier <= 2: Web搜索
```powershell
if ($tier -le 2) {
    # 调用Brave Search API
    $webData = Invoke-RestMethod -Uri "https://api.search.brave.com/res/v1/web/search?q=$entity" `
        -Headers @{"X-Subscription-Token" = $env:BRAVE_API_KEY}
}
```

#### 4.3 Tier <= 2: Twitter查询
```powershell
if ($tier -le 2) {
    # 调用Twitter API
    # 需要实体的Twitter handle
    $twitterHandle = "example_handle"
    $twitterData = Invoke-RestMethod -Uri "https://api.twitter.com/2/users/by/username/$twitterHandle" `
        -Headers @{"Authorization" = "Bearer $env:TWITTER_BEARER_TOKEN"}
}
```

#### 4.4 Tier == 1: LinkedIn丰富化
```powershell
if ($tier -eq 1) {
    # 调用Crustdata API (LinkedIn数据)
    $linkedinData = Invoke-RestMethod -Uri "https://api.crustdata.com/v1/enrich?name=$entity" `
        -Headers @{"Authorization" = "Bearer $env:CRUSTDATA_API_KEY"}
    
    # 检查连接数 < 20 = 错误匹配，丢弃
    if ($linkedinData.connections -lt 20) {
        Write-Warning "LinkedIn匹配错误：连接数过少，可能是错误人员"
        $linkedinData = $null
    }
}
```

#### 4.5 Tier == 1: 其他API（可选）
```powershell
if ($tier -eq 1) {
    # Happenstance Research (职业轨迹、网络存在)
    # Captain API (融资、估值、团队)
    # Circleback Search (会议记录搜索)
    # Google Contacts (联系人数据)
}
```

### Step 5: 存储原始数据（可审计，可重新处理）
```powershell
$rawData = @{
    "sources" = @{
        "brain"     = @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $brainData }
        "web"       = if ($tier -le 2) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $webData } } else { $null }
        "twitter"   = if ($tier -le 2) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $twitterData } } else { $null }
        "linkedin"  = if ($tier -eq 1) { @{ "fetched_at" = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"; "data" = $linkedinData } } else { $null }
    }
}

# 存储原始数据（覆盖，不追加）
$rawData | ConvertTo-Json -Depth 10 | Out-File -FilePath "C:\Users\Administrator\gbrain\knowledge\raw_data\$entity.json" -Encoding UTF8
```

### Step 6: 写入Brain页面

#### 创建新页面 (CREATE路径)
```powershell
if ($path -eq "CREATE") {
    $content = @"
# $entity

## Executive Summary
$executiveSummary

## State
$stateData

## What They Believe
$beliefsFromTwitter

## What They're Building
$currentProjects

## What Motivates Them
$motivations

## Assessment
(用户手写评估保留在此)

## Trajectory
$trajectory

## Relationship
$relationshipNotes

## Contact
$contactInfo

## Timeline
$(Get-Date -Format "yyyy-MM-dd"): Page created via enrichment
"@
    
    # 写入brain
    $content | Out-File -FilePath "temp_$entity.md" -Encoding UTF8
    bun run "C:\Users\Administrator\gbrain\src\cli.ts" put "$entity" --content "`"$(Get-Content temp_$entity.md -Raw)`"" 2>&1
    
    # 添加时间线条目
    bun run "C:\Users\Administrator\gbrain\src\cli.ts" timeline-add "$entity" "$(Get-Date -Format 'yyyy-MM-dd')" "Page created via enrichment" 2>&1
    
    Remove-Item "temp_$entity.md" -Force
}
```

#### 更新现有页面 (UPDATE路径)
```powershell
elseif ($path -eq "UPDATE") {
    # 追加时间线条目（仅当有实质性新信息时）
    bun run "C:\Users\Administrator\gbrain\src\cli.ts" timeline-add "$entity" "$(Get-Date -Format 'yyyy-MM-dd')" "Enriched: $newSignal" 2>&1
    
    # 不要覆盖用户手写的Assessment部分！
    # API数据仅更新State、Contact、Timeline部分
}
```

### Step 7: 交叉引用图谱
```powershell
# 创建实体间的关系链接
# 示例：
# 人物 -> 公司
bun run "C:\Users\Administrator\gbrain\src\cli.ts" link "$personSlug" "$companySlug" --type "works_at" 2>&1

# 公司 -> 人物
bun run "C:\Users\Administrator\gbrain\src\cli.ts" link "$companySlug" "$personSlug" --type "employee" 2>&1

# 人物 -> 交易/项目
bun run "C:\Users\Administrator\gbrain\src\cli.ts" link "$personSlug" "$dealSlug" --type "involved_in" 2>&1

# 检查反向链接
bun run "C:\Users\Administrator\gbrain\src\cli.ts" backlinks "$entity" 2>&1
```

## 重要注意事项

### ⚠️ 不要覆盖用户手写内容
- 如果用户写了Assessment部分，**API丰富化永远不能覆盖它**
- API数据仅进入State、Contact、Timeline部分
- 用户的评估是神圣的

### ⚠️ 不要每周多次丰富同一页面
- 检查`put_raw_data`时间戳
- 如果少于一周，跳过丰富化
- 丰富化成本高，数据不会那么快变化

### ⚠️ LinkedIn连接数 < 20 = 错误匹配
- Crustdata有时返回同名不同人
- 如果LinkedIn资料连接数 < 20，几乎可以肯定是错误匹配
- 丢弃该数据

### ⚠️ X/Twitter是最被低估的数据源
- 当我们有某人的handle时，他们的推文揭示：
  - 信念 (What They Believe)
  - 正在构建什么 (What They're Building)
  - 爱好话题 (Hobby Horses)
  - 网络 (回复模式)
  - 轨迹 (发帖频率、语气变化)
- 这比LinkedIn更丰富（对于"What They Believe"和"What Makes Them Tick"）

### ⚠️ 交叉引用不是可选的
- 丰富一个人后，更新他们的公司页面
- 丰富一个公司后，更新创始人页面
- 没有交叉链接的丰富页面是图谱中的死胡同

## 验证方法

1. **丰富Tier 1人物**
   - 运行协议
   - `gbrain get <slug>`确认页面有Executive Summary、State、What They Believe、Contact、Timeline部分

2. **检查原始数据存储**
   - `gbrain get_raw_data <slug>` (或检查原始JSON文件)
   - 确认原始API响应已存储，带有`sources.{provider}.fetched_at`时间戳

3. **检查交叉引用链接**
   - `gbrain get_links <slug>`
   - 确认存在到人物公司页面、交易页面、相关实体的链接

4. **检查用户手写内容保留**
   - 检查已丰富且有用户手写Assessment的页面
   - 确认Assessment部分被保留，没有被API数据覆盖

5. **测试重新丰富同一人物**
   - 尝试重新丰富同一人物
   - 确认系统检查`fetched_at`时间戳并跳过（如果少于一周）

## PowerShell实现注意事项

1. **使用bun run执行GBrain CLI**
   ```powershell
   bun run "C:\Users\Administrator\gbrain\src\cli.ts" <command> [args] 2>&1
   ```

2. **处理JSON数据**
   ```powershell
   $data = @{ "key" = "value" } | ConvertTo-Json -Depth 10
   $data | Out-File -FilePath "output.json" -Encoding UTF8
   ```

3. **调用外部API**
   ```powershell
   $headers = @{ "Authorization" = "Bearer $env:API_KEY" }
   $response = Invoke-RestMethod -Uri $url -Headers $headers
   ```

4. **错误处理**
   ```powershell
   try {
       # 执行命令
   } catch {
       Write-Error "错误: $_"
   }
   ```

## 下一步

1. 为实际实体运行此协议（例如：重要联系人）
2. 集成外部API（Brave Search、Twitter、LinkedIn/Crustdata）
3. 测试CREATE和UPDATE路径
4. 验证交叉引用链接正确创建
5. 设置定期运行（例如：每周nightly cron）

---
*基于GBrain文档: `docs/guides/enrichment-pipeline.md`*
*创建时间: 2026-06-01*
*作者: OpenClaw AI Assistant*