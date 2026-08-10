const fs = require('fs');
const b = fs.readFileSync('D:/QClaw/v0.2.35.624/resources/app.asar');
const hs = b.readUInt32LE(4);
const header = b.slice(16, 16 + hs).toString('utf8');
console.log('header length:', header.length);

const idx1 = header.indexOf('hermes-paths');
console.log('hermes-paths:', idx1);
if (idx1 >= 0) console.log(header.slice(Math.max(0, idx1 - 100), idx1 + 300));

const idx2 = header.indexOf('hermes_cli_main');
console.log('hermes_cli_main:', idx2);

const idx3 = header.indexOf('hermes_cli');
console.log('hermes_cli:', idx3);
if (idx3 >= 0) console.log(header.slice(Math.max(0, idx3 - 50), idx3 + 200));
