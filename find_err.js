const fs = require('fs');

// Search for the UTF-8 hex of "找不到 Hermes CLI 模块" in index_cjsc.bin
// 找: e4 bd a0, 不: e4 b8 8d, 到: e5 88 b0, 空格: 20
// H: 48 e=65 r=72 m=6d e=65 s=73
// C: 43 l=6c i=69
// 空格: 20
// M: 4d o=6f d=64
// 空格: 20
// 模: e6 a8 95, 块: e5 9d 97
// The full string: "找不到 Hermes CLI 模块"
// UTF-8 bytes as hex buffer
const needle = Buffer.from('e4bda0e4b88de588b0204865726d657320434c4920e6a895e593972095d97');
console.log('Searching for hex:', needle.toString('hex'));
console.log('Length:', needle.length);

// Actually let's just search for "hermes_cli_main_" as ASCII
const needle2 = Buffer.from('hermes_cli_main_');
console.log('\nSearching for "hermes_cli_main_" in index_cjsc.bin...');

const bin = fs.readFileSync('D:/QClawX/data/workspace-ua58rsb93veqtxl7/index_cjsc.bin');
let pos = bin.indexOf(needle2);
if (pos !== -1) {
    console.log('FOUND at', pos, ':', bin.slice(Math.max(0,pos-30), pos+60).toString('utf8'));
} else {
    console.log('NOT FOUND');
}

// Also try "找不到" as UTF-8
const needle3 = Buffer.from([0xe4, 0xbd, 0xa0, 0xe4, 0xb8, 0x8d, 0xe5, 0x88, 0xb0]);
console.log('\nSearching for "找不到" (UTF-8) in index_cjsc.bin...');
pos = bin.indexOf(needle3);
if (pos !== -1) {
    console.log('FOUND at', pos, ':', bin.slice(Math.max(0,pos-30), pos+80).toString('utf8'));
    // Also show hex
    console.log('Hex:', bin.slice(pos, pos+30).toString('hex'));
} else {
    console.log('NOT FOUND');
}
