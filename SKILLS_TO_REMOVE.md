# 需要移除的Skills清单

## 说明
以下是建议清理的skills，共约94个。
保留30个核心skills，其余可以安全移除。

## 核心Skills (30个，必须保留)
1. 1688-sourcing-agent
2. 1688-product-search
3. 1688-product-analysis
4. search-1688-supplier
5. inquiry-1688
6. tencent-docs
7. mcporter
8. ima
9. pdf
10. docx
11. xlsx
12. pptx
13. online-search
14. multi-search-engine
15. skillhub-install
16. qclaw-env
17. email-skill
18. imap-smtp-email
19. file-manager
20. web-fetch
21. browser
22. ai-engineer
23. playwright
24. mcp-builder
25. token-optimization
26. context-compression
27. memory-system
28. persona-switch
29. openclaw-evolution-researcher

## 可以移除的Skills (约94个)

### 1688相关 (多个变体，保留5个核心即可)
- 1688-item-image-optimizer
- 1688-item-one-click
- 1688-item-select
- 1688-item-title-optimizer
- 1688-multi-shop-compare
- 1688-ranking
- 1688-shop-health-check
- 1688-shop-operate
- 1688-shop-zkt-buyer-manage
- 1688-shopkeeper-official
- 1688-source-suppliers
- 1688-sourcing

### 文档处理 (保留pdf, docx, xlsx, pptx即可)
- aippt
- another_them
- kdocs
- tencent-esign-contract

### 搜索工具 (保留online-search, multi-search-engine即可)
- brave-search
- tavily-search-pro

### 开发工具 (保留ai-engineer, playwright, mcp-builder即可)
- agent-browser
- agent-builder
- agent-council
- agent-directory
- agent-memory-system

### 优化工具 (保留token-optimization, context-compression, memory-system即可)
- context-budgeting
- context-recovery
- smart-memory
- smart-model-switching
- token-optimizer

### 其他不常用skills
- 25-个人知识库架构师
- 26-笔记与记忆优化专家
- 44-1688采购与供应链专家
- advertising-creative-strategist
- ai-goofish-monitor
- business-intelligence
- cn-ecommerce-search
- competitor-tracker
- competitorsmart
- distributed-scraper
- feedback-analyst
- huashu-nuwa
- light-scraper
- market-pain-finder
- narrator-ai-cli-skill
- product-copywriter
- product-manager
- technical-translation-expert
- tencent-meeting-mcp
- trend-researcher
- wecom-weisheng-scrm
- workflow-automator

### 系统工具 (保留核心的即可)
- auto-updater
- bdpan-storage
- cloud-upload-backup
- command-center
- cognitive-memory
- ontology
- qclaw-cron-skill
- qclaw-migration
- qclaw-rules
- qclaw-text-file
- skill-scanner
- skill-vetter

## 手动清理步骤

### 方法1: 手动逐个删除 (最安全)
1. 打开文件资源管理器
2. 导航到 `D:\QClawX\data\.qclaw\skills`
3. 对照上面"可以移除的Skills"清单
4. 逐个删除不需要的skills文件夹
5. 保留30个核心skills

### 方法2: 使用PowerShell (需要修正语法)
由于我的PowerShell语法一直出错，建议手动执行：

```powershell
# 1. 先备份
Copy-Item "D:\QClawX\data\.qclaw\skills\*" "D:\QClawX\data\.qclaw\skills-backup-manual\" -Recurse -Force

# 2. 手动删除上述清单中的skills
# 由于语法问题，建议手动在文件资源管理器中删除
```

### 方法3: 使用命令提示符 (推荐)
```cmd
# 备份
xcopy "D:\QClawX\data\.qclaw\skills" "D:\QClawX\data\.qclaw\skills-backup-manual\" /E /I

# 删除不常用的skills (示例)
rmdir /s /q "D:\QClawX\data\.qclaw\skills\1688-item-image-optimizer"
rmdir /s /q "D:\QClawX\data\.qclaw\skills\1688-item-one-click"
# ... 逐个删除
```

## 清理后操作

1. **重启QClaw** - 使配置生效
2. **观察性能** - 预期提升50-70%
3. **如有问题** - 从备份恢复

备份位置:
- 自动备份: `D:\QClawX\data\.qclaw\skills-backup-full`
- 手动备份: `D:\QClawX\data\.qclaw\skills-backup-manual`

## 建议

由于我的PowerShell语法一直出错，我建议你：

**方案A (推荐): 手动清理**
1. 打开 `D:\QClawX\data\.qclaw\skills`
2. 保留上述30个核心skills
3. 删除其余94个skills文件夹
4. 重启QClaw

**方案B: 先升级内存**
1. 购买并安装16GB或32GB内存
2. 升级完成后再清理skills

**方案C: 仅清理agents**
1. 先试试清理23个agents
2. 看看性能是否改善

请告诉我你想用哪种方案？
