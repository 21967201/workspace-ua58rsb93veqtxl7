# Rejected Buffer 使用说明

## 目的
记录被拒绝的编辑提案，避免重复错误，加速优化收敛。

## 适用场景
1. **ECC压缩器优化** - 记录压缩失败的参数配置
2. **headroom集成** - 记录兼容性失败的版本
3. **技术突破集成** - 记录集成失败的突破

## 文件格式
每个被拒绝的编辑提案以JSON保存：

```json
{
  "id": "rej_<skill>_<timestamp>_<seq>",
  "timestamp": "ISO 8601格式",
  "skill": "技能名称",
  "step": 优化步骤编号,
  "epoch": 优化周期编号,
  "rejected_reason": "拒绝原因（定量描述）",
  "edit_proposal": "编辑提案内容",
  "target_dimension": "目标维度（如compression_ratio, token_reduction）",
  "failure_pattern": "失败模式（用于模式识别）",
  "test_case": "测试用例文件路径",
  "expected": "预期结果",
  "actual": "实际结果"
}
```

## 容量管理
- 保留最近 **50条** 记录
- 超限时压缩为 **失败模式摘要**

## 使用方式

### 写入Rejected Buffer
```python
import json
from datetime import datetime

rejected = {
    "id": f"rej_ecc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_001",
    "timestamp": datetime.now().isoformat(),
    "skill": "ecc-compressor",
    "step": 1,
    "epoch": 1,
    "rejected_reason": "Compression ratio dropped from 46% to 8%",
    "edit_proposal": "...",
    "target_dimension": "compression_ratio",
    "failure_pattern": "over-aggressive_compression",
    "test_case": "test.json",
    "expected": "60-80%",
    "actual": "8.28%"
}

with open(f"rejected-buffer/{rejected['id']}.json", 'w') as f:
    json.dump(rejected, f, ensure_ascii=False, indent=2)
```

### 查询Rejected Buffer（避免重复错误）
```python
import os
import json

buffer_dir = "rejected-buffer"
failure_patterns = {}

for filename in os.listdir(buffer_dir):
    if filename.endswith('.json'):
        with open(os.path.join(buffer_dir, filename), 'r') as f:
            data = json.load(f)
            pattern = data.get('failure_pattern', 'unknown')
            if pattern not in failure_patterns:
                failure_patterns[pattern] = []
            failure_patterns[pattern].append(data)

# 输出失败模式统计
for pattern, cases in failure_patterns.items():
    print(f"失败模式: {pattern} (出现 {len(cases)} 次)")
```

## 与优化流程集成

### ECC压缩器优化流程
1. 提出压缩参数调整提案
2. **检查Rejected Buffer** - 如果类似提案曾被拒绝，跳过或调整
3. 执行测试
4. 如果失败 → 写入Rejected Buffer
5. 如果成功 → 继续优化

### headroom集成流程
1. 提出集成方案
2. **检查Rejected Buffer** - 如果类似集成曾失败，先解决兼容性问题
3. 在测试环境验证
4. 如果失败 → 写入Rejected Buffer
5. 如果成功 → 集成到主会话

---

**创建时间**: 2026-06-03 14:22  
**版本**: v1.0  
**状态**: ✅ 已启用
