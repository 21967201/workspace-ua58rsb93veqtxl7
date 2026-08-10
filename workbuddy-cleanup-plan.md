# WorkBuddy 数据目录盘点与清理方案

> 生成时间: 2026-08-08 | 状态: **待用户确认后执行**

## 一、目录全景

| 路径 | 状态 | 最后活动 | 判定 |
|------|------|---------|------|
| `D:\WorkBuddyX\.workbuddy` | ✅ **活跃主数据** | 2026-08-08 15:12 | **保留（正在使用）** |
| `C:\Users\Administrator\.workbuddy` | Junction → 指向 `D:\WorkBuddyX\.workbuddy` | 今天 | **保留（是链接不是副本）** |
| `D:\WorkBuddyX\.workbuddy_backup` | 旧备份 (5/28) | 2026-05-28 | 可删（备份已有） |
| `D:\WorkBuddyX\.migration_backup` | 迁移备份 (7/23) | 2026-07-23 | 可删（迁移完成） |
| `D:\WorkBuddyX\WorkBuddyData` | **旧版 OpenClaw 数据（5/27前）** | 2026-07-25 | ⚠️ 含独立 db，**需确认**后归档 |
| `D:\WorkBuddyX\WorkBuddyExtension` | 扩展 (5/12) | 2026-05-12 | 可删 |
| `D:\WorkBuddyX\workbuddy-skin-studio` | 皮肤 (7/22) | 2026-07-22 | 可删（皮肤工具） |
| `D:\.workbuddy` | **旧过渡数据 (6/9-6/11)** | 2026-06-27 | ⚠️ 含独立 db 10MB，**需确认**后归档 |
| `D:\.workbuddy.backup_20260612_100002` | 空备份目录 | - | 可删（空的） |
| `D:\WorkBuddyData` | 空壳 (6/5) | 2026-06-05 | 可删（只有一个 .workbuddy 空壳） |
| `C:\Users\Administrator\.workbuddy-ai` | **旧 AI 数据 (5/30)** | 2026-05-30 | ⚠️ 含独立 db 0.1MB，需确认 |
| `C:\Users\Administrator\.workbuddy-key-fallback` | key 备份 (7/7) | 2026-07-07 | 保留（key 重要） |
| `C:\Users\Administrator\.workbuddy.bak` | 空备份目录 | - | 可删（空的） |
| `C:\Users\Administrator\WorkBuddy` | **大量时间戳备份** (4-6月) | 2026-06-16 | ⚠️ 备份集合，需确认 |
| `C:\Users\Administrator\WorkBuddy AI` | 空壳 (5/30) | 2026-05-30 | 可删 |
| `D:\Cache\WorkBuddy` | 空缓存 | - | 可删（空的） |
| `D:\Cache\Programs\WorkBuddy` | 只有一个 debug.log | 2026-04-29 | 可删 |
| `D:\d\WorkBuddyX` | 临时输出 | 2026-07-31 | 可删（video_output/tmp） |
| `D:\c\Users\Administrator\.workbuddy` | 只有一个 binaries/ | 2026-06-09 | 可删（残留） |

## 二、活跃数据（必须保留）

- `D:\WorkBuddyX\.workbuddy\` （全部）— 当前主数据，含活跃 workbuddy.db (4.9MB)
- `C:\Users\Administrator\.workbuddy` — Junction，不要动
- `C:\Users\Administrator\.workbuddy-key-fallback\` — connector keys 备份

## 三、建议处理（分两批）

### 批次 A：安全删除（空目录 / 明显废弃 / 已备份）
| 路径 | 理由 |
|------|------|
| `D:\.workbuddy.backup_20260612_100002` | 空目录 |
| `C:\Users\Administrator\.workbuddy.bak` | 空目录 |
| `D:\Cache\WorkBuddy` | 空目录 |
| `D:\WorkBuddyData` | 只有一个空壳 .workbuddy |
| `C:\Users\Administrator\WorkBuddy AI` | 只有一个空壳 Claw |
| `D:\Cache\Programs\WorkBuddy` | 只有 debug.log |
| `D:\c\Users\Administrator\.workbuddy` | 只有残留 binaries |
| `D:\d\WorkBuddyX` | 临时输出 |
| `D:\WorkBuddyX\WorkBuddyExtension` | 5月扩展，已废弃 |
| `D:\WorkBuddyX\.workbuddy_backup` | 5月备份 |

### 批次 B：需要确认（可能含历史数据）
| 路径 | 内容 | 建议 |
|------|------|------|
| `D:\.workbuddy` | 6月过渡数据 + 10MB db | 归档到 `D:\QClawX\data\archive\workbuddy\` 后删除 |
| `D:\WorkBuddyX\WorkBuddyData` | 5月旧 OpenClaw 数据 + 8MB db | 归档后删除 |
| `C:\Users\Administrator\.workbuddy-ai` | 5月旧 AI 数据 + 0.1MB db | 归档后删除 |
| `C:\Users\Administrator\WorkBuddy` | 17个时间戳备份 (4-6月) | 挑最新一个保留，其余归档 |
| `D:\WorkBuddyX\workbuddy-skin-studio` | 皮肤工作室 | 确认不再用则删除 |
| `D:\WorkBuddyX\.migration_backup` | 7/23 迁移备份 | 归档后删除 |

## 四、执行方式

所有删除**先移到回收站**（可恢复），不用永久删除。归档先复制到 `D:\QClawX\data\archive\workbuddy\`。

## 五、待确认问题

1. 批次 A 是否直接执行？
2. 批次 B 是否按建议归档？
3. `C:\Users\Administrator\WorkBuddy` 里的时间戳备份，是否只需要保留最新的 2026-06-16-17-54-03？

> ⚠️ 注意：删除前会先停掉 WorkBuddy 进程（避免文件占用），清理后自动重启。
