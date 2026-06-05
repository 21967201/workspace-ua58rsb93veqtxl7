# QClaw性能优化方案

## 检查结果汇总 (2026-06-04 10:15)

### 🔴 关键问题
1. **Skills数量过多** - 严重超标
   - 管理skills: 61个
   - 个人skills: 63个
   - **总计: 124个skills** ⚠️

2. **Agents数量较多**
   - Agents目录: 23个agents

3. **系统内存不足**
   - CPU: Intel i5-12400F (6核)
   - 可用内存: 仅2.3GB ⚠️
   - 总内存: 未正确获取

### 📊 性能影响分析

**Skills过多的影响:**
- 每个skill加载时消耗内存
- 启动时扫描所有skills，耗时增加
- 运行时匹配skill规则，CPU开销大
- 124个skills严重超标（建议: 20-30个）

**Agents过多的影响:**
- 23个agents可能同时运行
- 每个agent占用独立资源
- 上下文切换开销

**内存不足的影响:**
- 2.3GB可用内存过低
- 系统频繁换页
- Node.js进程内存受限

## 🚀 优化方案

### 立即执行 (高优先级)

#### 1. 清理Skills (预计提升50-70%性能)
```powershell
# 查看skills目录
Get-ChildItem 'D:\QClawX\data\.qclaw\skills' | Select-Object Name, LastWriteTime
Get-ChildItem '~/.qclaw/skills' | Select-Object Name, LastWriteTime

# 备份后删除不常用的skills
# 建议保留核心skills:
# - 1688相关 (5-8个)
# - 腾讯文档相关 (3-5个) 
# - 系统工具 (5-10个)
# - 其他常用 (5-10个)
# 目标: 保留20-30个最常用的
```

#### 2. 清理Agents (预计提升20-30%性能)
```powershell
# 查看agents状态
Get-ChildItem 'D:\QClawX\data\.qclaw\agents' | Select-Object Name, LastWriteTime

# 停用不需要的agents
# 建议保留3-5个核心agents
```

#### 3. 增加系统内存 (根本解决方案)
- **当前**: 可用内存仅2.3GB
- **建议**: 升级到16GB或32GB内存
- **预期**: 性能提升100%+

### 中级优化

#### 4. 优化QClaw配置
编辑 `D:\QClawX\data\.qclaw\openclaw.json`:
```json
{
  "skills": {
    "enabled": true,
    "autoLoad": false,  // 改为手动加载
    "maxLoaded": 20     // 限制加载数量
  },
  "agents": {
    "maxRunning": 3     // 限制同时运行数量
  }
}
```

#### 5. 清理日志和缓存
```powershell
# 清理QClaw日志
Remove-Item 'D:\QClawX\data\.qclaw\logs\*.log' -Recurse -Force -ErrorAction SilentlyContinue

# 清理node_modules缓存
Remove-Item 'D:\QClawX\data\workspace-*\node_modules' -Recurse -Force -ErrorAction SilentlyContinue
```

### 长期优化

#### 6. 定期维护计划
- 每周检查skills/agents数量
- 每月清理未使用的skills
- 监控内存使用情况

#### 7. 搜索官方优化方案
由于网络搜索受限，建议:
1. 查看QClaw官方文档
2. 搜索GitHub issues: "qclaw performance optimization"
3. 查看Discord/社区讨论

## 📋 执行步骤

### 第一步: 备份当前配置
```powershell
Copy-Item 'D:\QClawX\data\.qclaw\openclaw.json' 'D:\QClawX\data\.qclaw\openclaw.json.backup'
```

### 第二步: 清理Skills (分批执行)
1. 列出所有skills及最后使用时间
2. 识别30天内未使用的skills
3. 移动到备份目录(不要直接删除)
4. 重启QClaw测试性能

### 第三步: 清理Agents
1. 检查哪些agents正在运行
2. 停用不需要的agents
3. 保留3-5个核心agents

### 第四步: 监控性能
```powershell
# 重启后监控资源使用
Get-Process | Where-Object {$_.Name -eq 'node'} | Select-Object CPU, WorkingSet, StartTime
```

## 🎯 预期效果

执行优化后预期:
- **启动速度**: 提升50-70%
- **响应速度**: 提升30-50%  
- **内存使用**: 降低40-60%
- **整体流畅度**: 显著改善

## ⚠️ 注意事项

1. **备份优先**: 清理前务必备份
2. **分批执行**: 不要一次性删除所有skills
3. **测试验证**: 每次清理后重启测试
4. **硬件升级**: 内存升级是最根本的解决方案

## 下一步行动

1. ✅ 已完成: 问题诊断
2. ⏳ 待执行: Skills清理 (需要你确认哪些skills可以移除)
3. ⏳ 待执行: Agents清理
4. ⏳ 待执行: 配置优化
5. ⏳ 建议: 内存硬件升级

请告诉我你希望先执行哪一步，或者我可以帮你自动执行skills清理(我会先列出可以安全移除的skills清单)。
