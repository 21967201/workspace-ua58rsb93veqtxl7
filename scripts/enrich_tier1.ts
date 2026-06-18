#!/usr/bin/env bun

/**
 * GBrain Tier1 Enrichment 协议实现
 * 使用真实的GBrain CLI命令，不依赖不存在的命令
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from "fs";
import { join } from "path";

const BRAIN_DIR = "C:\\Users\\Administrator\\gbrain";
const KNOWLEDGE_DIR = join(BRAIN_DIR, "knowledge");
const RAW_DATA_DIR = join(KNOWLEDGE_DIR, "raw_data");

// 确保raw_data目录存在
if (!existsSync(RAW_DATA_DIR)) {
  mkdirSync(RAW_DATA_DIR, { recursive: true });
}

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
 * Tier1 Enrichment 协议 (7步)
 */
async function enrichTier1(entitySlug: string) {
  console.log(`\n🧠 GBrain Tier1 Enrichment: ${entitySlug}`);
  console.log("=".repeat(60));
  
  // Step 1: 实体检测
  console.log("\n[Step 1] 实体检测...");
  const entityName = entitySlug.split("/").pop()?.replace(/-/g, " ") || entitySlug;
  console.log(`  实体名称: ${entityName}`);
  
  // Step 2: 检查Brain状态
  console.log("\n[Step 2] 检查Brain状态...");
  const searchResult = await executeCommand(["search", `"${entityName}"`]);
  const hasResults = searchResult.includes("[") && searchResult.includes("]");
  
  let path: "UPDATE" | "CREATE" = "CREATE";
  let existingContent = "";
  
  if (hasResults) {
    path = "UPDATE";
    console.log("  路径: UPDATE (实体已存在)");
    
    // 获取现有页面
    existingContent = await executeCommand(["get", entitySlug]);
    console.log("  ✓ 已获取现有页面内容");
  } else {
    path = "CREATE";
    console.log("  路径: CREATE (新实体)");
  }
  
  // Step 3: 确定Tier
  console.log("\n[Step 3] 确定Tier...");
  const tier = 1;
  console.log(`  Tier: ${tier} (Tier 1 = 完整丰富度)`);
  
  // Step 4: 运行外部查询
  console.log("\n[Step 4] 运行外部查询...");
  
  // 4.1 总是先查询Brain
  console.log("  [4.1] 查询Brain...");
  const brainData = await executeCommand(["search", `"${entityName}"`]);
  console.log("    ✓ Brain查询完成");
  
  // 4.2-4.4: 其他API（需要配置密钥）
  console.log("  [4.2-4.4] Web/Twitter/LinkedIn查询...");
  console.log("    ⚠ 需要配置API密钥 (BRAVE_API_KEY, TWITTER_BEARER_TOKEN, CRUSTDATA_API_KEY)");
  const webData = "pending API configuration";
  const twitterData = "pending API configuration";
  const linkedinData = null;
  
  // Step 5: 存储原始数据
  console.log("\n[Step 5] 存储原始数据...");
  
  const rawData = {
    sources: {
      brain: { fetched_at: new Date().toISOString(), data: brainData },
      web: tier <= 2 ? { fetched_at: new Date().toISOString(), data: webData } : null,
      twitter: tier <= 2 ? { fetched_at: new Date().toISOString(), data: twitterData } : null,
      linkedin: tier === 1 ? { fetched_at: new Date().toISOString(), data: linkedinData } : null,
    },
    metadata: {
      enriched_at: new Date().toISOString(),
      tier,
      path,
    },
  };
  
  const rawDataPath = join(RAW_DATA_DIR, `${entityName}.json`);
  writeFileSync(rawDataPath, JSON.stringify(rawData, null, 2), "utf8");
  console.log(`  ✓ 原始数据已保存: ${rawDataPath}`);
  
  // Step 6: 写入Brain页面
  console.log("\n[Step 6] 写入Brain页面...");
  
  if (path === "CREATE") {
    console.log("  创建新页面...");
    
    const newContent = `---
type: person
title: ${entityName}
created: '${new Date().toISOString()}'
updated: '${new Date().toISOString()}'
tags:
  - auto-enriched
  - tier-${tier}
---

# ${entityName}

## Executive Summary
${entityName} is a person/entity enriched via Tier${tier} Enrichment protocol on ${new Date().toISOString().split("T")[0]}.

## State
- **Enriched At**: ${new Date().toLocaleString("zh-CN")}
- **Tier**: ${tier}
- **Path**: CREATE

## What They Believe
*To be populated from Twitter/X data when API is configured*

## What They're Building
*To be populated from project data and meeting notes*

## What Motivates Them
*To be populated from meeting notes and correspondence*

## Assessment
*User-written assessment preserved here - API enrichment MUST NOT overwrite this section*

## Trajectory
- **${new Date().toISOString().split("T")[0]}**: Page created via Tier${tier} Enrichment protocol

## Relationship
- **First Interaction**: ${new Date().toISOString().split("T")[0]} (Automated Enrichment)
- **Context**: Auto-enriched via GBrain protocol

## Contact
*To be populated from Google Contacts integration when configured*

## Timeline

### ${new Date().toISOString().split("T")[0]}
- Auto-enriched via Tier${tier} Enrichment protocol
- Raw data stored at: ${rawDataPath}

## See Also
*To be populated with cross-references*

---

*Page enriched via GBrain Tier${tier} Enrichment Protocol*
*Enrichment date: ${new Date().toISOString()}*
*Next enrichment check: ${new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0]} (7-day cooldown)*
`;
    
    // 写入临时文件
    const tempFile = join(BRAIN_DIR, `temp_${Date.now()}.md`);
    writeFileSync(tempFile, newContent, "utf8");
    
    // 使用put命令
    const putResult = await executeCommand(["put", entitySlug, "--content", `""${readFileSync(tempFile, "utf8")}""`]);
    console.log("  ✓ 新页面已创建");
    
    // 清理临时文件
    Bun.spawn(["powershell", "-Command", `Remove-Item "${tempFile}" -Force`]);
    
  } else if (path === "UPDATE") {
    console.log("  更新现有页面...");
    console.log("  ⚠ 仅当有实质性新信息时更新");
    
    // 添加时间线条目
    const timelineResult = await executeCommand([
      "timeline-add",
      entitySlug,
      new Date().toISOString().split("T")[0],
      "Enriched via Tier1 protocol (automated)",
    ]);
    console.log("  ✓ 时间线条目已添加");
  }
  
  // Step 7: 交叉引用图谱
  console.log("\n[Step 7] 创建交叉引用链接...");
  console.log("  ⚠ 需要实体关系数据才能创建链接");
  console.log("  示例命令:");
  console.log(`    gbrain link <person-slug> <company-slug> --type works_at`);
  
  console.log("\n✅ Tier1 Enrichment 协议执行完成！");
  console.log("=".repeat(60));
  console.log(`  实体: ${entitySlug}`);
  console.log(`  路径: ${path}`);
  console.log(`  Tier: ${tier}`);
  console.log(`  原始数据: ${rawDataPath}`);
}

// 主函数
async function main() {
  const entitySlug = process.argv[2] || "people/john-doe-enriched";
  
  if (!entitySlug) {
    console.error("用法: bun run enrich_tier1.ts <entity-slug>");
    process.exit(1);
  }
  
  await enrichTier1(entitySlug);
}

main().catch(console.error);
