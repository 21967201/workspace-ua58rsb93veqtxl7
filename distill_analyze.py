#!/usr/bin/env python3
"""
Distill 工作流发现 - Session 分析脚本
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
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
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
                            if re.search(r'(搜索|查找|分析|创建|更新|删除|读取|写入|执行|运行|检查|验证)', content):
                                session_data['tasks'].append(content[:100])  # 限制长度
                        
                        # 记录时间戳
                        ts = data.get('ts', '')
                        if ts:
                            session_data['timestamps'].append(ts)
                            
                    except json.JSONDecodeError:
                        continue
                
                if session_data['tool_calls']:  # 只保留有工具调用的 session
                    sessions.append(session_data)
                    
        except Exception as e:
            print(f"警告: 无法读取文件 {file_path}: {e}")
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
            seq = f"{tool_calls[i]} → {tool_calls[i+1]}"
            sequences[seq] += 1
    
    return sequences

def identify_workflow_patterns(sessions, min_repetitions):
    """识别工作流模式"""
    patterns = []
    
    # 定义常见工作流模式
    workflow_definitions = [
        {
            'name': '搜索-读取-总结-推送',
            'pattern': ['web_search', 'web_fetch', 'read', 'message'],
            'description': '搜索信息，读取内容，总结要点，推送结果'
        },
        {
            'name': '文件读取-编辑-写入',
            'pattern': ['read', 'edit', 'write'],
            'description': '读取文件，编辑内容，写回文件'
        },
        {
            'name': '代码分析-修复-测试',
            'pattern': ['read', 'exec', 'edit', 'exec'],
            'description': '分析代码，执行修复，编辑文件，测试验证'
        },
        {
            'name': '浏览器自动化流程',
            'pattern': ['browser', 'browser', 'browser'],
            'description': '多步骤浏览器操作（登录、导航、数据提取）'
        },
        {
            'name': '定时任务管理',
            'pattern': ['cron', 'cron', 'cron'],
            'description': '创建、查看、管理定时任务'
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
    
    report = f"""# Distill 工作流发现报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**扫描时间范围**: {(datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')} 至 {datetime.now().strftime('%Y-%m-%d')}  
**最小重复次数**: {MIN_REPETITIONS}  
**最小置信度**: {MIN_CONFIDENCE}

---

## 📊 执行摘要

| 指标 | 数值 |
|------|------|
| 扫描的 session 数量 | {total_sessions} |
| 识别的模式数量 | {len(patterns)} |
| 高价值模式数量 | {len(high_value_patterns)} |
| 创建/提议的 skill | {len(high_value_patterns)} |

---

## 🔍 详细分析结果

### 1. Session 扫描统计

- **Session 文件总数**: {total_sessions}
- **工具调用总数**: {total_tool_calls}
- **平均每个 session 工具调用数**: {total_tool_calls / total_sessions:.1f}

### 2. 工具调用序列分析

常见的工具调用序列（重复次数 ≥ {MIN_REPETITIONS}）:

"""

    # 添加序列分析
    if sequences:
        report += "\n| 序列 | 重复次数 | 置信度 |\n"
        report += "|------|----------|--------|\n"
        
        for seq, count in sorted(sequences.items(), key=lambda x: x[1], reverse=True)[:10]:
            confidence = count / total_sessions
            report += f"| {seq} | {count} | {confidence:.2f} |\n"
    else:
        report += "\n⚠️ 未找到重复的工具调用序列。\n"
    
    # 添加工作流模式
    report += "\n### 3. 工作流模式识别\n\n"
    report += "识别的完整工作流模式：\n\n"
    report += "| 模式名称 | 重复次数 | 置信度 | 状态 |\n"
    report += "|---------|----------|--------|------|\n"
    
    for pattern in patterns:
        status = "✅ 高价值" if pattern['confidence'] >= MIN_CONFIDENCE else "⚠️ 低价值"
        report += f"| {pattern['name']} | {pattern['repetitions']} | {pattern['confidence']:.2f} | {status} |\n"
    
    # 添加高价值模式详情
    if high_value_patterns:
        report += "\n### 4. 高价值模式详情\n\n"
        
        for pattern in high_value_patterns:
            report += f"""#### {pattern['name']}

- **描述**: {pattern['description']}
- **工具调用序列**: {' → '.join(pattern['pattern'])}
- **重复次数**: {pattern['repetitions']}
- **置信度**: {pattern['confidence']:.2f}
- **通用性**: {'是' if pattern['general'] else '否'}

**建议**: 为这个模式创建 skill，以便复用。

"""
    
    # 添加统计信息
    report += """---

## 📈 统计信息

### 工具使用频率

| 工具名称 | 使用次数 | 使用频率 |
|---------|----------|----------|
"""

    for tool, count in tool_usage.most_common(15):
        frequency = (count / total_tool_calls) * 100
        report += f"| {tool} | {count} | {frequency:.1f}% |\n"
    
    # 添加后续行动建议
    report += """---

## 🎯 后续行动建议

1. **为高价值模式创建 skill**
   - 使用 `skill_workshop` 工具的 `action=create` 创建提案
   - 生成 SKILL.md（包含：触发词、执行流程、工具调用、示例）

2. **优化现有工作流**
   - 根据识别的模式，优化重复的工作流
   - 减少手动操作，提高自动化程度

3. **监控新模式**
   - 定期运行此分析，发现新的工作流模式
   - 持续更新和优化 skill 库

---

## 📝 附录: 原始数据

### Session 列表

"""
    
    for session in sessions[:20]:  # 只显示前20个
        report += f"- **{session['file']}**: {len(session['tool_calls'])} 个工具调用, {len(session['tasks'])} 个任务\n"
    
    if len(sessions) > 20:
        report += f"\n... 还有 {len(sessions) - 20} 个 session\n"
    
    report += """
### 分析脚本

本分析使用的 Python 脚本: `distill_analyze.py`

---

**报告结束**
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
        skill_content = f"""# {pattern['name']} 工作流

## 触发词
- {pattern['name']}
- {pattern['description']}

## 执行流程

{' → '.join(pattern['pattern'])}

## 工具调用

"""
        
        for tool in pattern['pattern']:
            skill_content += f"- {tool}\n"
        
        skill_content += f"""
## 示例

**示例 1**: 
1. 用户请求: "{pattern['name']}"
2. 执行: {' → '.join(pattern['pattern'])}
3. 结果: 完成 {pattern['name']}

## 注意事项

- 此工作流已从 session 历史中识别
- 重复次数: {pattern['repetitions']}
- 置信度: {pattern['confidence']:.2f}
- 创建时间: {datetime.now().strftime('%Y-%m-%d')}
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
    print("=== Distill 工作流发现任务 ===")
    print(f"扫描时间范围: {(datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')} 至 {datetime.now().strftime('%Y-%m-%d')}")
    print(f"最小重复次数: {MIN_REPETITIONS}")
    print(f"最小置信度: {MIN_CONFIDENCE}")
    print()
    
    # 步骤 1: 加载 session 数据
    print("步骤 1: 扫描 session 文件...")
    cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)
    sessions = load_sessions(SESSION_DIR, cutoff_date)
    
    if not sessions:
        print("  ⚠️ 未找到符合条件的 session 文件")
        print("  建议: 检查 session 目录或延长扫描时间范围")
        return
    
    print(f"  找到 {len(sessions)} 个 session 文件")
    print()
    
    # 步骤 2: 提取工具调用序列
    print("步骤 2: 提取工具调用序列...")
    sequences = extract_tool_sequences(sessions)
    print(f"  找到 {len(sequences)} 个不同的工具调用序列")
    print()
    
    # 步骤 3: 识别工作流模式
    print("步骤 3: 识别工作流模式...")
    patterns = identify_workflow_patterns(sessions, MIN_REPETITIONS)
    print(f"  识别到 {len(patterns)} 个工作流模式")
    print()
    
    # 步骤 4: 计算工具使用频率
    print("步骤 4: 计算工具使用频率...")
    tool_usage = calculate_tool_usage(sessions)
    print(f"  共使用 {len(tool_usage)} 种不同的工具")
    print()
    
    # 步骤 5: 生成报告
    print("步骤 5: 生成报告...")
    report_path = generate_report(sessions, sequences, patterns, tool_usage, REPORT_PATH)
    print(f"  报告已保存: {report_path}")
    print()
    
    # 步骤 6: 创建 skill 提案
    print("步骤 6: 创建 skill 提案...")
    high_value_patterns = [p for p in patterns if p['confidence'] >= MIN_CONFIDENCE]
    proposals = create_skill_proposals(high_value_patterns, WORKSPACE_DIR)
    
    if proposals:
        print(f"  已创建 {len(proposals)} 个 skill 提案:")
        for proposal in proposals:
            print(f"    - {proposal['skill_name']}: {proposal['proposal_path']}")
    else:
        print("  ⚠️ 没有高价值模式可创建 skill")
    print()
    
    # 完成
    print("=== 任务完成 ===")
    print(f"报告位置: {report_path}")
    print(f"高价值模式: {len(high_value_patterns)} 个")
    print(f"Skill 提案: {len(proposals)} 个")

if __name__ == "__main__":
    main()
