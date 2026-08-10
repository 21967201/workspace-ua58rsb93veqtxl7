# 修复：数据分层与记忆索引维护 cron 任务（2026-08-07）

## 问题
- 原 jobId `5c3f3b98...`，连续 3 次 error。
- 根因：`payload.model = qclaw/pool-deepseek-v4-flash` 不在 allowlist `[qclaw/pool-hy3-preview]`，cron preflight 直接拒绝，脚本从未执行。
- 错误原文："cron payload.model 'qclaw/pool-deepseek-v4-flash' rejected by agents.defaults.models allowlist"

## 修复
- 经验佐证（MEMORY.md）：`cron.update` 对 model/delivery 的部分 patch 会被忽略，必须删除重建。
- 删除原 job，新建 jobId `df1ee225-2c46-4685-8cc5-d719ea18c168`。
- payload.model → `qclaw/pool-hy3-preview`；delivery 恢复 `announce → wechat-access / to=last`。
- schedule 不变：`0 15 * * 1,2,3,4,5,6`（周一至周六 15:00）。

## 验证（手动补跑）
- runId `manual:df1ee225...:1786085469648:2`
- status=ok，durationMs=67824，model=pool-hy3-preview（未被拒），delivered=true。
- 摘要输出：
  - 分层归档：温层移动 1 个文件，冷层压缩 0 个，释放约 0 KB（仅移动未压缩）。
  - 语义索引增量：新增 0 块、更新 3 块（文档 138 / 块 2088）。

## 结论
修复有效，下次定时 15:00 正常执行。模型名需与当前 allowlist 一致，否则 preflight 拒绝且不跑脚本。
