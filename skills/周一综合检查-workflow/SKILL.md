# 周一综合检查 工作流

## 概述
自动化执行「周一综合检查」：合并运行**季度评审**与 **OpenClaw 违规/合规检查**，生成综合报告并推送至负一屏。

**模式来源（Distill 2026-07-20 月检实证）：**
- 历史 session 复扫出现 **3 次**（2026-07-06 / 2026-07-13 / 2026-07-20），标题 `综合检查` / `综合周检查` / `周一综合检查`
- 置信度：0.75（步骤清晰、通用；由每周一 cron 11:50 触发，但此前无独立 skill 承载，仅散落在各 session 脚本调用中 → 本轮固化为可复用工作流）
- 自动发现时间：2026-07-20

## 适用场景
- 每周一（cron 约 14:40）自动执行季度评审 + 违规检查合并任务
- 需要"评审 + 合规"二合一产出周报并推送到负一屏
- 季度评审脚本本身按季度生效（其他周仅产出"无评审/无违规"的轻量合并报告）

## 工作流步骤

### 1. 季度评审（auto_quarterly_review.py）
- 运行 `auto_quarterly_review.py` 生成季度报告与技术路线图
- 脚本位置：`D:\QClawX\data\workspace-ua58rsb93veqtxl7\auto_quarterly_review.py`
- 仅在季度首月（1/4/7/10 月）产出完整评审；其余周脚本仍运行但内容为空/轻量
- 产物：`quarterly-review-report-YYYY-MM-DD.md`

### 2. 合规检查（check_cron_compliance.ps1 / check_compliance_simple.ps1）
- 扫描 skills / cron 配置，检查是否违反 AGENTS.md 规则（如 cron 时间段 周一至周六 10:30-18:10、禁止 C 盘存储等）
- 脚本位置：`D:\QClawX\data\workspace-ua58rsb93veqtxl7\check_cron_compliance.ps1`
- 记录违规项（通常 0 违规，仅有排各项），输出合规结论

### 3. 合并报告
- 将季度评审结论 + 合规检查结论合并为一份综合报告
- 文件名惯例：`周一综合检查报告_YYYY-MM-DD.md`
- 报告须包含：季度评审结论（任务完成率、技术进展、商业化短板）、违规检查结果、执行状态

### 4. 创建任务 JSON + 推送负一屏
- 调用 `today-task` skill 的推送链路：准备任务 JSON → `task_push.py --data <jsonFile>`
- 推送返回校验：`HTTP 200` 且 `code: 0000000000` / `"success": true`
- 推送脚本：`D:\QClawX\data\workspace\skills\today-task\scripts\task_push.py`

## 使用示例

```powershell
# 由 Cron 每周一 14:40 触发，全自动，无需人工干预
$root = "D:\QClawX\data\workspace-ua58rsb93veqtxl7"

# 1. 季度评审（季度首月才产出实质内容）
python "$root\auto_quarterly_review.py"

# 2. 合规检查
pwsh -File "$root\check_cron_compliance.ps1"

# 3. 合并报告（由 Agent 汇总两步结论写入 周一综合检查报告_<date>.md）
#    （见工作流步骤 3 模板）

# 4. 推送负一屏
#    构造任务 JSON 后调用：
#    python "D:\QClawX\data\workspace\skills\today-task\scripts\task_push.py" --data $jsonFile
#    校验返回 HTTP 200 / success:true
```

## 注意事项
- 季度评审脚本按季度生效，非季度首月运行时综合报告应明确标注"本季度暂无新评审"
- 合规检查命中项需区分"真实违规"与"排该项"（如 config.py 属历史排除项）
- 推送与本地报告解耦：即便负一屏不可用，报告文件也必须落盘
- 触发时间须符合 AGENTS.md 规则 4（周一至周六 10:30-18:10）

## 相关 Skill
- GitHub同步推送-workflow（报告同步到仓库）
- 负一屏推送-workflow（统一的负一屏推送范式）
- daily-tech-breakthrough-monitor（同属周一自动化检查族）
