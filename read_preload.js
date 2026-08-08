const fs = require('fs');
const asarPath = process.argv[2];
const targetPath = 'out/preload/index.cjs';

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
const target = allFiles.find(f => f.path === targetPath);
if (!target) { console.log('不存在'); process.exit(1); }
const buf = Buffer.alloc(target.size);
fs.readSync(fd, buf, 0, target.size, dataStart + target.offset);
const text = buf.toString('utf8');
console.log(`=== ${targetPath} (${target.size} bytes) ===`);
console.log(text.slice(0, Math.min(30000, text.length)));
