# MEMORY.md - Long-Term Memory (Dream Consolidated 2026-07-06)

> **Consolidation Info**: Cron redux (15鈫?2), patterns 4&5, tech dry spell, sessions_spawn template confirmed. All entries 鈮? lines.

---

## 馃敡 Core Configuration (Stable Facts)

### Workspace & Paths
- **Workspace**: `D:\QClawX\data\workspace-ua58rsb93veqtxl7` (migrated from C: to D: 2026-06-16)
- **Data Root**: `D:\QClawX\` (all auto-task data must save here per AGENTS.md Rule 6)
- **GBrain**: symlink `C:\Users\Administrator\gbrain` **宸插け鏁?*锛堢洰鏍?`D:\QClawX\gbrain` 涓虹┖鐩綍锛? 鐪熷疄鍙敤鍓湰: `D:\QClawX\docs\gbrain`锛堝惈 src/cli.ts + knowledge/锛変笌 `D:\QClawX\backups\gbrain`銆傗殸锔?pglite wasm 鍦?bun/Windows 宕╂簝(0xC0000409)锛宨mport 涓嶅彲鐢紝闇€绠＄悊鍛橀噸寤?symlink + 鎺掓煡 wasm 鍏煎
- **Skills Dir**: `skills/` (relative to workspace)

### Cron Tasks (12 Active, Last Updated 2026-06-22)
All tasks comply with Rule: Mon-Sat, 10:30-18:00, interval 鈮?0min.
**Daily (Mon-Sat)**:
1. 姣忔棩鐩戞帶浠诲姟 (10:30)
2. Memory Dreaming Promotion (11:10, this task)
3. tech-breakthrough-monitor (11:50)
4. 鑷姩鍚屾浠诲姟鏂囦欢鍒癎itHub (12:30)
5. 鏈堝害鎶ュ憡浠诲姟 (13:10)
**Monday Extra**:
6. 鍛ㄤ竴鐭ヨ瘑绠＄悊缁煎悎浠诲姟 (14:00)
7. 鍛ㄤ竴缁煎悎妫€鏌ヤ换鍔?(14:40)
8. AI绯荤粺鑷姩杩涘寲浠诲姟 (15:20)
9. Dream 璁板繂鏁寸悊 (16:00)
10. QClaw鏅鸿兘娓呯悊 (16:40)
11. Distill 宸ヤ綔娴佸彂鐜?(17:20, first Mon of month)
**Friday Extra**:
12. 鍟嗕笟鏅鸿兘鍛ㄦ姤 (15:00)

### Auto-Task Rules (Mandatory)
- **Rule 4 (Time Limit)**: Mon-Sat only, 10:20-18:00, no Sunday execution.
- **Rule 5 (Token Budget)**: Simple=0 token, Medium鈮?.6% CoT, Complex鈮?5% CoT.
- **Rule 6 (Data Storage)**: All data must save to `D:\QClawX\` (no C: drive).
- **Rule 2 (Uncertainty)**: Must web-search before answering uncertain questions.

---

## 馃殌 P0 Tech Breakthroughs (Integration Priority)

### Integrated (2/5)
1. 鉁?**headroom** (9.2/10) - Token compression 60-95%, already integrated (MCP mode, 2026-06-09)
2. 鉁?**Ponytail** (9.4/10) - AI coding绮剧畝, `clawhub install ponytail` (2026-06-20)

### Pending Integration (5/7)
3. 鈴?**OpenClaw-Skill/CSTS** (9.5/10) - Collective skill tree search, 100% enhanced done, pending production integration
4. 鈴?**SkillSpector** (9.0/10) - NVIDIA skill security scanner, 40% simplified done, expand to 64 patterns
5. 鈴?**EGSS** (8.8/10) - Entropy-guided test-time scaling, 30% simplified done, need real LLM logprobs

### Latest Monitoring Record (2026-07-06, 11:50 run)
- **Monitoring Coverage**: 2026-07-05, 2026-07-06; No P0/P1 breakthroughs (~9 consecutive days)
- **P0**: 0 found; **P1 (impact>8.5)**: 0 found
- **Tracked P0 items status**: headroom (stable, 60-95% token cut, GitHub Trending winner 06-07, no new release 24h); ECC (GitHub鏃ユ姤甯搁┗, no new 24h); DECS/AbstractCoT (no new citation paper 24h)
- **Notable signals (P2/watch)**: GSPO (Qwen鍥㈤槦, sequence-level RL, replaces GRPO variance issue) gaining traction 鈥?add to P1-watch; Goose migrated block/goose鈫抋aif-goose (Linux Foundation Agentic AI Foundation); OpenClaw shipped iOS/Android native apps (06-30)
- **Trend**: Tech breakthrough dry spell continues (~9 days); next catalyst ICLR 2026 (mid-July)
- **Details**: See `memory/2026-07-06-tech.md`
6. 鈴?**Octo** (9.0/10, 2026-07-01) - 鏄庣暐绉戞妧, 鍏ㄧ悆棣栦釜寮€婧愬彲淇gent鍗忎綔缃戠粶, 瀹氫箟"Agent浜掕仈缃?搴曞眰鍗忚銆侽pen/Context/Taste/Orchestration鍥涚淮搴︽爣鍑嗗寲, Apache 2.0, 3000+ Agents銆備笌OpenClaw浜掕ˉ(鍗忚灞?銆?7. 鈴?**CLI Agent璁粌鏁版嵁鐢熸垚鍣?* (7.4/10, 2026-07-01) - 闃惰穬鏄熻景, 6K杞ㄨ抗璁╁皬妯″瀷鍙嶈秴Qwen3-Coder-480B, Terminal Agent楂樻晥璁粌鏂规硶銆侾1绾ф寔缁洃鎺с€?8. 鈴?**Recognize Your Orchestrator** (ICML 2026, 9.0/10, 2026-07-07) - 鍗椾含澶у, arXiv:2606.01351. 璋冨害鐔甸噺鍖朞rchestrator澶辫触褰掑洜, Mean-Field Entropy Dynamics妗嗘灦, IWG鍙嶆帹楠岃瘉銆備笌OpenClaw Orchestrator-Executor鏋舵瀯楂樺害鍏煎(鏃犻渶閲嶈)銆?9. 鈴?**HSCodeComp** (ACL 2026 Best Resource Paper, 7.8/10, 2026-07-08) - 闃块噷宸村反杈炬懇闄? 鍟嗗搧鍑哄彛娴峰叧缂栫爜褰掔被鏂板熀鍑? 鏈€浼楢I绯荤粺浠厏45% vs 浜虹被涓撳95%銆傛彮绀篈gent鏋舵瀯缁撴瀯鎬х摱棰堬細鎺ㄧ悊閾炬紓绉?棰嗗煙鐭ヨ瘑涓嶈冻+鎺ㄧ悊骞昏銆備笌瑙勫垯鏁忔劅鍦烘櫙(鍚堣/绋庡姟/瀹¤)鐩存帴鍏宠仈銆?10. 鈴?**鑵捐浜?Agent Bucket** (8.2/10, 2026-07-10) - AI Agent鍘熺敓瀛樺偍鏈嶅姟, S3鍏煎+Space鐙珛绌洪棿+GooseFS鍔犻€? 宸插湪QClaw閮ㄧ讲(鍗庣/涓滈鏃ヤ骇)銆侾1, 鐢熸€佸奖鍝?.7銆?11. 鈴?**NVIDIA NeMoClaw Deep Agents** (7.8/10, 2026-07-10) - OpenShell娌欑+Landlock/seccomp澹版槑寮忕瓥鐣? 鎺ㄧ悊鎴愭湰闄?0鍊? Nemotron 3 Ultra寮€婧愩€侾1杈圭晫銆?12. 鈴?**OpenSquilla** (9.0/10, 2026-07-11) - GitHub opensquilla/opensquilla锛堝熀鍏冨緥鍔?鐜嬩簯楣?, Token-Efficient 鏅鸿兘浣撹繍琛屾椂銆係quillaRouter 鏈湴 LightGBM+ONNX 璺敱鐪?0-80% Token; DRACO鍙屾绗竴; Meta-Skills鑷姩娌夋穩澶嶇敤宸ヤ綔娴併€傛灦鏋勫悓鏋勪簬QClaw harness(寰唴鏍?璺敱+璁板繂+娌欑+MCP)銆侾0銆?
### Latest Monitoring Record (2026-07-08, 16:43 run)
- **Monitoring Coverage**: 2026-07-07, 2026-07-08; **1 P0 + 1 P1 found** (ends ~9-day dry spell)
- **P0**: Recognize Your Orchestrator (ICML 2026) 鈥?added to Pending Integration (#8)
- **P1 (impact>8.5)**: HSCodeComp (ACL 2026 Best Resource Paper, 8.7/10) 鈥?added to Pending Integration (#9)
- **Tracked P0 items status**: headroom (stable); ECC (stable); new RYO added Mon Jul 7
- **Details**: See `memory/2026-07-07-tech.md` and `memory/2026-07-08-tech.md`

### Latest Monitoring Record (2026-07-11, 11:50 run)
- **Monitoring Coverage**: 2026-07-10鈫?1; **1 P0 found** (break 1-day micro dry spell)
- **P0**: OpenSquilla (9.0/10, token-efficient agent runtime, 鍩哄厓寰嬪姩/鐜嬩簯楣? 鈥?added to Pending Integration #12
- **P1 (impact>8.5)**: 0
- **Tracked P0**: headroom(绋冲畾), ECC(绋冲畾), RYO(绋冲畾)
- **Trend**: Harness Engineering 鎴?026涓诲鑼冨紡; OpenSquilla 鏋舵瀯鍚屾瀯QClaw harness
- **Details**: See `memory/2026-07-11.md`

### Latest Monitoring Record (2026-07-13, 14:00 run)
- **Coverage**: 2026-07-12鈫?3; **0 P0, 0 P1** (dry spell 2 days from 07-11)
- **Paper Trends (1-week)**: Agent Memory + 鑷繘鍖?+ 鎴愭湰鎰熺煡 (SSPM 2607.09493, Agora 2607.09600, SAGEAgent 2607.09521, Agentic Memory 2601.01885, MemOS, AntiSD/GRPO)
- **P1-watch**: Agora (Agentic memory orchestration) + GSPO (sequence-level RL, replaces GRPO variance) 鈥?elevated from P2
- **GBrain Status**: symlink still broken; real copies confirmed at `D:\QClawX\docs\gbrain` and `D:\QClawX\backups\gbrain`
- **Details**: See `memory/2026-07-13.md`

### Latest Monitoring Record (2026-07-15, 09:46 run)
- **Monitoring Coverage**: 2026-07-14鈫?5 strict 24h; **0 P0, 0 P1 found** (dry spell 杩炵画5鏃?
- **P0**: 0; **P1(impact>8.5)**: 0
- **Tracked P0**: headroom(绋冲畾); ECC(鐞嗗康钀藉湴瑙?harness0, P2); DECS/AbstractCoT(鏃犳柊寮曠敤)
- **Near-window寮变俊鍙?*: ACL2026 SAC Highlight(娴欏ぇ+铓傝殎,鍗曟簮,watch); harness0(seekcontext, 07-13, P2)
- **寰呰ˉ**: 缇庡洟瑙呮父/楦胯挋ArkAF 鏈棩閬楁紡; ICLR 2026 璁烘枃鍒楄〃閲嶇偣鐩戞帶
- **Details**: See `memory/2026-07-15-tech.md`


### Latest Monitoring Record (2026-07-20, 09:46 run)
- **Monitoring Coverage**: 2026-07-19->20; **0 P0, 0 P1** found (dry spell >16 days)
- **P0**: 0; **P1(impact>8.5)**: 0
- **WAIC 2026** (7/17-20) ongoing, theme Token Cost-Efficiency Era (industry trend)
- **P1-candidate(to verify)**: TencentDB Agent Memory (9k stars, vector DB 4-layer memory arch, complements local Markdown)
- **P2**: G-Memory (GitHub bingreeky/GMemory, hierarchical multi-agent memory)
- **Tracked P0**: headroom(stable), DECS/AbstractCoT(no new refs)
- **Details**: See memory/2026-07-20-tech.md

### Latest Monitoring Record (2026-07-10, 11:50 run)
- **Monitoring Coverage**: 2026-07-09 to 2026-07-10; **0 P0, 2 P1 found**
- **P0**: 0 found; **P1 (impact>8.5)**: 鑵捐浜?Agent Bucket (8.2/10, 鐢熸€佸奖鍝?.7, 宸插湪QClaw閮ㄧ讲)
- **P1 (boundary)**: NVIDIA NeMoClaw Deep Agents (7.8/10, OpenShell娌欑+瀹夊叏杩愯鏃跺弬鑰冩爤)
- **Tracked P0 items status**: headroom (stable); ECC (stable); RYO (stable); DECS/AbstractCoT (no new 24h)
- **Trend**: End-side Agent sub-direction + Agent-native storage (Agent Bucket)
- **Details**: See `memory/2026-07-10.md`
- **Evaluation**: P0 hit on 07-07(RYO, ends 9-day spell), 07-09 dry again, 07-10 has 2 P1s (no P0)

### File Paths Verification (2026-07-06)
- 鉁?`skills/csts-skill-generator/scripts/`, `CSTS-implementation-design.md`, `CSTS-implementation-completion-20260618.md`, `QClaw-杩涘寲浼樺寲钃濆浘-20260609.md` (all exist)
- 鉁?`memory/` + `memory/strategy-changes.md`, `memory/patterns.md`, `memory/performance-baseline.md`, `memory/2026-07-06-tech.md` (all exist)
- 鉁?`D:\QClawX\data\distill-output\distill-report-2026-06-23.md`, `dream-memory-consolidation_20260623.md`, `scripts/memory-archive.ps1` (all exist)

---

## 馃敡 Improvement Strategies (Stable Facts)

### Implemented (2/5)
1. 鉁?**鎶€鑳藉姞杞戒笁姝ユ鏌ユ硶** (2026-06-29) - Written to AGENTS.md Rule 7
2. 鉁?**sessions_spawn鏍囧噯鍙傛暟妯℃澘** (2026-06-29) - Written to TOOLS.md (confirmed 2026-07-06)

### Pending Implementation (3/5)
3. 鈴?**API璋冪敤閲嶈瘯灏佽** - Estimated before 2026-07-13
4. 鈴?**蹇冭烦鏃堕棿绐楀彛绮剧‘鍒ゆ柇** (2026-07-06) - HEARTBEAT.md pending
5. 鈴?**姣忔棩鏁版嵁璁板綍鑷姩鍖?* (2026-07-06) - Establish daily recording mechanism

### New Patterns Discovered (2026-07-06)
- Pattern 4: 蹇冭烦鏃堕棿绐楀彛璇Е鍙?(heartbeat triggered outside window)
- Pattern 5: memory鏂囦欢缂轰箯姣忔棩璁板綍 (no daily data collection)

### Tracking Metrics
- 鎶€鑳藉姞杞藉け璐ョ巼: ~40% 鈫?target <5% (no quantitative data, tracking pending)
- 瀛愪换鍔″畬鎴愮巼: ~70% 鈫?target >95% (no quantitative data, tracking pending)
- 澶栭儴API鎴愬姛鐜? ~60% 鈫?target >90% (no quantitative data, tracking pending)
- **Action**: Establish daily recording mechanism to collect baseline data

---

## 馃搳 Recent Tech Breakthroughs (2026-06-17 to 2026-06-29)

### 2026-06-27 (Tech Breakthrough Monitor)
- 鉁?Monitoring executed (11:50), found 0 P0/P1 breakthroughs
- 馃搳 GitHub: Goose Agent migrated to AAIF (Linux Foundation)
- 馃搳 arXiv: 3 papers (Multi-Agent routing, RL without ground-truth, Hallucination)
- 馃摑 Decision: No push notification (conditions not met)

### 2026-06-29 (Tech Breakthrough Monitor)
- 鉁?Monitoring executed (11:50), found 0 P0/P1/P2 breakthroughs
- 馃搳 Multi-source verification: arXiv/GitHub/tech blogs all negative
- 馃摑 Decision: Silent update (no notification needed)
- 馃攧 Next: Expand search window to 48h if no breakthroughs for 3+ days

### 2026-06-23 (Distill Workflow Discovery)
- **Execution**: 10:15 (Monday), identified 5 workflow patterns from 58 skills
- **High-Priority Pattern**: 1688 procurement workflow (confidence 0.95, 18 related skills)
- **Suggested Skills**: 1688-procurement-workflow, document-pipeline, competitor-monitor-workflow
- **Limitation**: Access鍙楅檺, based on skill clustering vs full tool invocation history
- **Report**: Saved to `D:\QClawX\data\distill-output\distill-report-2026-06-23.md`

### 2026-06-27 (Tech Breakthrough Monitor Results)
- **Monitoring Execution**: 11:50 (Saturday), found 0 P0/P1 breakthroughs
- **P0 Breakthroughs**: 0 found (no push notification sent)
- **P1 Breakthroughs**: 0 found (no major impact breakthroughs)
- **arXiv Papers**: 3 new papers found (need further evaluation)
  - arXiv:2606.27288 - Multi-Agent combination theory
  - arXiv:2606.27369 - RL without ground-truth for LLMs
  - arXiv:2606.27326 - Hallucination in world models
- **GitHub Updates**: Goose Agent migrated to AAIF (Agentic AI Foundation)
- **Decision**: No push notification (conditions not met)

### 2026-06-20
- **P1**: 缇庡洟瑙呮父Agent绀惧尯鏀寔OpenClaw (8.2/10) - 3000+ agents, 40000+ skills, one curl to register, impact score 7.5/10
- **P0**: Ponytail - AI coding绮剧畝绁炲櫒 (9.4/10) - 80-94% code reduction, `clawhub install ponytail`
- **P1**: Trinity - AI Agent涓€閿儴缃?(7.8/10) - Docker containerized, one command deploy

### 2026-06-17
- **P1**: 缇庡洟瑙呮父Agent绀惧尯鍏祴 - OpenClaw/Codex/Claude Code鏃犱唬鐮佸叧鑱?- **P1**: Goose Agent (Twitter鍒涘浜哄洟闃? - 寮€婧愬彲鎵╁睍AI Agent妗嗘灦, 49.5k stars
- **P1**: 楦胯挋ArkAF绔晶鏅鸿兘浣撴鏋?- 绔晶Agent, 棣栨壒50+鏅鸿兘浣撳嵆灏嗕笂绾?
### 2026-06-18
- **P0**: CSTS Enhanced - 4 components 100% done, pipeline test passed
- **P0**: SkillSpector simplified - 20 vulnerability patterns, risk score 100/100
- **P0**: EGSS simplified - entropy calculation, uncertainty-aware scoring

---

## 馃摑 Memory Consolidation Report (2026-06-23)

### Merged Duplicates (0 items)
- No duplicates found since last consolidation (2026-06-22)

### New Information Merged (2 items)
1. 鉁?Added 2026-06-22 tech breakthrough monitoring results to "Recent Tech Breakthroughs" section
2. 鉁?Added 2026-06-23 Distill workflow discovery results (5 patterns, 3 suggested skills)

### Compressed Entries
- **Before**: ~150 lines (after 2026-06-22 consolidation)
- **After**: ~155 lines (added new monitoring results)
- **Compression Rate**: Maintained 鈮? lines per entry

### Promoted Stable Facts
- No new stable facts to promote (all core config already in top section)

### Statistics
- **Merged**: 0 duplicate items
- **New Info Merged**: 2 items (tech breakthrough monitoring + Distill workflow discovery)
- **Compressed**: Maintained compression (all entries 鈮? lines)
- **Verified Paths**: 7/7 exist (added distill report + dream consolidation artifact)

### Next Consolidation
- **Scheduled**: 2026-07-06 (7 days from 2026-06-29)
- **Note**: performance-baseline.md established, quantitative data collection started

---

## 馃梻锔?Historical Records (Compressed)

### 2026-06-23 - AI System Automatic Evolution Task
- 鉁?System evolution task executed (10:11)
- 馃搳 System status: Token consumption -95%, error rate <1%
- 馃搳 Tech breakthroughs found: 0 P0, 3 P1 (HermesAgent, Agent SkillCenter, Context Engineering)
- 馃摑 Artifacts: `system_evolution_report_2026-06-23.md`
- 馃攧 Next action: Manual review needed for P1 breakthroughs

### 2026-06-22 - Tech Breakthrough Monitoring & Memory Consolidation
- 鉁?Memory consolidation executed (09:56)
- 鉁?Tech breakthrough monitor executed (11:50)
- 馃搳 Monitoring results: 0 P0, 3 P1 (impact鈮?.5/10), 4 arXiv papers
- 馃摑 Artifacts: `dream-consolidation-report-20260622.md`, `2026-06-22.md`

### 2026-06-16 - QClaw Data Migration & 鏅鸿兘鍏ㄦ櫙绠＄悊
- 鉁?Migrated from C: to D:\QClawX (724+81,263 files)
- 鉁?鏅鸿兘鍏ㄦ櫙绠＄悊 executed (Step1-3,7 done, Step4 partial fail due to PGlite)
- 鈴?Pending: User manually create symbolic links (admin required)

### 2026-06-09 - 杩涘寲浼樺寲浣撶郴寤鸿
- 鉁?Installed context-budgeting + adaptive-reasoning skills
- 鉁?Created QClaw鑷繘鍖栨瘡鍛ㄨ繍琛?cron (Mon 12:00)
- 鉁?Added Rule 5 to AGENTS.md (Token budget + reasoning optimization)
- 馃幆 Target: 90-95% token savings, 鈮? manual intervention/week

### 2026-06-03 - ECC娣峰悎鍘嬬缉鍣ㄥ紑鍙?- 鉁?Designed & implemented ecc_compressor.py (433 lines, 45-46% compression)
- 鈿狅笍 Bug fixed: LightThinker++ negative compression, GenericAgent low compression
- 馃摑 Files: ecc-token-optimization-design.md, ecc_compressor.py, completion report

### 2026-05-29 to 2026-06-02 - Weekly Error Checks
- 鈿狅笍 Violations ~14,000 (mainly node_modules, dependency files)
- 鉁?Core files (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md) exist
- 馃挕 Suggestion: Add node_modules to .gitignore

---

## 馃摎 Knowledge Base Index (Stable References)

### AI Tech Breakthroughs
- **Token Optimization**: headroom (60-95%), Ponytail (80-94%), EGSS (38-42%)
- **Agent Frameworks**: CSTS (collective skill tree), SkillSpector (security), Trinity (deployment)
- **Community**: 缇庡洟瑙呮父 (3000+ agents, OpenClaw supported)

### Key Technologies
- **ECC Compressor**: 45-46% compression (2026-06-03)
- **CSTS Enhanced**: 4 components, pipeline passed (2026-06-18)
- **Adaptive Reasoning**: Installed skill (2026-06-09)

### Key Decisions
- **2026-06-09**: Tech breakthrough priority (P0/P1/P2) with 51-indicator evaluation
- **2026-06-16**: Data migration from C: to D: (Rule 6 compliance)
- **2026-06-20**: Ponytail integration priority (P0, 9.4/10)
- **2026-06-22**: Lowered 缇庡洟瑙呮父 priority from P0 to P1 (impact 7.5/10 < 8.5/10)

---

*Last Consolidation: 2026-07-20 09:47 (Memory Dreaming Promotion)*  
*Next Consolidation: 2026-07-27 (weekly dream consolidation)*  
*Cron Task: dream-memory-promotion (daily 11:10)*  
*Note: 12 cron tasks active; Added 07-20 monitoring (WAIC 2026), TencentDB Agent Memory P1-candidate, G-Memory P2. Dry spell >16 days. Cleaned stale 07-07 block. All entries 鈮? lines.*

## 馃摑 Memory Consolidation Report (2026-07-06)

### Merged / Removed Duplicates (2)
1. Removed raw "Promoted From Short-Term Memory" block (12 lines) 鈥?redundant with structured "Improvement Strategies" (top + heartbeat precision already recorded).
2. Removed verbose 2026-06-22 monitoring detail in "Recent Tech Breakthroughs" 鈥?duplicated by compressed "Historical Records" 2026-06-22 entry.

### Compression
- Before: 263 lines 鈫?After: 247 lines (removed 16 redundant lines: 12 raw block + 4 verbose monitoring detail).
- All entries maintained 鈮? lines per entry.

### Path Verification (2026-07-06)
- Verified 12 referenced paths: 12/12 exist (no `[path not found]`).
- Newly confirmed: `memory/strategy-changes.md`, `memory/patterns.md`, `scripts/memory-archive.ps1`, `memory/performance-baseline.md`, `memory/2026-07-06-tech.md`.

### Promoted Stable Facts
- None new (Patterns 4&5 + sessions_spawn template already in "Improvement Strategies" top section).
- Tracked: P0/P1 tech breakthrough dry spell ~9 days; next catalyst ICLR 2026 (mid-July).

### Statistics
- Merged/removed duplicates: 2 | Compressed lines: ~11 | Verified paths: 12/12 | Promoted facts: 0