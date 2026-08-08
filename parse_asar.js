// 解析 asar 归档（asar 格式：4字节头 + JSON + 文件数据）
const fs = require('fs');
const path = require('path');

const asarPath = process.argv[2];
const outDir = process.argv[3];
const onlyList = process.argv[4] === '--list';

function parseAsar(asarPath) {
  const fd = fs.openSync(asarPath, 'r');
  // 实际结构（Electron asar pickle 格式）:
  //   offset 0: 4 bytes = 0x04 0x00 0x00 0x00
  //   offset 4: 4 bytes LE = pickle size
  //   offset 8: 4 bytes LE = JSON header size
  //   offset 12: 4 bytes LE = JSON header size (重复)
  //   offset 16: JSON header
  //   数据区从 16 + headerSize 开始
  const buf16 = Buffer.alloc(16);
  fs.readSync(fd, buf16, 0, 16, 0);
  const headerSize = buf16.readUInt32LE(12);
  const headerBuf = Buffer.alloc(headerSize);
  fs.readSync(fd, headerBuf, 0, headerSize, 16);
  const header = JSON.parse(headerBuf.toString('utf8'));
  const dataStart = 16 + headerSize;
  return { fd, header, dataStart };
}

function walk(files, prefix, outDir, results, depth) {
  if (depth > 8) return;
  for (const [name, info] of Object.entries(files)) {
    const full = prefix ? `${prefix}/${name}` : name;
    if (info.files) {
      walk(info.files, full, outDir, results, depth + 1);
    } else if (info.size !== undefined) {
      results.push({ path: full, size: info.size, offset: info.offset, unpacked: !!info.unpacked });
    }
  }
}

function extractFile(fd, dataStart, entry) {
  if (entry.unpacked) return null;
  const buf = Buffer.alloc(entry.size);
  fs.readSync(fd, buf, 0, entry.size, dataStart + entry.offset);
  return buf;
}

const { fd, header, dataStart } = parseAsar(asarPath);
const results = [];
walk(header.files, '', outDir, results, 0);
console.log(`总文件数: ${results.length}`);

// 只列关键文件
const keyFiles = results.filter(r => {
  const p = r.path.toLowerCase();
  return (p.includes('hermes') || p.includes('session') || p.includes('chat') || p.includes('conversation')) 
    && (p.endsWith('.js') || p.endsWith('.json') || p.endsWith('.html'));
});
console.log(`hermes/session/chat 相关 JS/JSON: ${keyFiles.length}`);
keyFiles.slice(0, 30).forEach(f => console.log(`  ${f.path} (${f.size})`));
