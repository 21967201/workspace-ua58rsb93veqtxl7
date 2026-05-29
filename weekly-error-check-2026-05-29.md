# 每周错误预防检查报告

**执行时间**: 2026-05-29 09:48:18  
**检查类型**: 每周例行检查（持续改进）

## 检查结果摘要

- **合规文件数**: 5
- **违规文件数**: 67
- **违规项数**: 67
- **文件总数**: 72
- **合规率**: 6.94%

## 违规文件分析

### 主要违规类型

1. **.git目录文件** (约60个文件)
   - Git内部文件: COMMIT_EDITMSG, config, description, HEAD, index
   - Hooks样本文件: *.sample (16个)
   - Git对象文件: 40+ 个hash值命名的文件
   - 影响: 严重误报，占比约90%

2. **缓存和数据库文件** (3个文件)
   - chroma.sqlite3 (向量数据库文件)
   - events.jsonl (事件日志文件)
   - pre_check.cpython-311.pyc (Python字节码文件)

3. **其他Git相关文件** (4个文件)
   - .git/refs/heads/master
   - .git/logs/HEAD
   - .git/logs/refs/heads/master

## 问题根因

1. **pre_check.py未排除.git目录** - 扫描了.git内部文件，这些文件不应被检查
2. **缺乏文件类型白名单** - 没有区分必需文件和临时文件
3. **检查规则过于宽泛** - 将所有非核心文件都判定为违规

## 改进措施（已更新到MEMORY.md）

### 立即行动项

1. **修改pre_check.py** - 添加.git目录排除规则
   - 预期效果: 违规项数从67降至约7项
   - 优先级: 极高

2. **更新文件类型规则** - 添加缓存文件类型排除
   - 排除: *.pyc, *.sqlite3, *.jsonl, .git/**
   - 优先级: 高

3. **修复输出编码** - 解决Windows下中文乱码问题
   - 设置PYTHONIOENCODING=utf-8
   - 优先级: 中

## 持续改进跟踪

### 错误模式统计（本周）

| 错误类型 | 出现次数 | 频率趋势 |
|---------|---------|---------|
| .git目录文件误报 | 2次 | ↗️ 上升 (20→67) |
| 缓存文件违规 | 2次 | → 稳定 |
| 编码问题 | 2次 | → 稳定 |

### 下周检查重点

1. 验证pre_check.py修改效果
2. 监控违规项数是否降至个位数
3. 评估检查规则的准确性

## 附录：完整违规清单

<details>
<summary>点击展开67个违规文件列表</summary>

1. 文件名: COMMIT_EDITMSG
2. 文件名: config
3. 文件名: description
4. 文件名: HEAD
5. 文件名: index
6. 文件名: applypatch-msg.sample
7. 文件名: commit-msg.sample
8. 文件名: fsmonitor-watchman.sample
9. 文件名: post-update.sample
10. 文件名: pre-applypatch.sample
11. 文件名: pre-commit.sample
12. 文件名: pre-merge-commit.sample
13. 文件名: pre-push.sample
14. 文件名: pre-rebase.sample
15. 文件名: pre-receive.sample
16. 文件名: prepare-commit-msg.sample
17. 文件名: push-to-checkout.sample
18. 文件名: sendemail-validate.sample
19. 文件名: update.sample
20. 文件名: exclude
21. 文件名: HEAD
22. 文件名: master
23-66. 文件名: [40+个Git对象hash文件]
67. 文件名: chroma.sqlite3
68. 文件名: events.jsonl
69. 文件名: pre_check.cpython-311.pyc

</details>

---
**报告生成时间**: 2026-05-29 09:50:00  
**下次检查时间**: 2026-06-05 09:48
