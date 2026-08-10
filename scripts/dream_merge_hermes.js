const fs = require('fs');
const p = 'D:\\QClawX\\data\\workspace-ua58rsb93veqtxl7\\MEMORY.md';
let t = fs.readFileSync(p, 'utf8');

const before = '### 2026-08-05 Hermes 修复总结';
const after = 'models[].provider 仅展示不路由。';
const b = t.indexOf(before);
const a = t.indexOf(after) + after.length;
if (b < 0 || a < b) {
  console.error('markers not found: b=' + b + ' a=' + a);
  process.exit(1);
}

const replacement = [
  '### Hermes 修复与数据线（2026-08-05 + 08-08 合并）',
  '',
  '**08-05 修复**（角色无法调模型，UI 显示 [object Object]）：根因 = HERMES_HOME 指向不存在路径 + API Key 名不匹配 + config 过旧(v0→v33) + provider 错误(custom:zhipu→custom:agnes)。修复：重设 HERMES_HOME=C:\\Users\\Administrator\\.hermes、添加 HERMES_ZHIPU_API_KEY、doctor --fix、默认模型改 agnes-2.5-flash、重启 Gateway。验证 ✅（agnes-2.5-flash 与 glm-4-flash 均正常响应）。',
  '',
  '**三条数据线（关键稳定事实，勿再混淆）**：',
  '- `C:\\Users\\Administrator\\.hermes\\` = CLI/cron 用（8/5-8/7 修的，provider=custom:agnes）',
  '- `C:\\Users\\Administrator\\.qclaw-hermes\\` = **QClaw 前端"轩恒"真正数据源**（provider=qclaw, default=pool-hy3-preview, base_url=http://127.0.0.1:19000/proxy/llm）',
  '- `D:\\QClaw\\v0.2.35.624\\resources\\hermes\\.hermes\\` = 打包内置 Hermes，已停用',
  '',
  '**08-08 会话丢失事件**：audit.db 8/4 16:22 后停写；QClaw 8/8 自动合并只迁移 59/156 会话。数据未丢（state.db 156 会话/11709 消息完整）。修复：`migrate_state_to_audit.py` 幂等同步 97 会话/3219 消息 → audit 59→156 会话、4467→7686 消息 ✅。未决（等官方）：audit.db 停写根因、agent.json polluted(60)、tui_gateway GBK crash。',
  '',
  '**环境事实**：端口 8642（qclaw_launcher）/19000（auth-gateway）/57199（OpenClaw gateway）；前端"轩恒"= agentId hermes_default；Hermes provider 解析优先级 provider > config > env > auto（cli.py:3909-3914），models[].provider 仅展示不路由。',
  ''
].join('\n');

const newT = t.substring(0, b) + replacement + t.substring(a);
fs.writeFileSync(p, newT, 'utf8');
console.log('OK old=' + t.length + ' new=' + newT.length + ' removed=' + (a - b - replacement.length));
