const fs = require('fs');

function octalToInt(buf, offset, len) {
    let result = 0;
    for (let i = 0; i < len; i++) {
        const c = buf[offset + i] - 48;
        if (c < 0 || c > 7) return 0;
        result = result * 8 + c;
    }
    return result;
}

function findInTar(tarPath, patterns) {
    const buf = fs.readFileSync(tarPath);
    let offset = 0;
    let count = 0;
    const hits = [];
    
    while (offset < buf.length - 512) {
        const header = buf.slice(offset, offset + 512);
        const name = header.slice(0, 100).toString('utf8').replace(/\0.*$/, '');
        const size = octalToInt(header, 124, 12);
        
        if (name && name[0] !== '\0' && header[156] === 0) {
            for (const pat of patterns) {
                if (name.includes(pat)) {
                    hits.push({ name, size });
                }
            }
            count++;
        }
        
        const dataSize = Math.ceil(size / 512) * 512;
        offset += 512 + dataSize;
    }
    
    return hits;
}

console.log('Scanning hermes_1.tar...');
const h1 = findInTar('D:/QClaw/v0.2.35.624/resources/hermes_1.tar', ['hermes_paths', 'hermes_cli_main']);
console.log('hermes_1 hits:', h1.length, h1.slice(0, 10));

console.log('Scanning hermes_2.tar...');
const h2 = findInTar('D:/QClaw/v0.2.35.624/resources/hermes_2.tar', ['hermes_paths', 'hermes_cli_main']);
console.log('hermes_2 hits:', h2.length, h2.slice(0, 10));
console.log('Done');
