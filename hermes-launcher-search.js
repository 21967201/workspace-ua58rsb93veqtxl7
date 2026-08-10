// 搜索 app.asar 中所有与 launcher 启动相关的模块路径
const fs = require('fs');
const ASAR_PATH = 'D:\\QClaw\\v0.2.35.624\\resources\\app.asar';
const buf = fs.readFileSync(ASAR_PATH);

// 提取所有 nul 分隔的字符串（jarvis 风格 pickle 视图）
let off = 0;
off += 4; // pickle size
off += 12; // 3 uint32
const pickleSize1 = buf.readUInt32LE(0);
off = 4 + 12 + pickleSize1;
off += 4; off += 12;
const pickleSize2 = buf.readUInt32LE(off);
const pickle2 = buf.slice(off + 4 + 12, off + 4 + 12 + pickleSize2).toString('utf8');

// 整个 pickle2 包含 JSON 形式的对象（如 {"key":{"files":{...}}...}）
// 提取所有可能的文件路径（路径含 \）
const pathLike = pickle2.match(/[A-Za-z0-9_\-\.\/\\]+\.(cjs|js|cjsc|mjs|ts|json|node)/g) || [];
const lc = pathLike.filter(p => /hermes|launcher|main\.cjs|preload|main\.js|index\.cjs/i.test(p));
console.log('hermes/launcher/main files:');
lc.forEach(p => console.log(' ', p));

// 同时搜文件中文字符串（entry 启动逻辑）—— 直接在 raw bytes 里搜
const text = buf.toString('latin1');
const keywords = ['qclaw_launcher', 'python -m', 'child_process', 'spawn', 'launchHermes', 'HermesLauncher', '启动', '拉起', 'bootHermes', 'HermesStart', 'HermesExt', 'isHermesAlive'];
keywords.forEach(k => {
  const idx = text.indexOf(k);
  if (idx >= 0) {
    const start = Math.max(0, idx - 100);
    const end = Math.min(text.length, idx + 200);
    console.log(`\n=== ${k} at ${idx} ===`);
    console.log(text.substring(start, end).replace(/[^\x20-\x7E一-鿿]/g, '.'));
  }
});
