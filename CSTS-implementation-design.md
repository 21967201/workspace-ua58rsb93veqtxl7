# CSTS (Collective Skill Tree Search) 算法实现设计

**论文**: arXiv:2606.16774 (2026-06-15)  
**模型**: OpenClaw-Skill (论文中的训练模型，非OpenClaw平台)  
**目标**: 将CSTS算法集成到OpenClaw，实现自动化Skill树构建

---

## 📑 算法核心（基于论文摘要）

### 1. CSN-Gen (Collective Skill Node Generation)
**目标**: 利用多模型集体知识探索多样化候选技能

**输入**:
- 子任务描述 (subtask description)
- N个评估模型 (M1, M2, ..., Mn)
- 技能模板库 (skill template library)

**输出**:
- K个候选技能节点 (candidate skill nodes)

**算法流程**:
```
1. 对每个模型 Mi:
   - 生成候选技能 Si1, Si2, ..., Sik
   - 使用少样本提示 (few-shot prompting)
   - 温度参数 T ∈ [0.7, 1.2] 增加多样性

2. 聚合所有候选技能:
   - S_all = {S11, S12, ..., Snk}
   - 去重: 基于语义相似度 (embedding cosine similarity > 0.9 视为重复)

3. 返回前K个最多样化候选技能 (diversity-promoting selection)
```

**OpenClaw集成设计**:
- 使用配置的多个模型 (qclaw/pool-hy3-preview, GPT-4, Claude 等)
- 并行调用多个模型生成候选技能
- 使用sentence-transformers计算语义相似度

---

### 2. CSN-Assess (Collective Skill Node Assessment)
**目标**: 多模型作为评判评估技能节点

**输入**:
- 候选技能节点 S
- N个评估模型 (M1, M2, ..., Mn)
- 验证任务集 (validation task set)

**输出**:
- 质量评分 (quality score): Q(S) ∈ [0, 1]
- 可迁移性评分 (transferability score): T(S) ∈ [0, 1]

**评分机制**:

#### 2.1 Collective Quality Scoring (集体质量评分)
```
对每个模型 Mi:
  1. 在验证任务上执行技能 S
  2. 评估维度:
     - 正确性 (correctness): 任务是否完成？
     - 效率 (efficiency): token消耗、步骤数
     - 鲁棒性 (robustness): 对不同输入的适应性
  3. 生成评分 qi ∈ [0, 1]

聚合: Q(S) = mean(q1, q2, ..., qn)  [或加权平均]
```

#### 2.2 Collective Transferability Scoring (集体可迁移性评分)
```
对每个模型 Mi:
  1. 在不同模型 Mj (j ≠ i) 上测试技能 S
  2. 评估维度:
     - 跨模型性能保持度 (performance retention)
     - 技能泛化能力 (generalization to unseen tasks)
  3. 生成评分 ti ∈ [0, 1]

聚合: T(S) = mean(t1, t2, ..., tn)
```

**最终评分**: Score(S) = α·Q(S) + β·T(S), 其中 α + β = 1

**OpenClaw集成设计**:
- 使用多个模型作为judges (qclaw/pool-hy3-preview, GPT-4, Claude)
- 在多个验证任务上测试技能
- 使用LLM-as-a-Judge提示模板评估质量
- 在不同模型上重新运行测试可迁移性

---

### 3. Collective Skill Reinforcement Learning
**目标**: 主动选择多个相关技能，拓宽解空间探索

**输入**:
- 技能树 (skill tree): T = {S1, S2, ..., Sm}
- 当前任务 (current task): τ
- 策略网络 (policy network): πθ

**输出**:
- 选定的技能子集 (selected skills): S_selected ⊆ T
- 增强的推理轨迹 (augmented reasoning trajectory)

**算法流程**:
```
1. 任务编码:
   - τ_emb = encoder(τ)  [使用LLM embedding]

2. 技能检索:
   - 计算相似度: sim(τ_emb, S_i_emb) for all S_i in T
   - 检索Top-K相关技能: S_retrieved = TopK(sim)

3. 策略网络:
   - 输入: τ_emb, S_retrieved
   - 输出: 选择概率 p = πθ(τ, S_retrieved)
   - 采样: S_selected ~ Categorical(p)

4. 技能组合:
   - 将 S_selected 注入到推理prompt
   - 生成多条推理轨迹 (reasoning trajectories)
   - 使用RL奖励信号 (task success, token efficiency) 更新 πθ
```

**OpenClaw集成设计**:
- 构建技能树：所有已安装Skills作为树节点
- 使用vector database (e.g., Chroma, FAISS) 存储技能embedding
- 训练一个轻量级策略网络 (可以用LLM微调或prompt-based)
- 在推理时动态检索和注入相关技能

---

## 🔧 OpenClaw集成架构设计

### 系统组件

```
┌─────────────────────────────────────────────────────┐
│          CSTS Skill Generator (CSN-Gen)           │
│  - 多模型并行生成候选技能                          │
│  - 多样性去重                                       │
└────────────────┬────────────────────────────────────┘
                 │ 候选技能节点
                 ▼
┌─────────────────────────────────────────────────────┐
│        CSTS Skill Assessor (CSN-Assess)           │
│  - 多模型评估质量                                   │
│  - 跨模型测试可迁移性                               │
│  - 输出评分和排名                                    │
└────────────────┬────────────────────────────────────┘
                 │ 评估后的技能
                 ▼
┌─────────────────────────────────────────────────────┐
│     Skill Tree Manager (技能树管理器)               │
│  - 存储已验证技能                                    │
│  - 构建技能关系图                                    │
│  - 支持检索和遍历                                    │
└────────────────┬────────────────────────────────────┘
                 │ 技能树
                 ▼
┌─────────────────────────────────────────────────────┐
│  Collective Skill RL (集体技能强化学习)             │
│  - 任务编码                                         │
│  - 技能检索                                         │
│  - 策略网络选择技能组合                              │
│  - RL训练循环                                       │
└─────────────────────────────────────────────────────┘
```

### 文件结构

```
D:\QClawX\data\workspace-ua58rsb93veqtxl7\
├── skills\
│   └── csts-skill-generator\           # CSTS Skill生成器
│       ├── SKILL.md                    # Skill定义
│       ├── scripts\
│       │   ├── csn_gen.py             # CSN-Gen算法
│       │   ├── csn_assess.py          # CSN-Assess算法
│       │   ├── skill_tree.py          # 技能树管理
│       │   └── collective_rl.py      # Collective Skill RL
│       └── references\
│           ├── CSTS-paper-summary.md  # 论文摘要
│           └── prompt-templates.md    # 提示模板
├── memory\
│   └── csts-skill-tree.json          # 持久化的技能树
└── CSTS-implementation-design.md     # 本文件
```

---

## 🚀 实施计划 (2026-06-18 ~ 2026-06-24)

### 阶段1: CSN-Gen实现 (2026-06-18)
- [ ] 创建 `csts-skill-generator` Skill
- [ ] 实现 `csn_gen.py`:
  - 多模型并行调用 (使用 `sessions_spawn` 或API)
  - 候选技能生成 (few-shot prompting)
  - 多样性去重 (sentence-transformers)
- [ ] 测试: 生成一个简单技能 (e.g., "文件读取技能")

### 阶段2: CSN-Assess实现 (2026-06-19)
- [ ] 实现 `csn_assess.py`:
  - 质量评分 (LLM-as-a-Judge)
  - 可迁移性评分 (跨模型测试)
  - 聚合评分
- [ ] 测试: 评估阶段1生成的技能

### 阶段3: 技能树管理 (2026-06-20)
- [ ] 实现 `skill_tree.py`:
  - 技能节点数据结构
  - 技能关系图 (networkx)
  - 持久化 (JSON/SQLite)
- [ ] 集成现有OpenClaw Skills到技能树

### 阶段4: Collective Skill RL (2026-06-21 ~ 2026-06-22)
- [ ] 实现 `collective_rl.py`:
  - 任务编码 (LLM embedding)
  - 技能检索 (vector similarity)
  - 策略网络 (简化版: 基于规则的排序)
  - RL训练循环 (PPO/REINFORCE)
- [ ] 测试: 在长程任务上验证技能组合效果

### 阶段5: 集成与评估 (2026-06-23 ~ 2026-06-24)
- [ ] 创建OpenClaw-Skill (集成CSTS的Agent)
- [ ] 在基准测试上评估:
  - GAIA
  - SWE-bench
  - Custom long-horizon tasks
- [ ] 对比基线: 无CSTS的OpenClaw
- [ ] 生成评估报告

---

## 📊 预期收益

| 指标 | 基线 | 目标 | 提升 |
|------|------|------|------|
| 长程规划成功率 | 60% | 80% | +20% |
| 工具使用准确率 | 75% | 90% | +15% |
| 技能泛化能力 | 50% | 75% | +25% |
| Token效率 | 100% | 80% | +20%↓ |

---

## 🚨 风险与缓解

### 风险1: 多模型调用成本高
**缓解**: 
- 使用本地模型 (qclaw/pool-hy3-preview) 作为主要生成器
- 限制候选技能数量 K ≤ 10
- 缓存评估结果

### 风险2: 技能树爆炸
**缓解**:
- 定期剪枝低评分技能 (Score < threshold)
- 限制技能树大小 (Max nodes = 1000)
- 使用向量数据库高效检索

### 风险3: RL训练不稳定
**缓解**:
- 使用简化的策略网络 (基于规则)
- 逐步增加任务复杂度
- 使用课程学习 (curriculum learning)

---

## 📝 参考文献

1. **CSTS论文**: arXiv:2606.16774 (2026-06-15)
   - Title: "Collective Skill Tree Search for Agentic Large Language Models"
   - Authors: Tianyi Lin et al.

2. **相关技术**:
   - Tree of Thoughts (ToT): 树搜索推理
   - Skill Reinforcement Learning: 技能增强的RL
   - LLM-as-a-Judge: 使用LLM评估生成内容

---

**创建时间**: 2026-06-18 10:15  
**创建者**: OpenClaw Agent (P0级突破自动集成)  
**优先级**: 🔥 最高优先级 (P0级)  
**预期完成**: 2026-06-24
