const fs = require('fs');
const asarPath = process.argv[2];
const targetPath = 'out/renderer/assets/c-DMOGrtit.js';

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
  if (depth > 10) return;
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
const buf = Buffer.alloc(target.size);
fs.readSync(fd, buf, 0, target.size, dataStart + target.offset);
const text = buf.toString('utf8');

// 搜与 hermes agent / 轩恒 / 会话列表 相关的逻辑
const patterns = ['getAgent', 'electronAPI.hermes', 'listSessions', 'sessionList', '会话', '轩恒', 'getSession', 'sessionsStore', 'backendType'];
patterns.forEach(p => {
  let idx = -1;
  const hits = [];
  while ((idx = text.indexOf(p, idx + 1)) !== -1) {
    hits.push(idx);
    if (hits.length >= 3) break;
  }
  if (hits.length === 0) return;
  console.log(`\n### ${p} : ${hits.length}+ 命中 ###`);
  hits.forEach(h => {
    const s = Math.max(0, h - 150);
    const e = Math.min(text.length, h + 150);
    console.log('  ...' + text.slice(s, e).replace(/\n/g, ' ') + '...');
  });
});
