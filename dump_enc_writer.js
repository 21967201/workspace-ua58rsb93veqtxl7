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
  else { if (cur.length >= 4) strs.push({s: Buffer.from(cur).toString('utf8'), i: i - cur.length}); cur = []; }
}
if (cur.length >= 4) strs.push({s: Buffer.from(cur).toString('utf8'), i: b.length - cur.length});

// 从 requireMain$2 (352715) 到 appendJSON (358680) 全量输出，这是 EncryptedWriter 完整实现
console.log("=== EncryptedWriter 完整实现字符串（352715-358700）===");
strs.filter(x => x.i >= 352715 && x.i <= 359200).forEach(x => console.log(`(${x.i}) ${x.s.slice(0, 150)}`));

// 找 getAesKey 的定义位置附近的实现
console.log("\n=== getAesKey 区域（22581 附近的实现）===");
// 找 'getAesKey' 字符串之后最近的实现代码——从 22600 开始找
strs.filter(x => x.i >= 22581 && x.i <= 32000).forEach(x => console.log(`(${x.i}) ${x.s.slice(0, 150)}`));
