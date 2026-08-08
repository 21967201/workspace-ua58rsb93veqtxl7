const fs = require('fs');
const asarPath = process.argv[2];

function parseAsar(asarPath) {
  const fd = fs.openSync(asarPath, 'r');
  const buf16 = Buffer.alloc(16);
  fs.readSync(fd, buf16, 0, 16, 0);
  const headerSize = buf16.readUInt32LE(12);
  const headerBuf = Buffer.alloc(headerSize);
  fs.readSync(fd, headerBuf, 0, headerSize, 16);
  const header = JSON.parse(headerBuf.toString('utf8'));
  const dataStart = 16 + headerSize;
  return { fd, header, dataStart };
}
function walk(files, prefix, results, depth) {
  if (depth > 12) return;
  for (const [name, info] of Object.entries(files)) {
    const full = prefix ? `${prefix}/${name}` : name;
    if (info.files) walk(info.files, full, results, depth + 1);
    else if (info.size !== undefined) results.push({ path: full, size: info.size, offset: Number(info.offset) });
  }
}
const { fd, header, dataStart } = parseAsar(asarPath);
const allFiles = [];
walk(header.files, '', allFiles, 0);

const target = allFiles.find(f => f.path === 'out/main/index.cjsc');
const buf = Buffer.alloc(target.size);
fs.readSync(fd, buf, 0, target.size, dataStart + target.offset);

// 提取 ASCII 可打印字符串（长度>=6）
const strings = [];
let cur = [];
for (let i = 0; i < buf.length; i++) {
  const b = buf[i];
  if (b >= 32 && b <= 126) { cur.push(b); }
  else {
    if (cur.length >= 6) strings.push(Buffer.from(cur).toString('utf8'));
    cur = [];
  }
}
if (cur.length >= 6) strings.push(Buffer.from(cur).toString('utf8'));
console.log(`提取字符串总数: ${strings.length}`);

// 找会话相关
const sessionStrings = strings.filter(s => /session|Session|conversation|Conversation|chat|Chat|history|History|hermes|Hermes|audit|state\.db|listSession|getSession/i.test(s));
console.log(`\n=== 会话/hermes 相关字符串 (${sessionStrings.length}) ===`);
const seen = new Set();
sessionStrings.forEach(s => {
  if (seen.has(s)) return;
  seen.add(s);
  console.log(`  ${JSON.stringify(s)}`);
});
