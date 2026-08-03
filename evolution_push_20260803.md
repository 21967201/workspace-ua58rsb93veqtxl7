【系统自动进化 2026-08-03】

结论：本周无 P0 级外部技术突破，但内部审计挖出 3 个 P0 级线上缺陷，已全部修复并验证。

核心成果：skill-router 搜索准确率 0% → 100%
- 缺陷1：auto_partition() 清空索引后回填逻辑是一句 TODO pass，search() 对任何查询恒返回 0 结果
- 缺陷2：corpus-ref 用 Python 内置 hash()，受 PYTHONHASHSEED 随机化，跨进程不一致，三原语链路直接崩溃
- 缺陷3：中文长句未分词，整段中文当单个 term，子串匹配永远失败
- 缺陷4：skill-loader / today-task 两个 SKILL.md 编码严重损坏（today-task 905 行中 502 行乱码），导致无法被索引

修复验证（真实运行，非单元测试）：
- bench_router.py 16 条查询：Top-1 100%，Top-3 100%
- router.py demo：从 KeyError 崩溃变为 exit 0
- stable_ref 跨 3 个独立进程输出一致
- 已建可重复回归基准 bench_router.py，纳入每周固定回归项

新技术监控：5 项候选，最高 P1（context-compress，工具输出压缩 93%，MCP+hook 形态），需 >1h 集成工作量且触及核心链路，转人工审核，下周专项评估。

元教训：6-20 的优化报告写着"方案3 完成，Token 节省 99%"，实测 0% 且直接崩溃 —— 当时一次真实基准都没跑过。已用基准脚本堵住这个口子。

未实施（需人工确认）：context-compress 集成、Git 工作区 565 项变更清理、.qclaw/skills 183 个 SKILL.md 编码全量审计。
