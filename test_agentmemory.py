#!/usr/bin/env python3
"""测试 agentmemory 基本功能"""

from agentmemory import create_memory, search_memory, get_memories

# 1. 创建一些测试记忆
print("=== 创建记忆 ===")
create_memory("conversation", "用户询问了agentmemory的安装方法", 
              metadata={"speaker": "user", "topic": "installation"})
create_memory("conversation", "agentmemory可以减少Token消耗", 
              metadata={"speaker": "assistant", "topic": "benefits"})
create_memory("conversation", "Claude Code内置了skill-creator", 
              metadata={"speaker": "assistant", "topic": "tools"})

# 2. 搜索记忆
print("\n=== 搜索记忆 ===")
results = search_memory("conversation", "agentmemory")
print(f"搜索 'agentmemory' 找到 {len(results)} 条记忆:")
for r in results:
    print(f"  - {r['document']}")

# 3. 获取所有记忆
print("\n=== 获取所有记忆 ===")
all_memories = get_memories("conversation", n_results=10)
print(f"总共有 {len(all_memories)} 条记忆:")
for m in all_memories:
    print(f"  - [{m['metadata'].get('speaker', 'unknown')}] {m['document']}")

print("\n=== 测试完成 ===")
