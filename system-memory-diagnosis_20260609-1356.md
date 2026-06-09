# 系统内存诊断与修复报告

**时间**: 2026-06-09 13:56  
**错误**: ❌ 500 `{"error":"memory layout cannot be allocated"}`

---

## 诊断结果

### 根因分析
错误是 **V8/Chrome 引擎内存分配失败** 导致的，直接原因是系统物理内存耗尽（仅剩 2.4GB/16GB）。

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 可用物理内存 | **2.4 GB (15%)** | 5.5 GB (35%) |
| C盘剩余空间 | 9.5 GB | 10.1 GB |
| 冗余进程数 | 41+ | 已清理 |
| Gateway 状态 | 运行中 | 已重启 |

### 内存消耗 TOP 5（修复前）
| 进程 | 内存 | 说明 |
|------|------|------|
| QClaw (Node.js utility) | 1,382 MB | `--max-old-space-size=4096` 堆限制过高 |
| ima.copilot ×31 | ~4,517 MB | 大量冗余实例 |
| WorkBuddy ×10 | ~1,296 MB | 大量冗余实例 |
| QClaw (renderer) | 752 MB | Electron 渲染进程 |
| 浏览器/微信等 | ~1,000 MB | 正常前台应用 |

### 触发原因
当系统内存不足时，QClaw 的 Chromium/Node.js 引擎（配置了 4GB V8 堆上限）尝试分配新内存块，但系统无法满足，触发 V8 的 `memory layout cannot be allocated` 错误。

---

## 已执行修复

### ✅ 修复1: 清理冗余进程（释放 ~5.8GB）
- 杀掉 31 个冗余 `ima.copilot` 进程（释放 ~4.5GB）
- 杀掉 10 个冗余 `WorkBuddy` 进程（释放 ~1.3GB）
- 清理 QClaw 缓存（Cache、Code Cache、Crashpad）

### ✅ 修复2: Gateway 重启
- 向 OpenClaw Gateway (PID 23508) 发送 SIGUSR1 重启信号
- 清除累积的进程内存碎片

### ✅ 修复3: C盘临时文件清理
- 清理 `%TEMP%` 和 `%LOCALAPPDATA%\Temp`
- 清理 QClaw 缓存目录
- C盘从 9.5GB → 10.1GB

---

## 长期建议

### 🔴 高优先级 - 设置页面文件到 D 盘
需要在 **管理员权限** 下执行以下命令（当前尝试提升权限超时）:

```cmd
# 创建 D:\setpagefile.cmd 后用右键管理员运行
wmic computersystem where "name='%computername%'" set AutomaticManagedPagefile=false
wmic pagefileset delete
wmic pagefileset create name="D:\pagefile.sys",InitialSize=8192,MaximumSize=24576
```

D盘有 33GB 空余，设置 8GB-24GB 的页面文件可缓解内存压力。

### 🟡 中优先级 - 优化 QClaw 内存配置
- `--max-old-space-size=4096` 在 16GB 系统上过于激进
- 建议降低到 **2048 (2GB)** 或 **3072 (3GB)**
- 需要通过更新 QClaw 应用启动参数来实现

### 🟢 低优先级 - 后台进程管理
- `ima.copilot` 会启动多个实例，建议限制数量
- `WorkBuddy` 类似，建议检查配置
- `GameViewer` (295MB) 如不需要可关闭

---

*报告自动生成于: 2026-06-09 13:56*
