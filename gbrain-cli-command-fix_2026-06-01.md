# GBrain CLI命令修复报告

## 任务目标
修复定时任务中使用的无效GBrain CLI命令，根据实际CLI能力重新设计任务流程。

## 问题发现

### 无效的CLI命令（定时任务中使用的）
1. `gbrain enrich --tier=1` ❌ (不存在)
2. `gbrain dream --promotion` ❌ (不存在)  
3. `gbrain cycle --dream` ❌ (不存在)

### 实际GBrain CLI命令（从`gbrain --help`确认）
```
SETUP: init, migrate, upgrade, check-update, doctor, integrations
PAGES: get, put, delete, list
SEARCH: search, query, ask
IMPORT/EXPORT: import, sync, export
FILES: files list/upload/upload-raw/signed-url/sync/verify
EMBEDDINGS: embed
LINKS: link, unlink, backlinks, graph
TAGS: tags, tag, untag
TIMELINE: timeline, timeline-add
TOOLS: publish, check-backlinks, lint, report
ADMIN: stats, health, history, revert, config, serve, call, version
```

## 根本原因分析

根据GBrain文档(`GBRAIN_SKILLPACK.md`, `enrichment-pipeline.md`, `cron-schedule.md`)：

1. **"enrich"** - 是**7-step协议**（Enrichment Pipeline），不是CLI命令
2. **"dream"** - 是**nightly cron job概念**，不是CLI命令
3. **"cycle"** - 是**梦境循环阶段**，不是CLI命令
4. **"tier=1/2"** - 是**重要性分类系统**（Tier 1=10-15 API调用，Tier 2=3-5 API调用）

## 正确实现方式

### 1. Enrichment Pipeline协议实现
```bash
# 替代: gbrain enrich --tier=1

# Step1: 实体检测
entities = extract_entities(signal)

# Step2: 检查brain状态
for entity in entities:
    existing = gbrain search "{entity.name}"
    if existing:
        path = "UPDATE"
    else:
        path = "CREATE"

# Step3: 确定tier（根据重要性）
tier = classify_tier(entity)
# Tier1: 关键人物/公司，完整流水线
# Tier2: 重要人物，中等丰富度
# Tier3: 次要提及，基础丰富度

# Step4: 运行外部查询（按优先级）
data["brain"] = gbrain search "{entity.name}"  # 总是第一步
if tier <= 2:
    data["web"] = brave_search("{entity.name}")
if tier <= 2:
    data["twitter"] = twitter_lookup(entity.handle)
if tier == 1:
    data["linkedin"] = crustdata_enrich(entity.name)
    # ... 更多API调用

# Step5: 存储原始数据
gbrain put_raw_data <entity_slug> --data '{...}'

# Step6: 写入brain页面
gbrain put <entity_slug> --content "<compiled_truth>"

# Step7: 交叉引用图谱
gbrain link <person_slug> <company_slug>
```

### 2. Dream Cycle协议实现
```bash
# 替代: gbrain dream --promotion 和 gbrain cycle --dream

# Phase 1: 实体扫描
conversations = get_todays_conversations()
for message in conversations:
    entities = detect_entities(message)
    for entity in entities:
        page = gbrain search "{entity.name}"
        if not page:
            create_page(entity)         # 新实体
        elif page.is_thin():
            enrich_page(entity)        # 薄页面
        else:
            update_timeline(entity)     # 现有页面

# Phase 2: 修复损坏引用
pages = gbrain list --type person --limit 100
for page in pages:
    for entry in page.timeline:
        if not entry.has_source_attribution():
            fix_citation(entry)
        if entry.has_tweet_url() and not entry.url_is_valid():
            fix_url(entry)

# Phase 3: 巩固记忆
patterns = detect_patterns_across_conversations()
for pattern in patterns:
    promote_to_memory(pattern)         # 短暂 → 持久知识

# Phase 4: 同步
gbrain sync --no-pull --no-embed
gbrain embed --stale
```

## 修复方案

### 方案A: 重写定时任务（推荐）
将协议转换为实际的CLI命令序列 + 外部API调用。

### 方案B: 创建GBrain包装脚本
为"enrich"、"dream"、"cycle"创建包装脚本，内部调用正确的CLI命令。

## 下一步行动

1. ✅ 已确认GBrain CLI实际命令
2. ⏳ 需要重新设计定时任务流程
3. ⏳ 实现Enrichment Pipeline协议（使用真实CLI命令）
4. ⏳ 实现Dream Cycle协议（使用真实CLI命令）
5. ⏳ 测试修复后的定时任务

## 技术细节

- GBrain版本: 0.9.1
- CLI路径: `C:\Users\Administrator\gbrain\src\cli.ts`
- 执行方式: `bun run src/cli.ts <command>` 或编译后的 `gbrain.exe`
- 文档位置: `C:\Users\Administrator\gbrain\docs\`

## 验证方法

1. 运行 `gbrain --help` 确认可用命令
2. 阅读 `docs/guides/enrichment-pipeline.md` 了解Enrichment协议
3. 阅读 `docs/guides/cron-schedule.md` 了解Dream Cycle协议
4. 使用真实CLI命令测试每个步骤

---
*报告生成时间: 2026-06-01 11:48 GMT+8*
*任务状态: 已识别问题，待修复*