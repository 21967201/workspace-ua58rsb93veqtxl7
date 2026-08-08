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
    else if (info.size !== undefined) results.push({ path: full, size: info.size, offset: Number(info.offset), unpacked: !!info.unpacked });
  }
}

const { fd, header, dataStart } = parseAsar(asarPath);
const allFiles = [];
walk(header.files, '', allFiles, 0);

const target = allFiles.find(f => f.path === targetPath);
if (!target) { console.log('找不到 ' + targetPath); process.exit(1); }

const buf = Buffer.alloc(target.size);
fs.readSync(fd, buf, 0, target.size, dataStart + target.offset);
const text = buf.toString('utf8');

// 搜索会话列表相关关键字
const keywords = ['session', 'history', 'conversation', 'chat_list', 'conversations', 'chat_history', 'message_history', 'getSession', 'loadSession', 'fetchSession'];
keywords.forEach(k => {
  let idx = text.indexOf(k);
  if (idx === -1) return;
  console.log(`\n=== ${k} (首次出现在 ${idx}) ===`);
  // 打印前后各200字符
  const start = Math.max(0, idx - 200);
  const end = Math.min(text.length, idx + 200);
  console.log('...' + text.slice(start, end).replace(/\n/g, ' ') + '...');
});
