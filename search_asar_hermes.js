// 提取 asar 中所有含 hermes 的文件内容到内存搜索
const fs = require('fs');

const asarPath = process.argv[2];
const searchTerms = process.argv.slice(3);

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
    else if (info.size !== undefined) results.push({ path: full, size: info.size, offset: Number(info.offset), unpacked: !!info.unpacked });
  }
}

const { fd, header, dataStart } = parseAsar(asarPath);
const results = [];
walk(header.files, '', results, 0);

// 读取含 hermes 的文件（只读前 200KB 防爆内存）
const hits = [];
for (const r of results) {
  if (r.unpacked || r.size > 2000000) continue;
  const p = r.path.toLowerCase();
  if (!p.endsWith('.js') && !p.endsWith('.json')) continue;
  const buf = Buffer.alloc(r.size);
  fs.readSync(fd, buf, 0, r.size, dataStart + r.offset);
  const text = buf.toString('utf8');
  if (text.includes('hermes') || text.includes('Hermes')) {
    hits.push({ path: r.path, size: r.size, sample: text.slice(0, 300) });
  }
}
console.log(`含 hermes 的文件: ${hits.length}`);
hits.slice(0, 40).forEach(h => {
  console.log(`\n=== ${h.path} (${h.size}) ===`);
  console.log(h.sample.replace(/\n/g, ' ').slice(0, 250));
});
