# OpenClaw违规检查结果

**执行时间**: 2026-05-29 11:36 (Asia/Shanghai)

## 检查范围
- 扫描目录: `D:\QClawX\data\workspace\skills` (含子目录)
- 检测关键字: `.openclaw`、`openclaw.json`、`openclaw config`

## 发现违规
在 `today-task` 技能中发现多处违规引用：
- README.md: 7处
- SECURITY.md: 1处  
- SKILL.md: 12处

## 修复操作
已执行批量替换：
- `OpenClaw` → `QClaw`
- `openclaw.json` → `qclaw.json`
- `.openclaw` → `.qclaw`
- `openclaw config` → `qclaw config`
- `openclaw` → `qclaw`

## 验证结果
重新扫描确认无遗漏，所有违规引用已修复。

## 推送状态
华为负一屏推送失败 (authCode: dtG4JOCLM3ev)
- 尝试端点: `push.huweiss.com`、`api.huweiss.com`
- 错误: 无法解析远程名称
- 建议: 检查推送服务URL是否正确

## 结论
✅ 违规检查完成，所有 OpenClaw 引用已成功替换为 QClaw
❌ 推送通知失败，需核实华为推送服务配置
