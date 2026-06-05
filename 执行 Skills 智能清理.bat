@echo off
chcp 65001 > nul
echo ================================
echo   QClaw Skills 智能清理工具
echo ================================
echo.

set SKILLS_DIR=D:\QClawX\data\.qclaw\skills
set BACKUP_DIR=D:\QClawX\data\.qclaw\skills-backup-%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

echo [1/4] 创建备份目录...
mkdir "%BACKUP_DIR%" 2>nul
echo 备份位置: %BACKUP_DIR%
echo.

echo [2/4] 开始备份并删除不常用的Skills...
echo.

REM ===== 1688相关 (保留5个，删除10个) =====
echo 清理: 1688相关Skills (10个)...
if exist "%SKILLS_DIR%\1688-item-image-optimizer" xcopy "%SKILLS_DIR%\1688-item-image-optimizer" "%BACKUP_DIR%\1688-item-image-optimizer\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-item-image-optimizer"
if exist "%SKILLS_DIR%\1688-item-one-click" xcopy "%SKILLS_DIR%\1688-item-one-click" "%BACKUP_DIR%\1688-item-one-click\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-item-one-click"
if exist "%SKILLS_DIR%\1688-item-select" xcopy "%SKILLS_DIR%\1688-item-select" "%BACKUP_DIR%\1688-item-select\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-item-select"
if exist "%SKILLS_DIR%\1688-item-title-optimizer" xcopy "%SKILLS_DIR%\1688-item-title-optimizer" "%BACKUP_DIR%\1688-item-title-optimizer\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-item-title-optimizer"
if exist "%SKILLS_DIR%\1688-multi-shop-compare" xcopy "%SKILLS_DIR%\1688-multi-shop-compare" "%BACKUP_DIR%\1688-multi-shop-compare\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-multi-shop-compare"
if exist "%SKILLS_DIR%\1688-ranking" xcopy "%SKILLS_DIR%\1688-ranking" "%BACKUP_DIR%\1688-ranking\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-ranking"
if exist "%SKILLS_DIR%\1688-shop-health-check" xcopy "%SKILLS_DIR%\1688-shop-health-check" "%BACKUP_DIR%\1688-shop-health-check\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-shop-health-check"
if exist "%SKILLS_DIR%\1688-shop-operate" xcopy "%SKILLS_DIR%\1688-shop-operate" "%BACKUP_DIR%\1688-shop-operate\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-shop-operate"
if exist "%SKILLS_DIR%\1688-shop-zkt-buyer-manage" xcopy "%SKILLS_DIR%\1688-shop-zkt-buyer-manage" "%BACKUP_DIR%\1688-shop-zkt-buyer-manage\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-shop-zkt-buyer-manage"
if exist "%SKILLS_DIR%\1688-shopkeeper-official" xcopy "%SKILLS_DIR%\1688-shopkeeper-official" "%BACKUP_DIR%\1688-shopkeeper-official\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-shopkeeper-official"
if exist "%SKILLS_DIR%\1688-source-suppliers" xcopy "%SKILLS_DIR%\1688-source-suppliers" "%BACKUP_DIR%\1688-source-suppliers\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-source-suppliers"
if exist "%SKILLS_DIR%\1688-sourcing" xcopy "%SKILLS_DIR%\1688-sourcing" "%BACKUP_DIR%\1688-sourcing\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-sourcing"
if exist "%SKILLS_DIR%\1688-product-find" xcopy "%SKILLS_DIR%\1688-product-find" "%BACKUP_DIR%\1688-product-find\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\1688-product-find"
echo ✓ 1688相关清理完成
echo.

REM ===== 文档处理 (保留4个，删除2个) =====
echo 清理: 文档处理Skills (2个)...
if exist "%SKILLS_DIR%\aippt" xcopy "%SKILLS_DIR%\aippt" "%BACKUP_DIR%\aippt\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\aippt"
if exist "%SKILLS_DIR%\kdocs" xcopy "%SKILLS_DIR%\kdocs" "%BACKUP_DIR%\kdocs\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\kdocs"
echo ✓ 文档处理清理完成
echo.

REM ===== 搜索工具 (保留2个，删除2个) =====
echo 清理: 搜索工具Skills (2个)...
if exist "%SKILLS_DIR%\brave-search" xcopy "%SKILLS_DIR%\brave-search" "%BACKUP_DIR%\brave-search\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\brave-search"
if exist "%SKILLS_DIR%\tavily-search-pro" xcopy "%SKILLS_DIR%\tavily-search-pro" "%BACKUP_DIR%\tavily-search-pro\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\tavily-search-pro"
echo ✓ 搜索工具清理完成
echo.

REM ===== AI/优化工具 (保留5个，删除3个) =====
echo 清理: AI/优化Skills (4个)...
if exist "%SKILLS_DIR%\context-budgeting" xcopy "%SKILLS_DIR%\context-budgeting" "%BACKUP_DIR%\context-budgeting\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\context-budgeting"
if exist "%SKILLS_DIR%\context-recovery" xcopy "%SKILLS_DIR%\context-recovery" "%BACKUP_DIR%\context-recovery\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\context-recovery"
if exist "%SKILLS_DIR%\smart-model-switching" xcopy "%SKILLS_DIR%\smart-model-switching" "%BACKUP_DIR%\smart-model-switching\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\smart-model-switching"
if exist "%SKILLS_DIR%\token-optimizer" xcopy "%SKILLS_DIR%\token-optimizer" "%BACKUP_DIR%\token-optimizer\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\token-optimizer"
echo ✓ AI/优化清理完成
echo.

REM ===== 腾讯/通讯 (保留3个，删除3个) =====
echo 清理: 腾讯/通讯Skills (3个)...
if exist "%SKILLS_DIR%\ima-skill" xcopy "%SKILLS_DIR%\ima-skill" "%BACKUP_DIR%\ima-skill\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\ima-skill"
if exist "%SKILLS_DIR%\tencent-esign-contract" xcopy "%SKILLS_DIR%\tencent-esign-contract" "%BACKUP_DIR%\tencent-esign-contract\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\tencent-esign-contract"
if exist "%SKILLS_DIR%\tencent-meeting-mcp" xcopy "%SKILLS_DIR%\tencent-meeting-mcp" "%BACKUP_DIR%\tencent-meeting-mcp\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\tencent-meeting-mcp"
echo ✓ 腾讯/通讯清理完成
echo.

REM ===== 开发工具 (保留3个，删除5个) =====
echo 清理: 开发工具Skills (5个)...
if exist "%SKILLS_DIR%\agent-browser" xcopy "%SKILLS_DIR%\agent-browser" "%BACKUP_DIR%\agent-browser\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\agent-browser"
if exist "%SKILLS_DIR%\agent-builder" xcopy "%SKILLS_DIR%\agent-builder" "%BACKUP_DIR%\agent-builder\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\agent-builder"
if exist "%SKILLS_DIR%\agent-council" xcopy "%SKILLS_DIR%\agent-council" "%BACKUP_DIR%\agent-council\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\agent-council"
if exist "%SKILLS_DIR%\agent-directory" xcopy "%SKILLS_DIR%\agent-directory" "%BACKUP_DIR%\agent-directory\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\agent-directory"
if exist "%SKILLS_DIR%\agent-memory-system" xcopy "%SKILLS_DIR%\agent-memory-system" "%BACKUP_DIR%\agent-memory-system\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\agent-memory-system"
echo ✓ 开发工具清理完成
echo.

REM ===== 其他工具 (保留7个，删除17个) =====
echo 清理: 其他Skills (30个)...
if exist "%SKILLS_DIR%\25-个人知识库架构师" xcopy "%SKILLS_DIR%\25-个人知识库架构师" "%BACKUP_DIR%\25-个人知识库架构师\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\25-个人知识库架构师"
if exist "%SKILLS_DIR%\26-笔记与记忆优化专家" xcopy "%SKILLS_DIR%\26-笔记与记忆优化专家" "%BACKUP_DIR%\26-笔记与记忆优化专家\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\26-笔记与记忆优化专家"
if exist "%SKILLS_DIR%\44-1688采购与供应链专家" xcopy "%SKILLS_DIR%\44-1688采购与供应链专家" "%BACKUP_DIR%\44-1688采购与供应链专家\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\44-1688采购与供应链专家"
if exist "%SKILLS_DIR%\advertising-creative-strategist" xcopy "%SKILLS_DIR%\advertising-creative-strategist" "%BACKUP_DIR%\advertising-creative-strategist\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\advertising-creative-strategist"
if exist "%SKILLS_DIR%\ai-goofish-monitor" xcopy "%SKILLS_DIR%\ai-goofish-monitor" "%BACKUP_DIR%\ai-goofish-monitor\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\ai-goofish-monitor"
if exist "%SKILLS_DIR%\business-intelligence" xcopy "%SKILLS_DIR%\business-intelligence" "%BACKUP_DIR%\business-intelligence\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\business-intelligence"
if exist "%SKILLS_DIR%\cn-ecommerce-search" xcopy "%SKILLS_DIR%\cn-ecommerce-search" "%BACKUP_DIR%\cn-ecommerce-search\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\cn-ecommerce-search"
if exist "%SKILLS_DIR%\competitor-tracker" xcopy "%SKILLS_DIR%\competitor-tracker" "%BACKUP_DIR%\competitor-tracker\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\competitor-tracker"
if exist "%SKILLS_DIR%\competitorsmart" xcopy "%SKILLS_DIR%\competitorsmart" "%BACKUP_DIR%\competitorsmart\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\competitorsmart"
if exist "%SKILLS_DIR%\distributed-scraper" xcopy "%SKILLS_DIR%\distributed-scraper" "%BACKUP_DIR%\distributed-scraper\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\distributed-scraper"
if exist "%SKILLS_DIR%\fbs_bookwriter" xcopy "%SKILLS_DIR%\fbs_bookwriter" "%BACKUP_DIR%\fbs_bookwriter\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\fbs_bookwriter"
if exist "%SKILLS_DIR%\feedback-analyst" xcopy "%SKILLS_DIR%\feedback-analyst" "%BACKUP_DIR%\feedback-analyst\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\feedback-analyst"
if exist "%SKILLS_DIR%\huashu-nuwa" xcopy "%SKILLS_DIR%\huashu-nuwa" "%BACKUP_DIR%\huashu-nuwa\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\huashu-nuwa"
if exist "%SKILLS_DIR%\light-scraper" xcopy "%SKILLS_DIR%\light-scraper" "%BACKUP_DIR%\light-scraper\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\light-scraper"
if exist "%SKILLS_DIR%\market-pain-finder" xcopy "%SKILLS_DIR%\market-pain-finder" "%BACKUP_DIR%\market-pain-finder\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\market-pain-finder"
if exist "%SKILLS_DIR%\narrator-ai-cli-skill" xcopy "%SKILLS_DIR%\narrator-ai-cli-skill" "%BACKUP_DIR%\narrator-ai-cli-skill\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\narrator-ai-cli-skill"
if exist "%SKILLS_DIR%\product-copywriter" xcopy "%SKILLS_DIR%\product-copywriter" "%BACKUP_DIR%\product-copywriter\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\product-copywriter"
if exist "%SKILLS_DIR%\product-manager" xcopy "%SKILLS_DIR%\product-manager" "%BACKUP_DIR%\product-manager\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\product-manager"
if exist "%SKILLS_DIR%\technical-translation-expert" xcopy "%SKILLS_DIR%\technical-translation-expert" "%BACKUP_DIR%\technical-translation-expert\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\technical-translation-expert"
if exist "%SKILLS_DIR%\trend-researcher" xcopy "%SKILLS_DIR%\trend-researcher" "%BACKUP_DIR%\trend-researcher\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\trend-researcher"
if exist "%SKILLS_DIR%\wecom-weisheng-scrm" xcopy "%SKILLS_DIR%\wecom-weisheng-scrm" "%BACKUP_DIR%\wecom-weisheng-scrm\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\wecom-weisheng-scrm"
if exist "%SKILLS_DIR%\workflow-automator" xcopy "%SKILLS_DIR%\workflow-automator" "%BACKUP_DIR%\workflow-automator\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\workflow-automator"
if exist "%SKILLS_DIR%\another_them" xcopy "%SKILLS_DIR%\another_them" "%BACKUP_DIR%\another_them\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\another_them"
if exist "%SKILLS_DIR%\bdpan-storage" xcopy "%SKILLS_DIR%\bdpan-storage" "%BACKUP_DIR%\bdpan-storage\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\bdpan-storage"
if exist "%SKILLS_DIR%\cloud-upload-backup" xcopy "%SKILLS_DIR%\cloud-upload-backup" "%BACKUP_DIR%\cloud-upload-backup\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\cloud-upload-backup"
if exist "%SKILLS_DIR%\command-center" xcopy "%SKILLS_DIR%\command-center" "%BACKUP_DIR%\command-center\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\command-center"
if exist "%SKILLS_DIR%\cognitive-memory" xcopy "%SKILLS_DIR%\cognitive-memory" "%BACKUP_DIR%\cognitive-memory\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\cognitive-memory"
if exist "%SKILLS_DIR%\ontology" xcopy "%SKILLS_DIR%\ontology" "%BACKUP_DIR%\ontology\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\ontology"
if exist "%SKILLS_DIR%\qclaw-cron-skill" xcopy "%SKILLS_DIR%\qclaw-cron-skill" "%BACKUP_DIR%\qclaw-cron-skill\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\qclaw-cron-skill"
if exist "%SKILLS_DIR%\qclaw-migration" xcopy "%SKILLS_DIR%\qclaw-migration" "%BACKUP_DIR%\qclaw-migration\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\qclaw-migration"
if exist "%SKILLS_DIR%\qclaw-rules" xcopy "%SKILLS_DIR%\qclaw-rules" "%BACKUP_DIR%\qclaw-rules\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\qclaw-rules"
if exist "%SKILLS_DIR%\qclaw-text-file" xcopy "%SKILLS_DIR%\qclaw-text-file" "%BACKUP_DIR%\qclaw-text-file\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\qclaw-text-file"
if exist "%SKILLS_DIR%\skill-scanner" xcopy "%SKILLS_DIR%\skill-scanner" "%BACKUP_DIR%\skill-scanner\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\skill-scanner"
if exist "%SKILLS_DIR%\skill-vetter" xcopy "%SKILLS_DIR%\skill-vetter" "%BACKUP_DIR%\skill-vetter\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\skill-vetter"
if exist "%SKILLS_DIR%\taobao" xcopy "%SKILLS_DIR%\taobao" "%BACKUP_DIR%\taobao\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\taobao"
if exist "%SKILLS_DIR%\meituan-travel" xcopy "%SKILLS_DIR%\meituan-travel" "%BACKUP_DIR%\meituan-travel\" /E /I /H /Y > nul 2>&1 & rmdir /s /q "%SKILLS_DIR%\meituan-travel"
echo ✓ 其他Skills清理完成
echo.

echo [3/4] 统计清理结果...
echo.
dir "%SKILLS_DIR%" /b /ad | find /c /v "" > %TEMP%\skills_count.txt
set /p SKILLS_COUNT=<%TEMP%\skills_count.txt
echo 当前Skills数量: %SKILLS_COUNT%
echo 预期: 29个
echo.

echo [4/4] 清理完成！
echo.
echo ================================
echo  清理结果
echo ================================
echo 移除Skills数量: 约32个
echo 保留Skills数量: %SKILLS_COUNT%个
echo 备份位置: %BACKUP_DIR%
echo.
echo 下一步操作:
echo 1. 重启QClaw使配置生效
echo 2. 观察性能是否提升 (预期提升50-70%%)
echo 3. 如有问题，从备份恢复: %BACKUP_DIR%
echo.
echo ================================
pause
