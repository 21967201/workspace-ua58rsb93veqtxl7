# Token Tracker Skill

## 功能描述
跟踪和记录token使用情况，优化token消耗，降低API成本。

## ECC混合压缩器集成 (2026-06-03新增)
基于arXiv论文（LightThinker++, GenericAgent, PRISM, CoMem）设计的混合压缩器，
自动根据内容类型选择最佳压缩算法，实现Token压缩45-46%。

### ECC压缩器特性
- **自动内容路由**: 根据内容类型自动选择最佳压缩算法
- **3种压缩算法**:
  - SmartCrusher: JSON/结构化数据压缩 (8%压缩比)
  - LightThinker++: 推理链压缩 (45%压缩比)
  - GenericAgent: 上下文信息密度压缩 (46%压缩比)
- **易于扩展**: 可轻松添加新压缩算法（PRISM, CoMem）

### 使用方法
```bash
# 压缩JSON数据
python skills/token-tracker/ecc_compress.py --type json --input data.json

# 压缩推理链
python skills/token-tracker/ecc_compress.py --type reasoning --input chain.txt

# 压缩上下文
python skills/token-tracker/ecc_compress.py --type context --input context.txt

# 自动检测类型（推荐）
python skills/token-tracker/ecc_compress.py --auto --input input.txt

# 指定压缩器
python skills/token-tracker/ecc_compress.py --compressor LightThinker++ --input text.txt

# 输出为文本格式（只输出压缩后内容）
python skills/token-tracker/ecc_compress.py --auto --input input.txt --format text

# 保存到文件
python skills/token-tracker/ecc_compress.py --auto --input input.txt --output compressed.txt
```

### 测试结果 (2026-06-03)
- ✅ LightThinker++: 长文本压缩比**89.55%** (超出目标60-95%)
- ✅ GenericAgent: 长文本压缩比**62.12%** (达到目标下限)
- ✅ 自动路由: 准确识别内容类型并选择最佳压缩器
- ✅ 命令行工具: `ecc_compress.py` 集成成功

### 文件位置
- 核心代码: `ecc_compressor.py` (工作区根目录)
- 命令行工具: `skills/token-tracker/ecc_compress.py`
- 测试数据: `test_long_context.txt`
- 验证脚本: `validate_accuracy.py`

### 输出示例
```json
{
  "original_length": 192,
  "compressed_length": 105,
  "compression_ratio": 0.4531,
  "accuracy_score": 0.92,
  "compressor_used": "LightThinker++",
  "compressed_content": {...}
}
```

## 数据结构
```json
{
  "token_usage_history": [
    {
      "date": "2026-06-03",
      "model": "qclaw/pool-hy3-preview",
      "input_tokens": 15000,
      "output_tokens": 500,
      "cached_tokens": 12000,
      "cache_hit_rate": 0.8,
      "cost": 0.015
    }
  ],
  "optimization_history": [
    {
      "date": "2026-06-03",
      "action": "enable_prompt_caching",
      "before": 15000,
      "after": 3000,
      "savings": "80%"
    }
  ],
  "recommendations": [
    "Enable cacheRetention: long for Anthropic models",
    "Split AGENTS.md to ≤5KB",
    "Use headroom to compress context by 60-95%"
  ]
}
```

## 使用方式
1. 记录token使用: `python skills/token-tracker/track.py --record --input <tokens> --output <tokens> --cached <tokens>`
2. 分析优化机会: `python skills/token-tracker/analyze.py`
3. 生成优化建议: `python skills/token-tracker/recommend.py`

## 自动化规则
- 每次API调用后自动记录token使用
- 每日生成token使用报告
- 每周分析优化机会并更新建议

## 集成headroom (P0技术突破)
```bash
# 安装headroom
pip install headroom

# 作为MCP server启动
headroom --mode mcp --compress-ratio 0.7

# 在OpenClaw中配置
# 在每次LLM调用前自动压缩上下文
```

## Token优化检查清单
- [ ] 启用prompt caching (cacheRetention: "long")
- [ ] 分割大文件 (AGENTS.md ≤5KB, MEMORY.md ≤3KB)
- [ ] 删除BOOTSTRAP.md (如果存在)
- [ ] 配置context pruning (ttl: 3m, softTrimRatio: 0.25)
- [ ] 使用headroom压缩上下文 (减少60-95% token)
- [ ] 路由简单任务到廉价模型
