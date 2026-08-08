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

// 读 bytecode-loader
for (const p of ['out/main/bytecode-loader.cjs', 'out/preload/bytecode-loader.cjs']) {
  const t = allFiles.find(f => f.path === p);
  if (!t) { console.log(`不存在: ${p}`); continue; }
  const buf = Buffer.alloc(t.size);
  fs.readSync(fd, buf, 0, t.size, dataStart + t.offset);
  console.log(`\n=== ${p} (${t.size} bytes) ===`);
  console.log(buf.toString('utf8').slice(0, 8000));
}

// 尝试从 cjsc 提取可读字符串
console.log('\n=== cjsc 文件尺寸 ===');
allFiles.filter(f => f.path.endsWith('.cjsc')).forEach(f => console.log(`  ${f.path} (${f.size})`));
