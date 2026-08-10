const fs = require('fs');
const b = fs.readFileSync('D:/QClawX/data/workspace-ua58rsb93veqtxl7/preload_cjsc.bin');
const needles = [
  '找不到 Hermes CLI',
  'hermes_paths',
  'hermes_cli_main_',
  '[hermes-paths]'
];
for (const n of needles) {
  const buf = Buffer.from(n);
  let found = false;
  for (let i = 0; i < b.length - buf.length; i++) {
    let m = true;
    for (let j = 0; j < buf.length; j++) {
      if (b[i + j] !== buf[j]) { m = false; break; }
    }
    if (m) {
      console.log('FOUND: ' + n + ' at ' + i + ' | ctx: ' + b.slice(Math.max(0, i - 50), i + 80).toString('utf8'));
      found = true;
    }
  }
  if (!found) console.log('NOT FOUND: ' + n);
}
console.log('done');
