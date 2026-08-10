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
const strs = [];
let cur = [];
for (let i = 0; i < b.length; i++) { const c = b[i]; if (c >= 32 && c <= 126) cur.push(c); else { if (cur.length >= 5) strs.push({s: Buffer.from(cur).toString('utf8'), i: i - cur.length}); cur = []; } }
if (cur.length >= 5) strs.push({s: Buffer.from(cur).toString('utf8'), i: b.length - cur.length});

// 找 PYTHON_BIN_NAME / python.exe 的所有出现位置
['PYTHON_BIN_NAME', 'QCLAW_PYTHON_BINARY', 'python/python.exe', 'Python311'].forEach(name => {
  const positions = [];
  strs.forEach((x, idx) => { if (x.s === name) positions.push(idx); });
  console.log(`\n=== ${name} 出现 ${positions.length} 次 ===`);
  positions.slice(0, 3).forEach(idx => {
    console.log(`  [${idx}] 前后 12 字符串:`);
    for (let i = Math.max(0, idx - 12); i < Math.min(strs.length, idx + 12); i++) {
      console.log(`    [${i}] (${strs[i].i}) ${strs[i].s.slice(0, 100)}`);
    }
    console.log('  ---');
  });
});
