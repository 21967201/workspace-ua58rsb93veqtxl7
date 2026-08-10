const fs = require('fs');

// Scan runtime-paths-C5XqSP1M.js for hermes
const p = 'D:/QClaw/v0.2.35.624/resources/openclaw/node_modules/openclaw/dist/runtime-paths-C5XqSP1M.js';
const b = fs.readFileSync(p);
const txt = b.toString('utf8');

// Find all occurrences of 'hermes'
let pos = 0;
while ((pos = txt.indexOf('hermes', pos)) !== -1) {
  console.log('hermes at', pos, ':', txt.slice(Math.max(0, pos-30), pos+60));
  pos++;
}

// Also scan all dist files for hermes-paths or runtime:hermes
const dist = 'D:/QClaw/v0.2.35.624/resources/openclaw/node_modules/openclaw/dist';
const files = fs.readdirSync(dist);
const needles = ['hermes-paths', 'runtime:hermes:chat', '找不到 Hermes', 'hermes_cli_main_'];
for (const fn of files) {
  if (!fn.endsWith('.js')) continue;
  const content = fs.readFileSync(dist + '/' + fn, 'utf8');
  for (const n of needles) {
    if (content.includes(n)) {
      console.log('\nFOUND in', fn, ':', n);
    }
  }
}
console.log('\nDone scanning dist');
