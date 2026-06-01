# MEMORY.md - 长期记忆

## 情景记忆

[2026-05-30 09:42] 每周错误预防检查 - 5/106 合规，101 项违规

### 检查详情
- 合规文件: 5个 (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md)
- 违规文件: 101个
- 主要违规类型: 不允许的文件类型 (.git目录下的样本文件、Git对象文件、数据库文件、.pyc字节码文件等)
- 检查时间: 2026-05-30 09:42:06
- 问题分析: 违规数从67激增至101，.git目录未排除导致大量误报
- 状态: 已记录，急需优化pre_check.py扫描规则

[2026-05-29 11:15] **today-task技能配置问题修复** ✅

### 问题现象
用户提供的3个配置命令完全正确，但today-task技能无法读取`authCode`配置。

### 真正的问题根源
**用户的命令完全正确！** 问题出在`today-task`技能的代码中。

`D:\QClawX\data\workspace\skills\today-task\scripts\config.py`的`_get_from_openclaw_global()`方法有**逻辑BUG**：
1. 代码先正确读取了`C:\Users\Administrator\.qclaw\openclaw.json`（QClaw配置）
2. **但第108-117行错误地覆盖了读取结果**，导致即使配置正确也会失败

### 修复方法
删除`config.py`第103-117行的错误覆盖逻辑，让代码只读取一次配置。

### 正确配置命令（QClaw环境）
```bash
# 1. 安装today-task技能
npx clawhub@latest install today-task --force --registry=https://mirror-cn.clawhub.com

# 2. 配置authCode（会写入C:\Users\Administrator\.qclaw\openclaw.json）
openclaw config set skills.entries.today-task.config.authCode dtG4JOCLM3ev

# 3. 重启Gateway（可选，配置可能立即生效）
openclaw gateway restart
```

**注意**：QClaw基于OpenClaw，所以配置命令仍然用`openclaw config set`，但配置文件在`.qclaw\openclaw.json`。

### 教训
1. **用户的命令可能是对的** - 不要总怀疑用户，要检查代码
2. **读代码而不是猜问题** - 问题在代码里，不是在网上
3. **跳过无关问题** - 用户让跳过`gateway restart`，我偏要死磕
4. **立即记录** - 修复后马上写总结和更新记忆

---

[2026-05-29 12:01] 每周错误预防检查 - 5/72 合规，67 项违规

### 检查详情
- 合规文件: 5个 (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md)
- 违规文件: 67个
- 主要违规类型: 不允许的文件类型 (.git目录下的样本文件、Git对象文件、数据库文件、.pyc字节码文件等)
- 检查时间: 2026-05-29 12:01:19
- 问题分析: 工作区包含大量.git内部文件和缓存文件，需要优化检查规则
- 状态: 已记录，待优化pre_check.py扫描规则

[2026-05-28] 每周错误预防检查 - 5/25 合规，20 项违规

### 检查详情
- 合规文件: 5个 (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md)
- 违规文件: 20个
- 主要违规类型: 不允许的文件类型 (.git目录下的样本文件、.pyc文件、.sqlite3文件等)
- 检查时间: 2026-05-28 09:42:21

## 错误模式库

### 常见错误模式

#### 1. 文件类型违规（.git目录文件）
- **描述**: 工作区包含.git目录下的内部文件，被误判为违规
- **常见文件**: COMMIT_EDITMSG, config, description, HEAD, index, hooks样本文件, Git对象文件（hash值文件名）
- **出现次数**: 4次（2026-05-28: 20个，2026-05-29: 67个，2026-05-30: 101个）
- **解决方案**: 修改pre_check.py，完全排除.git目录的检查
- **出现频率**: 极高
- **状态**: 紧急 - 违规数持续增长（20→67→101），必须立即修复

#### 2. 文件类型违规（缓存和数据库文件）
- **描述**: 工作区包含Python字节码、数据库文件等临时文件
- **常见文件**: .pyc文件、.sqlite3文件、.jsonl文件
- **出现次数**: 2次（2026-05-28: 少量，2026-05-29: chroma.sqlite3, events.jsonl, pre_check.cpython-311.pyc）
- **解决方案**: 更新.gitignore文件，排除*.pyc, *.sqlite3, *.jsonl等
- **出现频率**: 高

#### 3. 编码问题
- **描述**: Python脚本输出中文乱码
- **常见场景**: Windows控制台编码问题
- **解决方案**: 使用UTF-8编码，避免特殊字符，或使用日志记录替代控制台输出
- **出现频率**: 中

#### 4. 代码BUG导致配置读取失败
- **描述**: today-task技能的`config.py`代码有逻辑BUG，正确读取配置后又被覆盖
- **常见场景**: 技能代码质量参差不齐，需要仔细检查
- **解决方案**: 仔细阅读代码，找出逻辑错误并修复
- **出现频率**: 中
- **出现日期**: 2026-05-29

#### 5. Cron任务delivery配置错误（高频！）
- **描述**: 所有Cron任务的delivery配置错误，`mode=none`时却设置了`channel`和`to`
- **常见场景**: 创建任务时复制粘贴错误配置模板
- **错误信息**: "Channel is required when multiple channels are configured: openclaw-weixin, wechat-access"
- **解决方案**: 
  - 需要推送：设`mode=announce, channel=wechat-access, to=last`
  - 不需要推送：设`mode=none`（删除channel和to）
- **出现频率**: 极高（16/16任务全部错误）
- **出现日期**: 2026-05-29
- **正确配置模板**:
  ```json
  // 方案A：需要推送（推荐）
  "delivery": {
    "mode": "announce",
    "channel": "wechat-access",
    "to": "last",
    "bestEffort": false
  }
  
  // 方案B：不需要推送
  "delivery": {
    "mode": "none"
  }
  ```

## 改进建议

### 优先解决的3个高频错误（2026-05-30更新）

1. **排除.git目录检查** (优先级: 极高 - 紧急)
   - 问题: pre_check.py未排除.git目录，导致大量Git内部文件被误判为违规（占比约95%）
   - 数据: 违规数持续增长（20→67→101），本周激增405%
   - 建议: 在pre_check.py的扫描逻辑中添加.git目录排除规则
   - 预期效果: 违规项数从101降至约5项，检查准确性大幅提升
   - 状态: 必须立即处理 - 已连续4次出现且持续恶化

2. **优化文件类型白名单** (优先级: 高)
   - 问题: 缓存文件（.pyc, .sqlite3, .jsonl）被判定为违规
   - 建议: 在pre_check.py中添加缓存文件类型排除规则，或创建明确的允许文件类型白名单
   - 预期效果: 减少误报，聚焦真正的问题文件
   - 状态: 待处理

3. **修复输出编码问题** (优先级: 中)
   - 问题: Python脚本在Windows下输出中文乱码，影响结果可读性
   - 建议: 设置环境变量PYTHONIOENCODING=utf-8，或将结果输出到日志文件而非控制台
   - 预期效果: 提高结果可读性和问题排查效率
   - 状态: 待处理

## 项目上下文

- 工作区: D:\QClawX\data\workspace-ua58rsb93veqtxl7
- 创建时间: 2026-05-27
- 用途: OpenClaw AI助手工作区

## 重要决策记录

- 2026-05-28: 创建每周错误预防检查机制
- 2026-05-28: 建立MEMORY.md作为长期记忆存储
- 2026-05-29: 修复today-task技能`config.py`的BUG，正确配置命令记录到MEMORY.md

[**2026-05-30 10:37] 每周错误预防检查 - 5/106 合规，101 项违规**
- 合规文件: 5个
- 违规文件: 101个
- 违规项数: 101项
- 主要违规类型: 不允许的文件类型: COMMIT_EDITMSG, 不允许的文件类型: config, 不允许的文件类型: description, 不允许的文件类型: HEAD, 不允许的文件类型: index...

## AI Technology Developments (2026-06-01 更新)

### 2026年6月 AI 大模型技术突破

#### 1. 多模态原生融合成为主流
- 模型从"语言模型"转向"原生多模态"（GPT-4o、Sora2、Meta Muse Spark）
- 实现"感知-推理-行动"的端到端统一
- 多模态模型能力一年提升超过50%
- 产业创新重心从语言模型向多模态迁移

#### 2. 数据墙挑战与解决方案
- 互联网公域数据已消耗殆尽，预训练撞上"数据墙"
- 三条解决路径：
  1. 从公域走向私域，针对特定行业和场景的私域数据深度开发
  2. 发展合成数据，通过传统算法及AI算法生成合成数据
  3. 提升数据质量，以先进的数据工程手段优化已有数据品质

#### 3. 算力架构革新
- 英伟达将推出Arm架构芯片N1和N1X，专为AIPC设计
- N1X采用台积电3nm工艺，集成20核CPU + Blackwell架构GPU
- 提供约200TOPS端侧AI算力，支持128GB统一内存
- 推理算力占比快速提升，未来将超过训练算力
- 端侧智能普及，AI交互延迟从300ms降至20ms以内

#### 4. 模型性能提升
- OpenAI GPT-5.6预计6月发布，上下文窗口达150万tokens（提升43%）
- 垂直大模型崛起（代码、生物医疗、工业等）
- 小模型（10亿-100亿参数）通过剪枝、量化、知识蒸馏等优化达到高效能

#### 5. 技术范式重构
- 从"规模崇拜"到"效率优先"
- 焦点转向"够用、好用、专用"
- 垂直大模型成为2026年的显著特征

---

### 2026年6月 AI Agent 技术突破

#### 1. 多模态感知全面升级
- AI Agent不再局限于文本理解
- 以GPT-6、Claude Opus 4.7、DeepSeek V4为代表的新一代大模型
- 实现文本、图像、音频、视频、代码的原生多模态理解与生成
- **视觉推理链**(Visual Chain-of-Thought)：Agent像人类一样逐步推理

#### 2. 自主规划与决策能力跃迁
- 从"听话的执行者"到"自主的思考者"
- 基于目标、环境状态和内部知识库，动态生成并优化行动计划
- 引入强化学习和博弈论思想，在不确定性下做出鲁棒性决策

#### 3. 交互范式重构
- 手机交互从"唤醒"走向"陪伴"
- 多模态Agent让设备不再只是被动响应工具
- 2026年6月26-27日，AICon全球人工智能开发与应用大会将在上海举办

#### 4. A2A协议与MCP协同架构
- 通过A2A(Agent-to-Agent)协议与MCP(多智能体协作协议)
- 实现跨部门、跨系统的业务流程自动化
- 群体智能协同架构日益成熟

#### 5. AI Agent规模化商用
- AI智能体从被动响应升级为自主决策执行者
- 具备数周级持续任务处理能力
- 据Gartner预测，2026年底超过70%企业AI应用将采用多智能体架构

---

#### 信息来源
- 搜索时间: 2026-06-01
- 搜索关键词: 
  1. \2026年6月 AI 大模型 技术突破 最新进展\
  2. \2026年6月 AI Agent 技术突破 自主规划 多模态\
- 信息来源: 今日头条、腾讯网、CSDN博客、搜狐等
- 更新频率: 每周一更新



## QClaw Native Knowledge Base (2026-06-01 创建)

### 三层知识架构

#### Layer 1: Memory System (日常知识)
- **核心文件**: MEMORY.md (本文件)
- **每日日志**: memory/YYYY-MM-DD.md`n- **分类存储**: memory/people/*.md, memory/projects/*.md, memory/tech/*.md, memory/decisions/*.md`n- **搜索工具**: memory_search, memory_get`n
#### Layer 2: LCM (对话历史)
- **自动捕获**: 重要对话自动压缩存储
- **搜索工具**: lcm_grep, lcm_expand, lcm_describe`n
#### Layer 3: Custom KB (结构化知识)
- **目录**: kb/`n- **分类**: kb/people/*.md, kb/projects/*.md, kb/tech/*.md, kb/ai-breakthrough/*.md, kb/decisions/*.md`n- **搜索**: memory_search --corpus="all"

### 知识流转

**每日流程**:
``n用户对话 → memory/YYYY-MM-DD.md → memory/people/*.md → memory/projects/*.md
``n
**每周整理** (周一):
``nmemory/*.md → 提取重要知识 → kb/*.md → 更新 MEMORY.md
``n
**搜索流程**:
``n用户提问 → Layer 1 (memory_search) → Layer 2 (lcm_grep) → Layer 3 (memory_search --corpus="all") → 综合回答
``n
### 快速访问

| 命令 | 用途 |
|------|------|
| memory_search --query="关键词" | 搜索 Layer 1 + 3 |
| memory_search --query="关键词" --corpus="all" | 跨库搜索 |
| lcm_grep --pattern="关键词" | 搜索 Layer 2 |
| ead --path="kb/tech/xxx.md" | 读取KB文件 |

### 目录结构

``nD:\QClawX\data\workspace-ua58rsb93veqtxl7\
├── MEMORY.md                    # 核心记忆索引
├── memory\                     # Layer 1: 日常记忆
│   ├── YYYY-MM-DD.md          # 每日日志
│   ├── people\                # 人物知识库
│   ├── projects\              # 项目知识库
│   ├── tech\                  # 技术知识库
│   └── decisions\            # 决策记录
├── kb\                        # Layer 3: 结构化知识库
│   ├── people\                # 人物档案
│   ├── projects\              # 项目文档
│   ├── tech\                  # 技术文档
│   ├── ai-breakthrough\      # AI技术突破
│   └── decisions\            # 重要决策
└── lcm\                       # Layer 2: LCM管理(自动)
``n
#### 信息来源
- 创建时间: 2026-06-01
- 方案类型: 混合方案 (Hybrid Solution)
- 更新频率: 每周一

