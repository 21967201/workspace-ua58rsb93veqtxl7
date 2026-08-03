# 轨迹评估体系设计 (Trajectory Evaluation — Harness 支柱4)

> **定位**: Harness Engineering 支柱4「全轨迹评估体系」的落地设计。
> **目标**: 为 distill-agent 及所有 cron 任务增加步骤级质量指标，实现"可观测性/反馈"闭环。

---

## 一、评估维度

### 1.1 推理层 (Plan 质量)
| 指标 | 定义 | 评分 |
|------|------|------|
| 计划完整性 | PLAN.md 是否覆盖所有任务阶段 | 0-10 |
| 计划可行性 | 计划步骤是否可执行 | 0-10 |
| 风险识别 | 是否识别潜在风险 | 0-10 |

### 1.2 行动层 (Execute 质量)
| 指标 | 定义 | 评分 |
|------|------|------|
| 计划依从性 | 实际执行是否遵循 PLAN.md | 0-10 |
| 工具选择准确性 | 使用的工具是否匹配任务 | 0-10 |
| 参数正确性 | 工具参数是否正确 | 0-10 |
| 步骤效率 | 是否用最少步骤完成任务 | 0-10 |

### 1.3 端到端 (结果质量)
| 指标 | 定义 | 评分 |
|------|------|------|
| 输出完整性 | 输出是否包含所有预期部分 | 0-10 |
| 错误处理 | 遇到错误时是否正确处理 | 0-10 |
| 时间效率 | 任务耗时是否合理 | 0-10 |

---

## 二、评分算法

```
综合评分 = 0.3 × 推理层 + 0.4 × 行动层 + 0.3 × 端到端

等级:
  ≥8.5  优秀 (A)
  ≥7.0  良好 (B)
  ≥5.0  及格 (C)
  <5.0  不合格 (D) → 触发改进机制
```

---

## 三、落地实现

### 3.1 新增文件
- `scripts/trajectory_eval.py` — 独立评估脚本
- `memory/trajectory/` — 评估记录存储目录
- `memory/trajectory/YYYY-MM-DD-<task>.json` — 单次评估记录

### 3.2 distill-agent 集成
在 distill-agent 的 SKILL.md 输出格式中增加:

```json
{
  "trajectory_quality": {
    "plan_score": 0-10,
    "execution_score": 0-10,
    "result_score": 0-10,
    "overall": 0-10,
    "grade": "A|B|C|D"
  }
}
```

### 3.3 cron 任务集成
每个 cron 任务执行后，自动调用:
```bash
python scripts/trajectory_eval.py --task <task-name> --report <report-file>
```

---

## 四、反馈闭环

```
评估结果 (D级) → 记录到 memory/trajectory/
    ↓
分析失败模式 → 写入 self-improving/corrections.md
    ↓
更新 AGENTS.md/TOOLS.md 规则 → 防止再次发生
    ↓
验证 (下次任务) → 确认改进生效
```

---

## 五、与现有机制关系

| 机制 | 频率 | 评估内容 |
|------|------|---------|
| action_gate.py | 每次执行前 | 命令/路径/情感风险 |
| trajectory_eval.py | 每次任务后 | 计划/执行/结果质量 |
| distill-agent | 每30天 | 工作流模式发现 |
| dream-memory | 每7天 | 记忆整理压缩 |

---

*创建: 2026-07-30 (Harness Phase 2)*
*状态: 设计完成，待实现 trajectory_eval.py*
