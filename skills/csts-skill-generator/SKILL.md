# CSTS-Skill-Generator

**名称**: CSTS Skill生成器  
**描述**: 基于Collective Skill Tree Search (CSTS) 算法自动生成和评估Skills  

## 功能

1. **CSN-Gen (Collective Skill Node Generation)**
   - 使用多个LLM模型并行生成候选技能
   - 基于少样本提示 (few-shot prompting)
   - 多样性去重 (语义相似度)

2. **CSN-Assess (Collective Skill Node Assessment)**
   - 多模型作为评判评估技能质量
   - 集体质量评分 (Collective Quality Scoring)
   - 集体可迁移性评分 (Collective Transferability Scoring)

3. **技能树管理**
   - 构建结构化技能树
   - 技能检索和遍历
   - 持久化存储

## 使用方法

### 生成候选技能
```bash
python scripts/csn_gen.py \
  --task "读取PDF文件并提取文本" \
  --models "qclaw/pool-hy3-preview,gpt-4,claude-3" \
  --num-candidates 10 \
  --output candidates.json
```

### 评估技能
```bash
python scripts/csn_assess.py \
  --candidates candidates.json \
  --validation-tasks validation_tasks.json \
  --models "qclaw/pool-hy3-preview,gpt-4" \
  --output assessed.json
```

### 构建技能树
```bash
python scripts/skill_tree.py \
  --assessed assessed.json \
  --tree-output memory/csts-skill-tree.json \
  --add-to-openclaw
```

## 依赖

- Python 3.8+
- sentence-transformers (语义相似度)
- scikit-learn (多样性选择)
- networkx (技能关系图)
- openclaw Python SDK

## 参考

- **论文**: arXiv:2606.16774 (2026-06-15)
  "Collective Skill Tree Search for Agentic Large Language Models"
- **模型**: OpenClaw-Skill (论文中的训练模型)
