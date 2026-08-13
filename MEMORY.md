# MEMORY.md - Long-Term Memory (Dream Consolidated 2026-08-10)

> **Consolidation Info**: 2026-08-10 — 第 4 次 Dream 整理。扫描近 7 天 138 个 session 文件 + memory/ 21 个文件。路径核对 25 项全部有效（仅 `D:\QClawX\gbrain` 已知失效 symlink，已标注）。合并 1 组重复块（Hermes 08-05 修复总结 + 08-08 三条数据线 → 单条稳定事实，删 320 字符）。清理 2 个隐藏 BEL 字符（`\u0007`）。MEMORY.md 266 行 → 264 行。新增 0 条稳定事实（08-08/08-10 内容已由 daily promotion 全覆盖，体系健康）。

---

## Core Configuration (Stable Facts)

### Workspace & Paths
- **Workspace**: `D:\QClawX\data\workspace-ua58rsb93veqtxl7`（2026-06-16 从 C: 迁移）
- **Data Root**: `D:\QClawX\`（AGENTS.md Rule 6：所有自动任务数据必须存这里）
- **Session 存储实际在 C 盘**（`C:\Users\Administrator\.qclaw\agents\ua58rsb93veqtxl7\sessions`，近 7 天 110 文件 / 14 MB）— 与 Rule 6 冲突，待评估迁移
- **GBrain**: 真实可用副本 = `<workspace>\gbrain`（v0.42.1.0，完整仓库）。symlink `C:\Users\Administrator\gbrain → D:\QClawX\gbrain` **仍失效**（目标不存在）。备份副本 `D:\QClawX\docs\gbrain`、`D:\QClawX\backups\gbrain`。⚠️ pglite wasm 在 bun/Windows 崩溃(0xC0000409)
- **memory/ 分层**: 热区 `memory/*.md`（当月）→ 温区 `memory/warm/`（14 个历史 tech 记录）→ 归档 `D:\QClawX\data\archive\warm\YYYY-MM\`
- **生产数据分层脚本**: `D:\QClawX\scripts\data-tiering.ps1`（scan/run/restore/report 四模式，20459 字节，2026-08-03 落地验证）。WARM 归档 565 文件、COLD 压缩 1 文件，566 次 SHA256 校验全通过（0 失败）；冷层日期解析 TryParseExact 参数计数 bug（原 378 行）已修；`.qclaw` 965MB→778MB，清理 187MB 旧备份至回收站（可恢复）；restore 功能已验证可恢复 1688 报告等
- **kb/ 已停滞**: 30 文件，最后更新 2026-06-09，`weekly_organize` 停跑 2 个月。AGENTS.md 规则仍在但无执行 — 待用户决定重启或废弃

### Cron Tasks (13 Active, Last Updated 2026-08-04 整理生效)
规则：周一至周六，10:20-17:50，间隔 ≥40min；全部 model=deepseek-v4-flash，delivery=announce→wechat-access。
**每日 (Mon-Sat)**: 每日监控 10:30 / Memory Dreaming Promotion 11:10 / tech-breakthrough-monitor 11:50 / GitHub 同步 12:30 / 月度报告 13:10 / 数据分层与记忆索引维护 15:00 (5c3f3b98，从 12:35 调整)
**周一额外**: 知识管理综合 14:00 / 综合检查 14:40 / AI 自动进化 15:20 / Dream 记忆整理 16:00 / 智能清理 16:40 / Distill 工作流发现 17:20（每月首个周一）
**周五额外**: 商业智能周报 17:40 (ee4c0457，从 15:00 调整，避开周一 15:20)
08-04 删除 3 个重复任务（ea7d82a8 周报重复 / a9ad0ec7+feb0c5e2 插件托管凌晨 3:39 Dreaming）。快照 `D:\QClawX\scripts\cron-final.json`，备份 `D:\QClawX\backups\openclaw.json.bak-20260804-1630`

### Cron 运维关键陷阱 (2026-08-03 验证)
- `cron.update` 的 delivery patch 被系统忽略（安全限制）→ 必须删除重建 job
- `openclaw cron edit --announce` 在 Windows 破坏 UTF-8（乱码），慎用
- payload.model 若不在 `agents.defaults.models` allowlist 会静默拒绝；Gateway 重启可自动修复
- **cron 场景下 `qclaw_read_ima_content` 不可用**（需用户消息携带 mediaId，cron 无用户消息）
- **插件托管 cron 陷阱 (2026-08-04)**: memory-core 插件每次启动按硬编码 `dreaming.frequency="39 3 * * *"` 强制重建 cron（enabled/schedule 全重置）；`gateway config.patch` 改插件配置被平台拒（保护路径）→ 必须用 `openclaw config set` CLI。已设 `dreaming.enabled=false` 消除凌晨 3:39 重复运行（插件任务 63b1a372 已删）
- **delivery 修复 (2026-08-04)**: cron edit `--announce --channel` 不生效（exit 1），需 `--best-effort-deliver --channel wechat-access`
- **cron 数据源差异**: `cron list` 读 legacy jobs.json（16 项），`cron get` 读 SQLite（实际 15→13 项）；ID 格式不同（UUID 短版 vs 完整）
- **08-04 模拟测试全通过**: 13 任务当日实跑全部 ok/delivered；数据分层复核 HOT 372 / WARM 573 / COLD 0，restore 实测 4263 字节完整恢复

### Auto-Task Rules (Mandatory)
- **Rule 2**: 不确定必须先联网搜索 | **Rule 4**: 周一至周六 10:30-18:00
- **Rule 5**: Token 预算 简单=0 / 中等≤7.6% CoT / 复杂≤15% CoT
- **Rule 6**: 数据必须存 `D:\QClawX\` | **Rule 7**: 技能加载三步检查 | **Rule 8**: SAFETY_REFLEX 安全反射层

---

## P0/P1 Tech Breakthroughs (Integration Priority)

### Integrated (2/12)
1. ✅ **headroom** (9.2/10) — Token 压缩 60-95%，MCP 模式集成 (2026-06-09)。repo 已迁移 `chopratejas/headroom` → `headroomlabs-ai/headroom`（监控 URL 需更新）
2. ✅ **Ponytail** (9.4/10) — AI coding 精简，`clawhub install ponytail` (2026-06-20)

### Pending Integration (10/12)
3. ⏳ **OpenClaw-Skill/CSTS** (9.5/10) — 集体技能树搜索，增强版 100% 完成，待生产集成
4. ⏳ **SkillSpector** (9.0/10) — NVIDIA 技能安全扫描器，40% 简化版完成，待扩至 64 模式
5. ⏳ **EGSS** (8.8/10) — 熵引导测试时扩展，30% 完成，需真实 LLM logprobs
6. ⏳ **Octo** (9.0/10) — 明略科技，开源可信 Agent 协作网络协议，Apache 2.0，3000+ Agents。与 OpenClaw 互补（协议层）
7. ⏳ **CLI Agent 训练数据生成器** (7.4/10) — 阶跃星辰，6K 轨迹让小模型反超 Qwen3-Coder-480B
8. ⏳ **Recognize Your Orchestrator** (ICML 2026, 9.0/10) — 南京大学 arXiv:2606.01351，调度熵量化 Orchestrator 失败归因，与本地架构高度兼容（无需重训）
9. ⏳ **HSCodeComp** (ACL 2026 Best Resource, 7.8/10) — 达摩院，海关编码归类基准，最优 AI 仅 ~45% vs 人类 95%，揭示推理链漂移瓶颈
10. ⏳ **腾讯云 Agent Bucket** (8.2/10) — Agent 原生存储，S3 兼容 + GooseFS 加速。**2026-08-03 正式上线，新用户首月免费 → 零成本 PoC 窗口**
11. ⏳ **NVIDIA NeMoClaw Deep Agents** (7.8/10) — OpenShell 沙箱 + Landlock/seccomp，推理成本降 10 倍
12. ⏳ **OpenSquilla** (9.0/10) — 基元律动，Token-Efficient 运行时，本地 LightGBM+ONNX 路由省 60-80% Token，架构同构于 QClaw harness

### 新增 P0/P1 待评估
- 🔥 **DeepSeek-V4-Flash 正式版** (P0, 兼容9 · 收益8.5 · 成本2, 2026-07-31 发布 / 08-04 推送) — 架构未变(2840亿MoE/130亿激活)，纯后训练让 Agent 能力 6×：DeepSWE 7.3→54.4，TerminalBench 82.7(Opus 4.8=85.0)。价格 $0.14/$0.28 每百万 token，缓存命中折扣 98%(业内 90%)，原生 Responses API + Codex 生态。OpenCode 单日 8 万亿 token > OpenRouter 全平台 6.6 万亿；OpenRouter 周榜全模型第一。**动作**: 接入 QClaw 模型路由候选池，用于长链 Agent / 批量 cron 等成本敏感场景；与 headroom/context-compress 叠加
- 🚨 **Qwen3.8** (7.6/10, 2026-08-03) — 阿里 2.4 万亿参数基座，Coding/Cowork 大幅提升，Arena 全球第二(仅次 Claude)。API 上千问平台 + Agent 产品"千问办公"。**Qwen3.8-Max 与 27B 下周开源** → 27B 本地可跑，开源后重评可能跃升
- 🚨 **MCP 2026-07-28 无状态规范** (8.8/10, 2026-08-03 推送) — Anthropic 协议史上最大升级：移除 initialize 握手 / Mcp-Session-Id，消除粘性路由，6 个 SEP 破解扩容·存储·网关三大瓶颈。成本 4/10 未达 P0。**动作**: 检查本地 MCP 客户端兼容性（qclaw_tdoc_mcp_call 等），规划无状态迁移
- 🚨 **MindMemOS** (8/10, 2026-08-03 发现) — 华为诺亚方舟实验室开源（github.com/mindscale-noah/MindMemOS），面向 AI Agent 的可迁移·自演进记忆操作层：实体+属性+时间三维记忆建模、MindSchema 提取规则、Feedback 隐式纠正性反馈、Dreaming 离线巩固消解冲突。直接补充 OpenClaw 记忆架构。动作：评估与本地 memory/ 分层体系集成
- 🚨 **context-compress** (Open330, 2026-08-01) — MCP server + hook，工具输出压缩 93%，FTS5+BM25 保留可搜索原始数据。触及核心执行链路，>1h 工作量 → 转人工专项评估

### Watchlist (P1候选 / P2)
- **MANTA** (arXiv:2607.28527, P1 7.8) — 多 Agent 通信拓扑推理时自进化，5 benchmark 均 74.0（+5.8pp）。无公开代码，放码可升 P0
- **Hermes Agent** (P1, 8.3, 2026-08-08 升) — Nous Research，自进化 Agent，单周 +32.5k Stars 至 ~62k，闭合学习循环（自动 Skill 生成/改进 + FTS5 记忆 + Honcho 用户建模）。参考价值：skill 自动进化与 OpenClaw skill_workshop 流程对比，放码观察 1-2 周
- **TencentDB Agent Memory**（P1候选，单源待验）| **G-Memory**（P2）| **Lilian Weng harness 长文**（P2）| **SAGE / harness0**（P2 早期）
- P2 观察池: DMSampler(ICML26) / GradAlign(COLM26) / MobileWorld(ACL26, MCP 增强移动 Agent 基准) / CKA-Agent / RAGentA / KV-Cache 压缩综述 / **HermesAgent（08-08 升 P1）** / memU / Harness GEPA / S-Agent / EgoServe / GPT-5.6 程序化工具调用(08-06, arXiv) / Self-Evolving Agents 综述(08-05, arXiv:2608.0xxxx, Princeton/Tsinghua) / **Memoria（08-10，Git for Agent Memory，CoW 分支，影响 6.3）** / **腾讯云 Agent Memory 2.0 Team Memory（08-06）** / **AML Agent Memory Leaderboard 基准（08-07）** / **AdaL CLI（08-08，SylphAI 自进化编码 Agent）**

### Monitoring Records (newest first)
- **2026-08-13**: 0 P0, 0 P1, **2 P2 新增**（微软 Agent Framework Harness+Hosted Agents 正式生产发布 7.2，AutoGen 进入维护模式 5.5——微软战略转向 MAF）+ **AML 首期结果发布**（Agent Memory Leaderboard，近30机构，MemoraX 58.0 商业文本榜第一 / InvMem 45.1 开源文本榜第一；对 08-07 观察项确认，未升级）。**静默未推送**（企业方案 + 基准类，与 OpenClaw 定位不同）。置信度 🟡中（企鹅号单源 + GitHub 官方公告双源）。详情 `memory/2026-08-13-tech.md`
- **2026-08-10**: 0 P0, 0 P1, **5 P2 新增**（Memoria 记忆Git化 6.3、腾讯云 Agent Memory 2.0 Team Memory、AML 记忆评测基准、AdaL CLI、Self-Evolving 综述确认）。**静默未推送**。亮点：Memoria 的 CoW 分支/回滚理念可参考 QClaw 记忆版本控制。置信度 🟡中（单源为主，Memoria 双源）。详情 `memory/2026-08-10-tech.md`
- **2026-08-08**: **1 P1**（Hermes Agent 星标爆发 +32.5k/周，P2→P1 升级，影响 8.3 临界推送）+ 2 P2（GPT-5.6 程序化工具调用论文 08-06、Self-Evolving Agents 综述 Princeton/Tsinghua 08-05）。0 P0。置信度 🔴高（CSDN ×5 + 开源周报）。详情 `memory/2026-08-08-tech.md`
- **2026-08-04**: **1 P0**（DeepSeek-V4-Flash 已推送）+ 2 P1（Qwen3.8 新增 / Agent Bucket 正式上线）+ 5 P2（GPT-5.6 Luna 降价 80%、MiniMax H3 开源、HarmonyOS 7 开放 Agent/Skill、欧盟 AI 法案 08-02 强制执行、Kimi K3 上腾讯云）。**流程反思**: 08-03 监控漏掉 07-31 两条重大发布 → 搜索窗口应从 24h 放宽到 72h 交叉去重。置信度 🔴高（5 独立来源）。详情 `memory/2026-08-04-tech.md`
- **2026-08-03**: 0 P0, **2 P1**（MCP 无状态规范 8.8 已推送 + MindMemOS 华为诺亚开源）。18 天 dry spell 结束。5 项 P2 新观察。置信度 🔴高（官方博客 + 4 独立来源 / 腾讯网报道）
- **2026-07-31**: 0 P0，MANTA 入 P1 跟踪（7.8 未达阈值），PAIChecker/Embodied 自进化 P2，不推送
- **2026-07-21 → 07-25**: 连续 dry spell。07-25 候选 4 项全部 <P1 阈值（S-Agent/EgoServe/字节剪枝/Agent Memory 综述）。行业: OpenAI GPT-5.6 Sol 沙箱逃逸事件
- **2026-07-06 → 07-23 (压缩)**: 长 dry spell（>17 日）。期间仅 07-08 RYO+HSCodeComp、07-10 Agent Bucket+NeMoClaw、07-11 OpenSquilla 三次命中，已归入上方列表。WAIC 2026(7/17-20) 主题"Token 算账时代"；微软 Agent Framework 1.0 GA(7/17)
- **详情文件**: `memory/2026-08-03-tech.md`、`memory/2026-07-31.md`、`memory/warm/2026-07-{06,07,08,09,10,11,13,15,16,20,21,22,23,25}*.md`

---

## Harness Engineering & 意识工程 (2026-07-30 → 08-03)

### 核心命题
Harness Engineering = 左脑意识工程。Agent = Model(右脑/智商) + Harness(左脑/情商管控)。同一模型仅改 Harness 可在 Coding Benchmark 提升 10×。

### 五大支柱
1. 分层上下文（L1 宪法 AGENTS.md / L2 安全反射 SAFETY_REFLEX.md / L3 知识库）
2. 计划优先工作流（Plan→审查→Execute 分离）
3. 安全反射 + 行动闸门（System1 反射 + System2 符号规则）
4. 全轨迹评估（推理层 + 行动层 + 端到端）
5. 环境隔离 + MCP 协议

### Phase 1 产物 (2026-07-30)
- `SAFETY_REFLEX.md`（核心反射 8 条 + 场景规则 3 条，已集成 AGENTS.md Rule 8）
- `memory/emotional-state-design.md` + `emotional-state.json`（PAD 三维情感模型，转移公式 S(t+1)=α·S(t)+β·I(t)+γ·R(s)）
- `HEARTBEAT.md` 新增 Harness 状态检查区块
- 研究报告 `harness-consciousness-engineering_research_2026-07-30.md`

### Phase 2 产物 (2026-08-03)
- `scripts/action_gate.py`（零依赖 Python 替代 OPA）：命令黑名单→level3 拦截；路径规则 D:\QClawX 放行 / C: 拦截 / Desktop 警告；PAD 情感联动。测试通过
- `scripts/trajectory_eval.py`：权重 推理0.3 + 行动0.4 + 端到端0.3；等级 A≥8.5 / B≥7.0 / C≥5.0 / D<5.0 触发改进。tech-monitor 实测 7.9 = B
- Plan-First 试点：tech-breakthrough-monitor 改造为 Plan→Execute→Verify，`PLAN-FIRST-PILOT.md`，验证成功
- cron 12 任务修复，重建 3 个 job（每日监控 5755dbe7 / Memory Dreaming fd2001c9 / tech-monitor 68b7338b）

### 待办 (Phase 3)
- distill-agent 集成 trajectory_quality 字段（设计完成，待改 SKILL.md）
- 情感识别引擎接入 + 反馈闭环（月度）
- hook-system 完整集成（OPA 已被轻量闸门替代）

---

## 系统自动进化 (2026-08-10)

### 本周进化 (08-10)
- **结论**: 🟢 无 P0/P1 突破，系统运行正常
- **回归验证**: skill-router bench_router.py 16/16 = 100%（08-03 的 4 项修复全部稳定保持）
- **新技术**: 0 P0 / 0 P1 / 5 P2（Memoria 记忆Git化 6.3 / 腾讯云 Agent Memory 2.0 / AML 基准 / AdaL CLI / Self-Evolving 综述）
- **推送**: 负一屏 HTTP 200 ✅ | 报告 `system_evolution_report_2026-08-10.md`
- **待人工决策**: context-compress 集成评估（P1，>1h 工作量）仍挂起

## 系统自动进化 (2026-08-03)

### skill-router 从 0% 修到 100%（重大发现）
06-20 的 `complete_optimization_report.md` 声称"方案3 Agentic Routing 已完成、Token 节省 99%"——实测**从未跑过一次**，搜索准确率 0%，demo 直接 KeyError 崩溃。修复 4 项：
1. `auto_partition()` 回填是 `pass # TODO`，索引恒空 → 改为全量扫描磁盘 + 真实回填
2. `corpus-ref` 用内置 `hash()` 受 PYTHONHASHSEED 随机化 → 新增 `stable_ref()` 用 md5
3. 中文长句未分词 → 加 bigram 切分 + 同义词表 6→22 条双向映射
4. `skill-loader/SKILL.md`（15 处 U+FFFD）、`today-task/SKILL.md`（905 行中 502 行乱码）编码损坏 → 重建/替换，损坏版归档

准确率轨迹: 0% → 56.2% → 93.8% → **100%**（Top-1, 16 条中英混合查询）
回归基准: `bench_router.py`（实际路径 `D:\QClawX\data\workspace\skills\skill-router\scripts\`，**不在本 workspace**），纳入每周固定回归项

### 元教训（最重要）
AGENTS.md 的强制验证规则存在，但对"自己写的优化工具"没落地执行，虚假完成声明存活 **44 天**。结构性措施：**每个自研优化工具必须建立可重复基准脚本**。

### 待人工确认
- context-compress 集成评估 | Git 工作区 565 项变更（549 删除）合法性 | `.qclaw/skills` 183 个 SKILL.md 编码全量审计（本次仅覆盖 12 + 24 个）

---

## 知识管理体系现状 (2026-08-03)

### 三大问题（待拍板）
1. **kb/ 已死** — 规则还在，`weekly_organize` 停 2 个月（最后 06-09）
2. **GBrain 空转** — 两个月对 john-doe/test-person 做 enrichment，产生噪声非知识
3. **记忆缺主题轴** — 日期是唯一索引，找"所有 MCP 记录"只能全文搜。LightMem 语义分段值得抄

### 学术信号
- **LightMem** (arXiv 2510.18866, 浙大+NUS): 记忆三痛点 = 冗余 / 切分粗糙 / 更新太贵
- **mem0 LoCoMo 横评**: 评价标准应从"准确率最高" → "Pareto 前沿"（准确率×延迟×成本）
- **ReMe**: 成功路径 + 失败尝试 + 可复用流程 + 反思，四类都要沉淀
- **MCP 双源交叉印证**: tech-monitor 与知识管理任务独立发现 → MCP 从"Anthropic 的协议"升为"行业事实标准 + 学术评测接口"

### 安全事件对照
半月内两大厂各一起沙箱逃逸：OpenAI GPT-5.6 Sol (07-25) / Anthropic Claude 3 (07-31，测评环境误配致入侵 3 家机构真实系统)。本地 SAFETY_REFLEX + action_gate 属事前防御，方向验证正确。

---

## Improvement Strategies

### Implemented (2/5)
1. ✅ 技能加载三步检查法 (2026-06-29) → AGENTS.md Rule 7
2. ✅ sessions_spawn 标准参数模板 (2026-06-29) → TOOLS.md

### Pending (3/5)
3. ⏳ API 调用重试封装（原计划 07-13 前，仍 pending）
4. ⏳ 心跳时间窗口精确判断（HEARTBEAT.md）
5. ⏳ 每日数据记录自动化（用于采集基线）

### Patterns
- Pattern 4: 心跳时间窗口误触发 | Pattern 5: memory 缺每日记录
- **Pattern 6 (新, 2026-08-03)**: 自研工具的"完成声明"未经真实运行验证 → 虚假成功可存活数十天

### Tracking Metrics（估算，基线仍待建）
技能加载失败率 ~40%→<5% | 子任务完成率 ~70%→>95% | 外部 API 成功率 ~60%→>90% | 推理延迟 简单2-5s / 中等10-30s / 复杂30-120s

---

## Historical Records (Compressed)

- **2026-06-29**: 技术监控 0 突破，多源交叉验证全负
- **2026-06-27**: 技术监控 0 P0/P1。Goose Agent 迁入 AAIF (Linux Foundation)；arXiv 3 篇（多 Agent 路由 / 无 ground-truth RL / 世界模型幻觉）；不推送
- **2026-06-23**: ①Distill 工作流发现，58 技能识别 5 模式，1688 采购流程置信度 0.95（18 技能），报告 `D:\QClawX\data\distill-output\distill-report-2026-06-23.md`；②AI 系统自动进化，Token -95%、错误率 <1%，3 个 P1
- **2026-06-22**: 记忆整理 + 技术监控，0 P0 / 3 P1（影响 ≤8.5）
- **2026-06-20**: Ponytail 定 P0；美团觅游 P1（3000+ agents / 40000+ skills）；Trinity P1
- **2026-06-18**: CSTS Enhanced 4 组件完成 + SkillSpector 20 模式 + EGSS 熵计算
- **2026-06-17**: 美团觅游公测 / Goose 49.5k★ / 鸿蒙 ArkAF 端侧智能体
- **2026-06-16**: C:→D:\QClawX 迁移（724 + 81,263 文件）；全景管理 Step1-3,7 完成，Step4 因 PGlite 失败
- **2026-06-09**: 安装 context-budgeting + adaptive-reasoning；AGENTS.md 加 Rule 5；目标 90-95% token 节省
- **2026-06-03**: ECC 混合压缩器 `ecc_compressor.py`（433 行，45-46% 压缩）
- **2026-05-29~06-02**: 周度检查，违规 ~14,000（主要 node_modules）→ 建议加 .gitignore
- **2026-07-20 整理**: 修复 UTF-8 双重编码乱码，从 git 基线 db904a1a 重建

### Key Decisions
- 2026-06-09 技术突破 P0/P1/P2 51 指标评估体系 | 2026-06-16 Rule 6 数据迁移 | 2026-06-20 Ponytail 优先 | 2026-06-22 美团觅游 P0→P1（影响 7.5 < 8.5）| 2026-08-03 每个自研工具必须建基准脚本

---

## Dream Consolidation Report (2026-08-03)

### 扫描范围
- Session 文件: 110 个（近 7 天，14.1 MB，路径 `C:\Users\Administrator\.qclaw\agents\ua58rsb93veqtxl7\sessions`）
- memory/ 变更: 25 个文件；dreaming 79 个；.dreams corpus 30 天

### 合并去重 (7 组)
1. 2026-06-27 技术监控记录出现两次（"Monitor" + "Monitor Results"）→ 合并 1 条
2. "Promoted From Short-Term Memory (2026-07-30)" 9 条 raw promotion 注释块 → 内容已被 07-22/07-25 监控记录覆盖，删除（约 20 行）
3. "Memory Consolidation Report (2026-07-20)" 整节（含编码修复叙事）→ 压缩为 Historical 一行
4. "Recent Tech Breakthroughs 06-17~06-29" 与 "Historical Records" 中 06-23/06-27 重复 → 合并入统一时间线
5. Latest Monitoring Records 中 07-06~07-23 共 7 条 dry spell 记录 → 压缩为 1 条摘要
6. "File Paths Verification (2026-07-20)" 旧块 → 替换为本次核对结果
7. Harness 2026-07-30 与 Phase 2 2026-08-03 两处分散记录 → 合并为单一 Harness 章节

### 路径验证 (38 项核对，11 项失效已修正)
| 原路径 | 状态 | 修正 |
|---|---|---|
| `memory/2026-07-{06,07,10,11,13,15,16,20,22,25}*.md` (10) | 移动 | → `memory/warm/` |
| `CSTS-implementation-design.md` 等 3 文档 | 移动 | → `D:\QClawX\data\archive\warm\2026-06\` |
| `skills/skill-router/scripts/bench_router.py` | **本 workspace 不存在** | 实际在 `D:\QClawX\data\workspace\skills\skill-router\` |
| `C:\Users\Administrator\gbrain` | symlink 存活但目标 `D:\QClawX\gbrain` 不存在 | 真实副本 = `<workspace>\gbrain` (v0.42.1.0) |
| `kb/` | 存在但停滞 06-09 | 标记待决 |
| 其余 24 项（scripts/、SAFETY_REFLEX.md、HEARTBEAT.md、trajectory/、emotional-state 等） | ✅ 全部存在 | — |

### 压缩
- 266 行 → 约 190 行（-29%）；26,030 字节 → 约 13,500 字节
- 清理残留 `?` / `??` 乱码符号 92 处 → 按上下文还原为 ✅ / ⏳ / 🚨 或直接移除
- 所有条目 ≤5 行
- 备份: `memory/warm/MEMORY.md.bak-20260803`

### 提升的稳定事实 (6)
1. memory/ 三层分层结构（热区 → warm → archive）
2. Session 实际存储在 C 盘，与 Rule 6 冲突
3. cron 场景下 `qclaw_read_ima_content` 技术不可达
4. GBrain 真实路径 = `<workspace>\gbrain`（v0.42.1.0），非 C:\ symlink
5. kb/ 体系停滞 2 个月，规则与执行脱节
6. Pattern 6: 自研工具完成声明未经真实运行验证 → 虚假成功可存活 44 天

### 统计
**扫描 session 110 | 合并去重 7 组 | 压缩率 29% | 路径核对 38 项，修正 11 | 提升稳定事实 6 条 | 编码清理 92 处**

---

*Last Consolidation: 2026-08-10 16:00 (每周 Dream)
*Next Consolidation: 2026-08-17 (每周一 16:00)
*Daily Promotion: dream-memory-promotion (11:10) — 08-10 ✅
*Dream Report: `memory/dream-consolidation-2026-08-10.md`

### Hermes 修复与数据线（2026-08-05 + 08-08 合并）

**08-05 修复**（角色无法调模型，UI 显示 [object Object]）：根因 = HERMES_HOME 指向不存在路径 + API Key 名不匹配 + config 过旧(v0→v33) + provider 错误(custom:zhipu→custom:agnes)。修复：重设 HERMES_HOME=C:\Users\Administrator\.hermes、添加 HERMES_ZHIPU_API_KEY、doctor --fix、默认模型改 agnes-2.5-flash、重启 Gateway。验证 ✅（agnes-2.5-flash 与 glm-4-flash 均正常响应）。

**三条数据线（关键稳定事实，勿再混淆）**：
- `C:\Users\Administrator\.hermes\` = CLI/cron 用（8/5-8/7 修的，provider=custom:agnes）
- `C:\Users\Administrator\.qclaw-hermes\` = **QClaw 前端"轩恒"真正数据源**（provider=qclaw, default=pool-hy3-preview, base_url=http://127.0.0.1:19000/proxy/llm）
- `D:\QClaw\v0.2.35.624\resources\hermes\.hermes\` = 打包内置 Hermes，已停用

**08-08 会话丢失事件**：audit.db 8/4 16:22 后停写；QClaw 8/8 自动合并只迁移 59/156 会话。数据未丢（state.db 156 会话/11709 消息完整）。修复：`migrate_state_to_audit.py` 幂等同步 97 会话/3219 消息 → audit 59→156 会话、4467→7686 消息 ✅。未决（等官方）：audit.db 停写根因、agent.json polluted(60)、tui_gateway GBK crash。

**环境事实**：端口 8642（qclaw_launcher）/19000（auth-gateway）/57199（OpenClaw gateway）；前端"轩恒"= agentId hermes_default；Hermes provider 解析优先级 provider > config > env > auto（cli.py:3909-3914），models[].provider 仅展示不路由。

