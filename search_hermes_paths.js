const fs = require('fs');
const needle = Buffer.from('hermes-paths');
const dirs = [
  'C:/Users/Administrator/AppData/Roaming/Python/Python311/site-packages',
  'D:/QClaw/v0.2.35.624/resources/python/Lib/site-packages'
];
for (const root of dirs) {
  try {
    const entries = fs.readdirSync(root, { withFileTypes: true });
    for (const e of entries) {
      if (!e.name.toLowerCase().includes('hermes') && !e.name.toLowerCase().includes('qclaw')) continue;
      const p = root + '/' + e.name;
      if (e.isDirectory()) {
        try {
          const files = fs.readdirSync(p, { withFileTypes: true });
          for (const f of files) {
            const fp = p + '/' + f.name;
            try {
              const b = fs.readFileSync(fp);
              for (let i = 0; i < b.length - needle.length; i++) {
                let m = true;
                for (let j = 0; j < needle.length; j++) if (b[i + j] !== needle[j]) { m = false; break; }
                if (m) { console.log('FOUND at', fp, 'offset', i); }
              }
            } catch (e2) { }
          }
        } catch (e1) { }
      } else {
        const b = fs.readFileSync(p);
        for (let i = 0; i < b.length - needle.length; i++) {
          let m = true;
          for (let j = 0; j < needle.length; j++) if (b[i + j] !== needle[j]) { m = false; break; }
          if (m) { console.log('FOUND at', p, 'offset', i); }
        }
      }
    }
  } catch (e) { console.log('error', root, e.message); }
}
console.log('done');
