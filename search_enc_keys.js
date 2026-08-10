const fs = require('fs');
const asarPath = 'D:\\QClaw\\v0.2.35.624\\resources\\app.asar';
const buf = fs.readFileSync(asarPath);
const headerSize = buf.readUInt32LE(12);
const header = JSON.parse(buf.slice(16, 16 + headerSize).toString('utf8'));
const files = [];
function walk(f, p) {
  for (const [n, i] of Object.entries(f)) {
    const fp = p ? p + '/' + n : n;
    if (i.files) walk(i.files, fp);
    else if (i.size !== undefined) files.push({path: fp, size: i.size, offset: Number(i.offset)});
  }
}
walk(header.files, '');
const target = files.find(f => f.path === 'out/main/index.cjsc');
const dataStart = 16 + headerSize;
const b = Buffer.alloc(target.size);
fs.readSync(fs.openSync(asarPath, 'r'), b, 0, target.size, dataStart + target.offset);
const strs = [];
let cur = [];
for (let i = 0; i < b.length; i++) {
  const c = b[i];
  if (c >= 32 && c <= 126) cur.push(c);
  else { if (cur.length >= 8) strs.push(Buffer.from(cur).toString('utf8')); cur = []; }
}
if (cur.length >= 8) strs.push(Buffer.from(cur).toString('utf8'));

// 找 PEM 公钥和私钥相关
const pemHits = strs.filter(s => s.includes('BEGIN') || s.includes('PRIVATE') || s.includes('PUBLIC') || /log.?encrypt|encrypt.?log|LOG_ENCRYPT/i.test(s));
console.log("=== PEM / 密钥相关字符串 ===");
const seen = new Set();
pemHits.slice(0, 60).forEach(s => { if (!seen.has(s)) { seen.add(s); console.log(s.slice(0, 200)); } });

// 找 EncryptedWriter / isEncryptedLogFile 周围的字符串（找 .enc 相关逻辑线索）
console.log("\n=== .enc / log 加密相关 ===");
const encHits = strs.filter(s => /\.enc|logPath|logFile|encryptedLog|ENCRYPTED_FILE/i.test(s));
const seen2 = new Set();
encHits.slice(0, 40).forEach(s => { if (!seen2.has(s)) { seen2.add(s); console.log(s.slice(0, 200)); } });
