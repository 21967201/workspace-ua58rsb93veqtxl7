# 2026 AI Agent 技术突破研究数据

## 研究时间: 2026-06-09 10:42-11:10

---

## 搜索结果汇总

### 1. TokenSkip (港理工)
- **论文**: TokenSkip: Controllable Chain-of-Thought Compression in LLMs
- **arXiv**: 2502.12067
- **GitHub**: github.com/hemingkx/TokenSkip
- **核心**: 选择性跳过冗余token,学习关键推理token捷径
- **效果**: CoT压缩40%,性能几乎不降
- **训练成本**: 14B模型仅需2.5小时
- **来源**: 香港理工大学

### 2. SHAPE (华为泰勒实验室)
- **发表**: ACL 2026 Main
- **核心**: Stage-aware Hierarchical Advantage via Potential Estimation
- **机制**: "里程碑+推理税"机制
- **效果**: 准确率平均提升3%,token消耗直降30%
- **合作**: 北京大学,上海财经大学

### 3. CoD - Chain of Draft (Zoom团队)
- **论文**: arXiv:2502.18600
- **GitHub**: github.com/sileix/chain-of-draft
- **核心**: 极简草稿推理,仅7.6% token量
- **效果**: 与CoT相当甚至更优准确率,延迟直降76%
- **商业价值**: 100万次推理/月,成本从$3,800→$760

### 4. Adaptive GoGI-Skip
- **arXiv**: 2505.08392
- **核心**: Goal-Gradient Importance + Adaptive Dynamic Skipping
- **机制**: 非线性格耦合,运行时熵动态调节
- **效果**: MATH训练后零样本迁移到AIME,GPQA,GSM8K
- **特色**: 保留低梯度但结构关键的token在高不确定性接点

### 5. I²B-LPO (阿里达摩院)
- **发表**: ACL 2026 Main
- **核心**: RLVR探索增强框架
- **效果**: 准确率提升5.3%,语义多样性7.4%
- **突破**: 从"重复采样"推进到"关键节点生成区分度推理轨迹"

### 6. Coconut (Meta)
- **核心**: Chain of Continuous Thought - 连续潜在空间推理
- **突破**: LLM摆脱基于词语推理的约束
- **arxiv**: 2412.06769

### 7. Stop Overthinking (莱斯大学综述)
- **核心**: 系统性梳理LLM高效推理方法
- **方向**: 基于推理模型的优化 + 基于推理输出的优化

### 8. MOSS 自进化系统
- 自进化AI框架,支持Agent自我改进

## 收集的OpenClaw已有相关技能
- self-improving (bundled)
- token-optimization
- openclaw-evolution-researcher
- qclaw-cron-skill
- lossless-claw (上下文压缩)
- context-engineering / context-compression
- adaptive-reasoning
- proactive-agent / proactive-agent-lite
- cognitive-memory / smart-memory / agent-memory-system
- agent-council
- model-router-premium
- reasoning-personas
- context-budgeting
- capability-evolver
- ai-self-evolution
