const fs = require('fs');

const p = 'D:/QClaw/v0.2.35.624/resources/openclaw/node_modules/openclaw/dist/channel.runtime-AscTY00w.js';
const b = fs.readFileSync(p);
const txt = b.toString('utf8');

const needles = ['hermes', 'cli_main', '找不到', 'hermes-paths', 'runtime:hermes', 'invoke.*hermes'];
for (const n of needles) {
    if (txt.includes(n)) {
        let pos = 0;
        let count = 0;
        console.log('\n=== ' + n + ' ===');
        while ((pos = txt.indexOf(n, pos)) !== -1 && count < 3) {
            console.log('  [' + pos + ']: ' + txt.slice(Math.max(0, pos - 40), pos + 80));
            pos += n.length;
            count++;
        }
    }
}
console.log('\nDone');
