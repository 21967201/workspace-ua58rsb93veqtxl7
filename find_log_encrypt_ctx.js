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

// 提取所有字符串并找 LOG_ENCRYPT_PUBLIC_KEY_PEM 附近（按顺序找索引）
const strs = [];
let cur = [];
for (let i = 0; i < b.length; i++) {
  const c = b[i];
  if (c >= 32 && c <= 126) cur.push(c);
  else { if (cur.length >= 5) strs.push({s: Buffer.from(cur).toString('utf8'), i: i - cur.length}); cur = []; }
}
if (cur.length >= 5) strs.push({s: Buffer.from(cur).toString('utf8'), i: b.length - cur.length});

// 找所有包含 encr/Encr 的字符串及其位置
const encStrs = strs.filter(x => /encr|Encr|ENCR|aes|AES|cipher|Cipher|decrypt|Decrypt|xor|XOR|scramble/i.test(x.s));
console.log("=== 加密相关字符串及偏移 ===");
encStrs.forEach(x => console.log(`${x.i}: ${x.s.slice(0, 120)}`));

// 找 LOG_ENCRYPT_PUBLIC_KEY_PEM 的偏移
const logEncIdx = strs.findIndex(x => x.s === 'LOG_ENCRYPT_PUBLIC_KEY_PEM');
if (logEncIdx >= 0) {
  console.log(`\n=== LOG_ENCRYPT_PUBLIC_KEY_PEM 在字符串列表位置 ${logEncIdx}，前后各 15 个字符串 ===`);
  for (let i = Math.max(0, logEncIdx - 15); i < Math.min(strs.length, logEncIdx + 15); i++) {
    console.log(`[${i}] (${strs[i].i}) ${strs[i].s.slice(0, 100)}`);
  }
}
