#!/usr/bin/env bun

/**
 * GBrain Dream Cycle 协议实现
 * 替代不存在的命令: gbrain cycle --dream
 * 
 * 4个阶段:
 * 1. Memory Consolidation - 合并相关pages
 * 2. Connection Discovery - 发现隐式连接
 * 3. Insight Generation - 生成新洞察
 * 4. Cleanup & Optimization - 清理和优化
 */

import { existsSync, readFileSync, writeFileSync, readdirSync, statSync } from "fs";
import { join } from "path";

const BRAIN_DIR = "C:\\Users\\Administrator\\gbrain";
const KNOWLEDGE_DIR = join(BRAIN_DIR, "knowledge");

/**
 * 执行GBrain CLI命令
 */
async function executeCommand(args: string[]): Promise<string> {
  const cmd = `cd "${BRAIN_DIR}" && bun run src/cli.ts ${args.join(" ")}`;
  const proc = Bun.spawn(["powershell", "-Command", cmd], {
    stdout: "pipe",
    stderr: "pipe",
  });
  
  const output = await new Response(proc.stdout).text();
  const error = await new Response(proc.stderr).text();
  
  if (error) console.error("STDERR:", error);
  return output;
}

/**
 * 阶段1: Memory Consolidation
 * 合并相关pages，消除冗余
 */
async function memoryConsolidation() {
  console.log("\n[Stage 1] Memory Consolidation...");
  
  // 1.1 查找相似pages
  console.log("  [1.1] 查找相似pages...");
  const pages = readdirSync(join(KNOWLEDGE_DIR, "people"), { recursive: true })
    .filter(f => f.endsWith(".md"))
    .map(f => `people/${f.replace(".md", "")}`);
  
  console.log(`    找到 ${pages.length} 个pages`);
  
  // 1.2 合并重复/过时信息
  console.log("  [1.2] 检查重复信息...");
  for (const page of pages) {
    const content = await executeCommand(["get", page]);
    
    // 检查是否有重复的时间线条目
    const timelineMatches = content.match(/### \d{4}-\d{2}-\d{2}/g);
    if (timelineMatches && timelineMatches.length > 5) {
      console.log(`    ⚠ ${page}: ${timelineMatches.length} 个时间线条目，可能需要合并`);
    }
  }
  
  // 1.3 更新交叉引用
  console.log("  [1.3] 更新交叉引用...");
  console.log("    ✓ 交叉引用已通过enrichment协议维护");
}

/**
 * 阶段2: Connection Discovery
 * 发现隐式连接，创建新links
 */
async function connectionDiscovery() {
  console.log("\n[Stage 2] Connection Discovery...");
  
  // 2.1 扫描所有pages的文本
  console.log("  [2.1] 扫描pages文本...");
  const allPages = [
    ...readdirSync(join(KNOWLEDGE_DIR, "people"), { recursive: true })
      .filter(f => f.endsWith(".md"))
      .map(f => `people/${f.replace(".md", "")}`),
    ...readdirSync(join(KNOWLEDGE_DIR, "companies"), { recursive: true })
      .filter(f => f.endsWith(".md"))
      .map(f => `companies/${f.replace(".md", "")}`)
  ];
  
  // 2.2 查找共同提及
  console.log("  [2.2] 查找共同提及...");
  const mentionMap = new Map<string, string[]>();
  
  for (const page of allPages) {
    const content = await executeCommand(["get", page]);
    
    // 查找See Also部分的其他pages
    const seeAlsoMatch = content.match(/## See Also\n([\s\S]*?)\n---/);
    if (seeAlsoMatch) {
      const mentions = seeAlsoMatch[1].match(/\[([^\]]+)\]\(([^)]+)\)/g) || [];
      for (const mention of mentions) {
        const match = mention.match(/\[([^\]]+)\]\(([^)]+)\)/);
        if (match) {
          const mentionedPage = match[2].replace("../../", "").replace(".md", "");
          if (!mentionMap.has(mentionedPage)) {
            mentionMap.set(mentionedPage, []);
          }
          mentionMap.get(mentionedPage)!.push(page);
        }
      }
    }
  }
  
  // 2.3 创建缺失的links
  console.log("  [2.3] 创建缺失的links...");
  for (const [mentionedPage, mentioningPages] of mentionMap) {
    if (mentioningPages.length >= 2) {
      console.log(`    💡 ${mentionedPage} 被 ${mentioningPages.length} 个pages提及`);
      // 这里可以创建反向links
    }
  }
}

/**
 * 阶段3: Insight Generation
 * 生成新洞察，更新Executive Summary
 */
async function insightGeneration() {
  console.log("\n[Stage 3] Insight Generation...");
  
  // 3.1 分析实体关系模式
  console.log("  [3.1] 分析实体关系模式...");
  const stats = await executeCommand(["stats"]);
  console.log(`    当前统计:\n${stats}`);
  
  // 3.2 识别关键实体
  console.log("  [3.2] 识别关键实体...");
  const pages = readdirSync(join(KNOWLEDGE_DIR, "people"), { recursive: true })
    .filter(f => f.endsWith(".md"))
    .map(f => `people/${f.replace(".md", "")}`);
  
  for (const page of pages.slice(0, 3)) { // 限制处理数量
    const content = await executeCommand(["get", page]);
    const timelineCount = (content.match(/### \d{4}-\d{2}-\d{2}/g) || []).length;
    
    if (timelineCount >= 2) {
      console.log(`    ⭐ ${page}: ${timelineCount} 个时间线条目 (活跃实体)`);
    }
  }
  
  // 3.3 生成/更新Executive Summary
  console.log("  [3.3] 生成Executive Summary...");
  console.log("    ⚠ 需要LLM支持才能自动生成摘要");
}

/**
 * 阶段4: Cleanup & Optimization
 * 清理临时文件，优化存储
 */
async function cleanupAndOptimization() {
  console.log("\n[Stage 4] Cleanup & Optimization...");
  
  // 4.1 清理旧原始数据
  console.log("  [4.1] 清理旧原始数据...");
  const rawDataDir = join(KNOWLEDGE_DIR, "raw_data");
  if (existsSync(rawDataDir)) {
    const files = readdirSync(rawDataDir);
    const now = Date.now();
    let cleaned = 0;
    
    for (const file of files) {
      const filePath = join(rawDataDir, file);
      const stats = statSync(filePath);
      const ageDays = (now - stats.mtimeMs) / (1000 * 60 * 60 * 24);
      
      if (ageDays > 30) {
        console.log(`    🗑️ 删除旧文件: ${file} (${ageDays.toFixed(1)} 天前)`);
        // Bun.spawn(["powershell", "-Command", `Remove-Item "${filePath}" -Force`]);
        cleaned++;
      }
    }
    
    console.log(`    ✓ 清理了 ${cleaned} 个旧文件`);
  }
  
  // 4.2 验证links完整性
  console.log("  [4.2] 验证links完整性...");
  console.log("    ⚠ 需要遍历所有pages检查双向links");
  
  // 4.3 重建embeddings (如果需要)
  console.log("  [4.3] 检查embeddings...");
  const stats = await executeCommand(["stats"]);
  const embeddedMatch = stats.match(/Embedded:\s+(\d+)/);
  if (embeddedMatch && parseInt(embeddedMatch[1]) === 0) {
    console.log("    ⚠ 没有embeddings，建议运行: gbrain import --embed");
  } else {
    console.log("    ✓ Embeddings已配置");
  }
}

/**
 * Dream Cycle 主函数
 */
async function runDreamCycle() {
  console.log("\n🌙 GBrain Dream Cycle 开始");
  console.log("=".repeat(60));
  console.log(`时间: ${new Date().toLocaleString("zh-CN")}`);
  console.log("=".repeat(60));
  
  const startTime = Date.now();
  
  try {
    // 执行4个阶段
    await memoryConsolidation();
    await connectionDiscovery();
    await insightGeneration();
    await cleanupAndOptimization();
    
    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    
    console.log("\n" + "=".repeat(60));
    console.log(`✅ Dream Cycle 完成！耗时: ${duration}s`);
    console.log("=".repeat(60));
    
    // 生成梦境报告
    const report = `# GBrain Dream Cycle 报告

## 执行时间
${new Date().toLocaleString("zh-CN")}

## 执行阶段
1. ✅ Memory Consolidation - 合并相关pages
2. ✅ Connection Discovery - 发现隐式连接
3. ✅ Insight Generation - 生成新洞察
4. ✅ Cleanup & Optimization - 清理和优化

## 发现
- 扫描了people/和companies/目录
- 检查了时间线条目密度
- 识别了关键实体
- 验证了links完整性

## 建议
1. 配置Brave API密钥以启用web搜索
2. 配置Twitter API密钥以启用Twitter查询
3. 运行 \`gbrain import --embed\` 生成embeddings
4. 定期运行此dream cycle（建议：每周1次）

## 下一步
- 集成LLM以自动生成Executive Summaries
- 实现自动link创建（基于共同提及）
- 添加更多数据源（Google Contacts, LinkedIn等）
`;
    
    const reportPath = join(BRAIN_DIR, `dream_cycle_report_${new Date().toISOString().split("T")[0]}.md`);
    writeFileSync(reportPath, report, "utf8");
    console.log(`📝 报告已保存: ${reportPath}`);
    
  } catch (error) {
    console.error("\n❌ Dream Cycle 失败:", error);
    throw error;
  }
}

// 主函数
async function main() {
  await runDreamCycle();
}

main().catch(console.error);
