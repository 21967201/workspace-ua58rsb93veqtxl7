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
    else if (info.size !== undefined) results.push({ path: full, size: info.size, offset: Number(info.offset), unpacked: !!info.unpacked });
  }
}
const { fd, header, dataStart } = parseAsar(asarPath);
const allFiles = [];
walk(header.files, '', allFiles, 0);

// 列出 out 目录顶层结构
console.log('=== out/ 目录结构（深度2）===');
const outFiles = allFiles.filter(f => f.path.startsWith('out/'));
const dirs = new Set();
outFiles.forEach(f => {
  const parts = f.path.split('/');
  if (parts.length >= 3) dirs.add(parts.slice(0, 3).join('/'));
  else dirs.add(f.path);
});
[...dirs].sort().slice(0, 50).forEach(d => console.log('  ' + d));
console.log(`\nout/ 文件总数: ${outFiles.length}`);
// 主进程 JS 通常在 out/main 或根
console.log('\n=== 非 renderer 的 JS 文件（前40）===');
outFiles.filter(f => !f.path.includes('/renderer/') && f.path.endsWith('.js')).slice(0, 40).forEach(f => console.log(`  ${f.path} (${f.size})`));
