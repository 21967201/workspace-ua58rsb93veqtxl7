// 解析 QClaw app.asar 找 launcher 启动逻辑
const fs = require('fs');
const path = require('path');

const ASAR_PATH = 'D:\\QClaw\\v0.2.35.624\\resources\\app.asar';

// 简化版 asar 解析（已知 header 格式：4B pickle size + 4+4+4 uint32 fields + pickle(header) + 4B pickle size + 4+4+4 uint32 fields + pickle(files list)）
function parseAsarHeader(buf) {
  let off = 0;
  // 第一段 pickle header (metadata about contents)
  const pickleSize1 = buf.readUInt32LE(off); off += 4;
  // skip 3 uint32 fields
  off += 12;
  const pickle1 = buf.slice(off, off + pickleSize1); off += pickleSize1;
  // 第二段 pickle header (files list)
  const pickleSize2 = buf.readUInt32LE(off); off += 4;
  off += 12;
  const pickle2 = buf.slice(off, off + pickleSize2); off += pickleSize2;
  // 之后是文件内容
  return { pickle1: pickle1.toString('utf8'), pickle2: pickle2.toString('utf8'), contentOffset: off };
}

const buf = fs.readFileSync(ASAR_PATH);
const header = parseAsarHeader(buf);
console.log('pickle2 length:', header.pickle2.length);
console.log('contentOffset:', header.contentOffset);

// 列出所有 out/main, out/preload, src/main 等可读目录
const files = header.pickle2.split('\0').filter(s => s && (/^out\//.test(s) || /^src\/main/.test(s) || /^package\.json/.test(s) || /main\.js/.test(s) || /launcher/.test(s) || /hermes-cli/.test(s) || /HermesTar/.test(s) || /HermesExt/.test(s) || /child_process/.test(s)));
console.log('--- matching files ---');
files.slice(0, 50).forEach(f => console.log(' ', f));
console.log('total:', files.length);
