const fs = require('fs');
const needle = Buffer.from('找不到 Hermes CLI');
const roots = [
  'D:/QClaw/v0.2.35.624/resources/hermes/libs',
  'D:/QClaw/v0.2.35.624/resources/hermes/plugins',
  'D:/QClaw/v0.2.35.624/resources/hermes/skills',
  'D:/QClaw/v0.2.35.624/resources/app.asar.unpacked/node_modules'
];
let searched = 0;
let found = 0;
for (const root of roots) {
  try {
    function walk(dir) {
      try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const e of entries) {
          const p = dir + '/' + e.name;
          if (e.isDirectory()) {
            walk(p);
          } else if (e.isFile() && (e.name.endsWith('.py') || e.name.endsWith('.pyc') || e.name.endsWith('.pyd') || e.name.endsWith('.js') || e.name.endsWith('.mjs'))) {
            searched++;
            try {
              const b = fs.readFileSync(p);
              for (let i = 0; i < b.length - needle.length; i++) {
                let m = true;
                for (let j = 0; j < needle.length; j++) {
                  if (b[i + j] !== needle[j]) { m = false; break; }
                }
                if (m) {
                  console.log('FOUND at', p, 'offset', i);
                  found++;
                }
              }
            } catch (e2) { }
          }
        }
      } catch (e1) { }
    }
    walk(root);
  } catch (e) { console.log('error', root, e.message); }
}
console.log('searched:', searched, 'found:', found);
