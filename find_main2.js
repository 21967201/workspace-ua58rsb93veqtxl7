const fs = require('fs');

const p = 'D:/QClaw/v0.2.35.624/resources/openclaw/node_modules/openclaw/dist/manager.runtime-DUEg9_u5.js';
const b = fs.readFileSync(p);
const txt = b.toString('utf8');
console.log('Size:', b.length);

// Find all 'hermes' occurrences in context
let pos = 0;
let count = 0;
while ((pos = txt.indexOf('hermes', pos)) !== -1 && count < 10) {
    console.log('[' + pos + ']:', txt.slice(Math.max(0,pos-50), pos+100));
    pos += 6;
    count++;
}

// Also search for 'cli_main'
const idx = txt.indexOf('cli_main');
console.log('\ncli_main at:', idx);
if (idx !== -1) console.log(txt.slice(Math.max(0,idx-50), idx+100));
