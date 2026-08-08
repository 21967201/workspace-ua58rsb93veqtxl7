// 测试 qclaw_launcher 8642 的 WebSocket API
const http = require('http');
const net = require('net');

// 先试 HTTP 路由
const paths = ['/api/ws', '/api/jobs', '/api/health', '/api/state', '/api/sessions', '/api/agent', '/api/agents', '/api/hermes', '/api/chat', '/api/conversations', '/api/history'];
function tryHttp(path) {
  return new Promise((resolve) => {
    const req = http.request({
      host: '127.0.0.1',
      port: 8642,
      path: path,
      method: 'GET',
      timeout: 3000
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(`${path} → ${res.statusCode}: ${data.slice(0, 200)}`));
    });
    req.on('error', e => resolve(`${path} → ERR: ${e.message}`));
    req.on('timeout', () => { req.destroy(); resolve(`${path} → TIMEOUT`); });
    req.end();
  });
}

(async () => {
  for (const p of paths) {
    console.log(await tryHttp(p));
  }
})();
