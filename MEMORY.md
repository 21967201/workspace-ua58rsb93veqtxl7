# MEMORY.md - Weekly Error Prevention Check Results

## 2026-06-03 Weekly Check (每周错误预防检查)

**检查时间**: 2026-06-03 09:42:44  
**违规总数**: 14,047 violations  
**状态**: ❌ 存在大量违规

### 检查结果
- ✅ AGENTS.md 存在
- ✅ SOUL.md 存在
- ✅ USER.md 存在
- ✅ IDENTITY.md 存在
- ✅ TOOLS.md 存在

### 违规类型统计
1. **文件类型违规** (不允许的文件类型): 约 14,045 项
   - 主要涉及: `.js`, `.ts`, `.d.ts`, `.mjs`, `.cjs`, `.cts`, `.map`, `.json`, `.wasm` 等文件
   - 来源: `node_modules`, `.git` 目录等依赖文件
   
2. **文件大小违规** (文件过大): 约 2 项
   - `diagnosticMessages.generated.json` (多个版本, 289KB-433KB)
   - `CHANGELOG.md` (134.9KB)
   - `db.json` (181.5KB, 199.1KB)
   - `mappingTable.json` (254.0KB)

### 建议处理
- 违规主要来自依赖文件和构建产物
- 建议将 `node_modules` 添加到 `.gitignore` 或使用更精准的检查规则
- 大型 JSON 文件可能需要拆分或压缩存储

---
*自动生成于: 2026-06-03 09:42*

## 2026-06-02 Weekly Check (每周错误预防检查)

**检查时间**: 2026-06-02 09:53:08  
**违规总数**: 14,142 violations  
**状态**: ❌ 存在大量违规

### 检查结果
- ✅ AGENTS.md 存在
- ✅ SOUL.md 存在
- ✅ USER.md 存在
- ✅ IDENTITY.md 存在
- ✅ TOOLS.md 存在

### 违规类型统计
1. **文件类型违规** (不允许的文件类型): 约 14,140 项
   - 主要涉及: `.js`, `.ts`, `.d.ts`, `.mjs`, `.cjs`, `.cts`, `.map`, `.json`, `.wasm` 等文件
   - 来源: `node_modules`, `.git` 目录等依赖文件
   
2. **文件大小违规** (文件过大): 约 2 项
   - `diagnosticMessages.generated.json` (多个版本, 289KB-433KB)
   - `CHANGELOG.md` (134.9KB)
   - `db.json` (181.5KB, 199.1KB)
   - `mappingTable.json` (254.0KB)

### 建议处理
- 违规主要来自依赖文件和构建产物
- 建议将 `node_modules` 添加到 `.gitignore` 或使用更精准的检查规则
- 大型 JSON 文件可能需要拆分或压缩存储

---
*自动生成于: 2026-06-02 09:53*

## 历史记录

### 2026-06-02 09:49 - 初次检查
- 违规总数: 14,142
- 状态: 需要清理依赖文件
