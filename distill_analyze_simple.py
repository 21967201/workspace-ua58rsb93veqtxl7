#!/usr/bin/env python3
"""
Distill 工作流发现 - Session 分析脚本 (简化版)
目标: 扫描最近 30 天的 session 历史，识别重复模式并固化为可复用 skill
"""

import json
import os
import glob
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re

# 配置
WORKSPACE_DIR = r"D:\QClawX\data\workspace-ua58rsb93veqtxl7"
SESSION_DIR = r"D:\QClawX\data\.qclaw\agents\main\sessions"
REPORT_PATH = os.path.join(WORKSPACE_DIR, f"distill-report-{datetime.now().strftime('%Y-%m-%d')}.md")

# 参数
DAYS_BACK = 30
MIN_REPETITIONS = 3
MIN_CONFIDENCE = 0.7

def load_sessions(session_dir, cutoff_date):
    """加载符合条件的 session 文件"""
    sessions = []
    
    # 查找所有 jsonl 文件
    pattern = os.path.join(session_dir, "*.jsonl")
    files = glob.glob(pattern)
    
    print(f"  在 {session_dir} 中搜索 session 文件...")
    print(f"  找到 {len(files)} 个 JSONL 文件")
    
    for file_path in files:
        # 检查文件修改时间
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        if mtime < cutoff_date:
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = {
                    'file': os.path.basename(file_path),
                    'tool_calls': [],
                    'tasks': [],
                    'timestamps': []
                }
                
                # 读取 JSONL 文件
                line_count = 0
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    line_count += 1
                    try:
                        data = json.loads(line)
                        
                        # 提取工具调用
                        if data.get('type') in ['tool.call', 'tool.result']:
                            tool_name = data.get('data', {}).get('toolName', '')
                            if tool_name:
                                session_data['tool_calls'].append(tool_name)
                        
                        # 提取任务描述
                        if data.get('type') == 'message' and data.get('data', {}).get('role') == 'user':
                            content = data.get('data', {}).get('content', '')
                            # 简单匹配任务关键词
                            if re.search(r'(search|find|analyze|create|update|delete|read|write|execute|run|check|verify)', content, re.IGNORECASE):
                                session_data['tasks'].append(content[:100])  # 限制长度
                        
                        # 记录时间戳
                        ts = data.get('ts', '')
                        if ts:
                            session_data['timestamps'].append(ts)
                            
                    except json.JSONDecodeError:
                        continue
                
                if session_data['tool_calls']:  # 只保留有工具调用的 session
                    sessions.append(session_data)
                    print(f"    已加载: {os.path.basename(file_path)} ({len(session_data['tool_calls'])} 个工具调用)")
                    
        except Exception as e:
            print(f"  警告: 无法读取文件 {file_path}: {e}")
            continue
    
    return sessions

def extract_tool_sequences(sessions):
    """提取工具调用序列"""
    sequences = defaultdict(int)
    
    for session in sessions:
        tool_calls = session['tool_calls']
        if len(tool_calls) < 2:
            continue
        
        # 提取连续工具调用对
        for i in range(len(tool_calls) - 1):
            seq = f"{tool_calls[i]} -> {tool_calls[i+1]}"
            sequences[seq] += 1
    
    return sequences

def identify_workflow_patterns(sessions, min_repetitions):
    """识别工作流模式"""
    patterns = []
    
    # 定义常见工作流模式
    workflow_definitions = [
        {
            'name': 'Search-Read-Summarize-Push',
            'pattern': ['web_search', 'web_fetch', 'read', 'message'],
            'description': 'Search information, read content, summarize key points, push results'
        },
        {
            'name': 'File-Read-Edit-Write',
            'pattern': ['read', 'edit', 'write'],
            'description': 'Read file, edit content, write back to file'
        },
        {
            'name': 'Code-Analyze-Fix-Test',
            'pattern': ['read', 'exec', 'edit', 'exec'],
            'description': 'Analyze code, execute fix, edit file, test verification'
        },
        {
            'name': 'Browser-Automation',
            'pattern': ['browser', 'browser', 'browser'],
            'description': 'Multi-step browser operations (login, navigation, data extraction)'
        },
        {
            'name': 'Cron-Task-Management',
            'pattern': ['cron', 'cron', 'cron'],
            'description': 'Create, view, manage scheduled tasks'
        }
    ]
    
    for workflow in workflow_definitions:
        match_count = 0
        
        for session in sessions:
            tool_calls = session['tool_calls']
            pattern = workflow['pattern']
            
            # 检查是否包含模式中的所有工具（顺序不重要）
            if all(tool in tool_calls for tool in pattern):
                match_count += 1
        
        if match_count >= min_repetitions:
            # 计算置信度
            confidence = (match_count / len(sessions)) * 0.8
            if len(pattern) >= 3:
                confidence += 0.2
            confidence = min(confidence, 1.0)
            
            patterns.append({
                'name': workflow['name'],
                'pattern': workflow['pattern'],
                'description': workflow['description'],
                'repetitions': match_count,
                'confidence': confidence,
                'general': True
            })
    
    return patterns

def calculate_tool_usage(sessions):
    """计算工具使用频率"""
    tool_counter = Counter()
    
    for session in sessions:
        tool_counter.update(session['tool_calls'])
    
    return tool_counter

def generate_report(sessions, sequences, patterns, tool_usage, report_path):
    """生成 Markdown 报告"""
    total_sessions = len(sessions)
    total_tool_calls = sum(len(s) for s in sessions)
    
    # 筛选高价值模式
    high_value_patterns = [p for p in patterns if p['confidence'] >= MIN_CONFIDENCE]
    
    report = f"""# Distill Workflow Discovery Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Time Range**: {(datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}  
**Min Repetitions**: {MIN_REPETITIONS}  
**Min Confidence**: {MIN_CONFIDENCE}

---

## Summary

| Metric | Value |
|--------|-------|
| Sessions Scanned | {total_sessions} |
| Patterns Identified | {len(patterns)} |
| High-Value Patterns | {len(high_value_patterns)} |
| Skills to Create | {len(high_value_patterns)} |

---

## Detailed Analysis

### 1. Session Scan Statistics

- **Total Sessions**: {total_sessions}
- **Total Tool Calls**: {total_tool_calls}
- **Avg Tool Calls per Session**: {total_tool_calls / total_sessions:.1f}

### 2. Tool Call Sequence Analysis

Common tool call sequences (repetitions >= {MIN_REPETITIONS}):

"""

    # 添加序列分析
    if sequences:
        report += "\n| Sequence | Repetitions | Confidence |\n"
        report += "|----------|-------------|------------|\n"
        
        for seq, count in sorted(sequences.items(), key=lambda x: x[1], reverse=True)[:10]:
            confidence = count / total_sessions
            report += f"| {seq} | {count} | {confidence:.2f} |\n"
    else:
        report += "\n**Warning**: No repeated tool call sequences found.\n"
    
    # 添加工作流模式
    report += "\n### 3. Workflow Pattern Identification\n\n"
    report += "Identified workflow patterns:\n\n"
    report += "| Pattern Name | Repetitions | Confidence | Status |\n"
    report += "|-------------|-------------|------------|--------|\n"
    
    for pattern in patterns:
        status = "High Value" if pattern['confidence'] >= MIN_CONFIDENCE else "Low Value"
        report += f"| {pattern['name']} | {pattern['repetitions']} | {pattern['confidence']:.2f} | {status} |\n"
    
    # 添加高价值模式详情
    if high_value_patterns:
        report += "\n### 4. High-Value Pattern Details\n\n"
        
        for pattern in high_value_patterns:
            report += f"""#### {pattern['name']}

- **Description**: {pattern['description']}
- **Tool Call Sequence**: {' -> '.join(pattern['pattern'])}
- **Repetitions**: {pattern['repetitions']}
- **Confidence**: {pattern['confidence']:.2f}
- **General**: {'Yes' if pattern['general'] else 'No'}

**Recommendation**: Create a skill for this pattern to enable reuse.

"""
    
    # 添加统计信息
    report += """---

## Statistics

### Tool Usage Frequency

| Tool Name | Usage Count | Usage Frequency |
|-----------|-------------|-----------------|
"""

    for tool, count in tool_usage.most_common(15):
        frequency = (count / total_tool_calls) * 100
        report += f"| {tool} | {count} | {frequency:.1f}% |\n"
    
    # 添加后续行动建议
    report += """---

## Next Steps

1. **Create Skills for High-Value Patterns**
   - Use `skill_workshop` tool with `action=create` to create proposals
   - Generate SKILL.md (include: trigger words, execution flow, tool calls, examples)

2. **Optimize Existing Workflows**
   - Based on identified patterns, optimize repeated workflows
   - Reduce manual operations, increase automation

3. **Monitor New Patterns**
   - Run this analysis regularly to discover new workflow patterns
   - Continuously update and optimize skill library

---

## Appendix: Raw Data

### Session List

"""
    
    for session in sessions[:20]:  # Show only first 20
        report += f"- **{session['file']}**: {len(session['tool_calls'])} tool calls, {len(session['tasks'])} tasks\n"
    
    if len(sessions) > 20:
        report += f"\n... and {len(sessions) - 20} more sessions\n"
    
    report += """
### Analysis Script

Python script used for this analysis: `distill_analyze_simple.py`

---

**End of Report**
"""
    
    # 保存报告
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path

def create_skill_proposals(patterns, workspace_dir):
    """为高价值模式创建 skill 提案"""
    proposals = []
    
    for pattern in patterns:
        if pattern['confidence'] < MIN_CONFIDENCE:
            continue
        
        # 生成 skill 名称
        skill_name = pattern['name'].replace(' ', '-').lower()
        skill_name = re.sub(r'[^a-z0-9\-]', '', skill_name)
        
        # 生成 SKILL.md 内容
        skill_content = f"""# {pattern['name']} Workflow

## Trigger Words
- {pattern['name']}
- {pattern['description']}

## Execution Flow

{' -> '.join(pattern['pattern'])}

## Tool Calls

"""
        
        for tool in pattern['pattern']:
            skill_content += f"- {tool}\n"
        
        skill_content += f"""
## Example

**Example 1**: 
1. User request: "{pattern['name']}"
2. Execution: {' -> '.join(pattern['pattern'])}
3. Result: Complete {pattern['name']}

## Notes

- This workflow was identified from session history
- Repetitions: {pattern['repetitions']}
- Confidence: {pattern['confidence']:.2f}
- Created: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        # 保存提案文件
        proposal_path = os.path.join(workspace_dir, f"skill-proposal-{skill_name}.md")
        with open(proposal_path, 'w', encoding='utf-8') as f:
            f.write(skill_content)
        
        proposals.append({
            'pattern': pattern['name'],
            'skill_name': skill_name,
            'proposal_path': proposal_path
        })
    
    return proposals

def main():
    """主函数"""
    print("=== Distill Workflow Discovery Task ===")
    print(f"Time Range: {(datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Min Repetitions: {MIN_REPETITIONS}")
    print(f"Min Confidence: {MIN_CONFIDENCE}")
    print()
    
    # 步骤 1: 加载 session 数据
    print("Step 1: Scanning session files...")
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)
    sessions = load_sessions(SESSION_DIR, cutoff_date)
    
    if not sessions:
        print("  [WARNING] No qualifying session files found")
        print("  Suggestion: Check session directory or extend time range")
        return
    
    print(f"  Found {len(sessions)} session files")
    print()
    
    # 步骤 2: 提取工具调用序列
    print("Step 2: Extracting tool call sequences...")
    sequences = extract_tool_sequences(sessions)
    print(f"  Found {len(sequences)} different tool call sequences")
    print()
    
    # 步骤 3: 识别工作流模式
    print("Step 3: Identifying workflow patterns...")
    patterns = identify_workflow_patterns(sessions, MIN_REPETITIONS)
    print(f"  Identified {len(patterns)} workflow patterns")
    print()
    
    # 步骤 4: 计算工具使用频率
    print("Step 4: Calculating tool usage frequency...")
    tool_usage = calculate_tool_usage(sessions)
    print(f"  Used {len(tool_usage)} different tools")
    print()
    
    # 步骤 5: 生成报告
    print("Step 5: Generating report...")
    report_path = generate_report(sessions, sequences, patterns, tool_usage, REPORT_PATH)
    print(f"  Report saved: {report_path}")
    print()
    
    # 步骤 6: 创建 skill 提案
    print("Step 6: Creating skill proposals...")
    high_value_patterns = [p for p in patterns if p['confidence'] >= MIN_CONFIDENCE]
    proposals = create_skill_proposals(high_value_patterns, WORKSPACE_DIR)
    
    if proposals:
        print(f"  Created {len(proposals)} skill proposals:")
        for proposal in proposals:
            print(f"    - {proposal['skill_name']}: {proposal['proposal_path']}")
    else:
        print("  [WARNING] No high-value patterns to create skills for")
    print()
    
    # 完成
    print("=== Task Complete ===")
    print(f"Report: {report_path}")
    print(f"High-Value Patterns: {len(high_value_patterns)}")
    print(f"Skill Proposals: {len(proposals)}")

if __name__ == "__main__":
    main()
