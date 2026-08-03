# Action Gate — 确定性行动闸门（Harness System2 层）

> **定位**: Harness Engineering 支柱3「安全反射+行动闸门」的 System2 实现。
> **原理**: 安全反射(SAFETY_REFLEX.md)是推理层注入(System1)，本闸门是执行层确定性拦截(System2)。
> **零依赖**: 纯 Python 标准库，无需 OPA/Rego 外部引擎。
> **集成**: 每个 cron 任务执行前调用 `action_gate.py --check <risk-level>`。

---

## 一、设计原理

```
用户/任务输入
    ↓
[System1 安全反射] — 推理层注入，SAFETY_REFLEX.md 8条规则
    ↓
[System2 行动闸门] — 本文件，确定性规则判定
    ├─ 风险分级 (0-3)
    ├─ 路径白名单
    ├─ 命令黑名单
    └─ 情感状态检查 (PAD)
    ↓
放行 / 拦截 / 人工接管
```

## 二、使用方式

```bash
# 检查单个命令的风险等级
python action_gate.py --check "rm -rf /tmp/x"

# 检查文件写入目标
python action_gate.py --path "C:\Users\Administrator\Desktop\x.txt"

# 检查情感状态 (读取 memory/emotional-state.json)
python action_gate.py --emotion

# 完整闸门检查 (命令+路径+情感)
python action_gate.py --full --command "Remove-Item x" --path "D:\QClawX\data\x"
```

## 三、判定规则

### 3.1 风险分级

| 等级 | 含义 | 处理 |
|------|------|------|
| 0 | 安全 | 直接放行 |
| 1 | 低风险 | 放行 + 日志记录 |
| 2 | 中风险 | 放行 + 显著警告 |
| 3 | 高风险 | **拦截 + 人工确认** |

### 3.2 命令黑名单（命中即等级3）

```
rm -rf, Remove-Item -Recurse, del /s, diskpart, format, 
bootrec, reg delete, sc delete, taskkill /f, shutdown
```

### 3.3 路径规则

- 目标在 `D:\QClawX` 下 → 等级0（放行）
- 目标在 `C:\` 系统关键路径 → 等级3（拦截）
- 目标在 `C:\Users\*\Desktop` 等用户目录 → 等级2（警告）

### 3.4 情感状态联动

读取 `memory/emotional-state.json`：
- 若处于高风险状态 (pleasure < -0.5 且 arousal > 0.5) → 等级+1
- 若连续3次高唤醒 → 建议触发人工接管

---

## 四、输出格式

```json
{
  "verdict": "allow|warn|block",
  "level": 0,
  "reasons": ["path in D:\\QClawX", "emotion stable"],
  "emotion": {"pleasure": 0.1, "arousal": -0.1, "dominance": 0.0}
}
```

---

*创建: 2026-07-30 (Harness Phase 2)*
*关联: SAFETY_REFLEX.md (System1) + emotional-state.json (状态)*
