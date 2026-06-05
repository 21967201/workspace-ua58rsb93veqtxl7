# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 📋 自动任务时间限制规则 (2026-06-05)

**规则内容**: 所有自动任务时间必须在周一至周六,10:30-18:10之前。

### 规则详情
1. **时间范围**: 周一至周六（工作日+周六）
2. **时间限制**: 必须在10:30-18:10之前执行
3. **禁止时间**: 禁止在周日执行，禁止在18:10之后执行
4. **禁止时间**: 禁止在10:30之前执行（早晨太早）

### 执行标准
1. 所有Cron任务必须设置在周一至周六
2. 所有Cron任务必须在10:30-18:10之前执行
3. 检查现有任务，不符合的必须立即修改
4. 创建新任务时，必须遵循此时间限制

### 底层规则说明
- 这是底层规则，所有任务调度都必须遵循
- 在创建或修改Cron任务时，必须检查是否符合此规则
- 如果任务时间不符合，必须立即修改

### 修改后的任务时间（2026-06-05 15:10）
| 任务名称 | 修改前时间 | 修改后时间 | 是否符合 |
|----------|------------|------------|----------|
| 自动同步任务文件到GitHub | 每天18:00 | 周一至周六17:50 | ✅ 符合 |
| 季度评审任务 | 每天09:00 | 周一至周六10:30 | ✅ 符合 |
| 月度报告任务 | 每天09:00 | 周一至周六10:40 | ✅ 符合 |
| 每日监控任务 | 每天09:00 | 周一至周六10:50 | ✅ 符合 |
| 每周检查任务 | 每周一09:00 | 每周一11:10 | ✅ 符合 |

### 验证结果
- ✅ 所有17个任务的执行时间都符合"周一至周六,10:30-18:10之前"的要求
- ✅ 所有任务delivery配置正确（mode="announce", channel="wechat-access", to="last"）
- ✅ 所有任务均为全自动执行，无需人工确认

---

*规则添加时间: 2026-06-05 15:10*  
*规则添加原因: 用户要求将自动任务时间限制加入第一优先原则、记忆和底层规则*  
*规则执行标准: 所有Cron任务必须遵循此时间限制*  

---
