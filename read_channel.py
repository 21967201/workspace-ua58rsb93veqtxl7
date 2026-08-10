const fs = require('fs');

const dir = 'D:/QClaw/v0.2.35.624/resources/openclaw/node_modules/openclaw/dist';
const files = fs.readdirSync(dir).filter(f => f.startsWith('channel.runtime'));
console.log('channel.runtime files:', files.length);
for (const f of files) {
    const size = fs.statSync(dir + '/' + f).size;
    console.log('  ' + f + ' : ' + size);
}
