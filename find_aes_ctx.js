const fs = require('fs');
const buf = fs.readFileSync('D:\\QClaw\\v0.2.35.624\\resources\\app.asar');
const headerSize = buf.readUInt32LE(12);
const header = JSON.parse(buf.slice(16, 16 + headerSize).toString('utf8'));
const files = [];
function walk(f, p) { for (const [n, i] of Object.entries(f)) { const fp = p ? p + '/' + n : n; if (i.files) walk(i.files, fp); else if (i.size !== undefined) files.push({path: fp, size: i.size, offset: Number(i.offset)}); } }
walk(header.files, '');
const target = files.find(f => f.path === 'out/main/index.cjsc');
const dataStart = 16 + headerSize;
const b = Buffer.alloc(target.size);
fs.readSync(fs.openSync('D:\\QClaw\\v0.2.35.624\\resources\\app.asar', 'r'), b, 0, target.size, dataStart + target.offset);

// 提取字符串
const strs = [];
let cur = [];
for (let i = 0; i < b.length; i++) {
  const c = b[i];
  if (c >= 32 && c <= 126) cur.push(c);
  else { if (cur.length >= 5) strs.push({s: Buffer.from(cur).toString('utf8'), i: i - cur.length}); cur = []; }
}
if (cur.length >= 5) strs.push({s: Buffer.from(cur).toString('utf8'), i: b.length - cur.length});

// getAesKey 上下文
const idx = strs.findIndex(x => x.s === 'getAesKey');
if (idx >= 0) {
  console.log("=== getAesKey 前后 20 字符串 ===");
  for (let i = Math.max(0, idx - 20); i < Math.min(strs.length, idx + 20); i++) console.log(`[${i}] (${strs[i].i}) ${strs[i].s.slice(0, 120)}`);
}
console.log("\n=== EncryptedWriter 前后 20 字符串 ===");
const idx2 = strs.findIndex(x => x.s === 'EncryptedWriter');
if (idx2 >= 0) {
  for (let i = Math.max(0, idx2 - 20); i < Math.min(strs.length, idx2 + 20); i++) console.log(`[${i}] (${strs[i].i}) ${strs[i].s.slice(0, 120)}`);
}
console.log("\n=== encryptAesCbc 前后 15 ===");
const idx3 = strs.findIndex(x => x.s === 'encryptAesCbc');
if (idx3 >= 0) {
  for (let i = Math.max(0, idx3 - 15); i < Math.min(strs.length, idx3 + 15); i++) console.log(`[${i}] (${strs[i].i}) ${strs[i].s.slice(0, 120)}`);
}
console.log("\n=== publicEncrypt / aes-256-gcm / createCipheriv 区域 ===");
const idx4 = strs.findIndex(x => x.s === 'publicEncrypt');
if (idx4 >= 0) {
  for (let i = Math.max(0, idx4 - 25); i < Math.min(strs.length, idx4 + 25); i++) console.log(`[${i}] (${strs[i].i}) ${strs[i].s.slice(0, 120)}`);
}
