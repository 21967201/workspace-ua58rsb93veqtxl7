const fs = require('fs');
// Search for the error source
const needles = [
  { name: '[hermes-paths]', buf: Buffer.from('[hermes-paths]') },
  { name: '找不到 Hermes CLI', buf: Buffer.from('找不到 Hermes CLI') },
  { name: 'hermes_cli_main_', buf: Buffer.from('hermes_cli_main_') }
];

const roots = [
  'D:/QClaw/v0.2.35.624/resources/hermes',
  'D:/QClaw/v0.2.35.624/resources/app.asar.unpacked',
  'D:/QClaw/v0.2.35.624/resources/openclaw'
];

let searched = 0;
for (const root of roots) {
  console.log('Searching in:', root);
  function walk(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const e of entries) {
        const p = dir + '/' + e.name;
        if (e.name === 'node_modules') continue; // skip, too big
        if (e.isDirectory()) {
          walk(p);
        } else if (e.isFile()) {
          const ext = e.name.split('.').pop();
          if (['py', 'pyc', 'pyd', 'js', 'mjs', 'cjs'].includes(ext)) {
            searched++;
            if (searched % 500 === 0) console.log('searched:', searched);
            try {
              const b = fs.readFileSync(p);
              for (const { name, buf } of needles) {
                for (let i = 0; i < b.length - buf.length; i++) {
                  let m = true;
                  for (let j = 0; j < buf.length; j++) {
                    if (b[i + j] !== buf[j]) { m = false; break; }
                  }
                  if (m) {
                    console.log('FOUND', name, 'in', p, 'at offset', i);
                  }
                }
              }
            } catch (e2) { }
          }
        }
      }
    } catch (e1) { }
  }
  walk(root);
}
console.log('Total searched:', searched);
