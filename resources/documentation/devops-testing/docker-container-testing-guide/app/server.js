// Minimal health endpoint for the compose test stack.
// /health returns 200 only when the db dependency is reachable;
// /ready returns 200 when the process is up regardless of deps.
const http = require('http');
const net = require('net');

const dbReady = () =>
  new Promise((resolve) => {
    const s = net.connect(5432, process.env.DB_HOST || 'db');
    s.on('connect', () => { s.end(); resolve(true); });
    s.on('error', () => { s.destroy(); resolve(false); });
    s.setTimeout(2000, () => { s.destroy(); resolve(false); });
  });

http.createServer(async (req, res) => {
  if (req.url === '/ready') {
    res.writeHead(200).end('ready');
    return;
  }
  if (req.url === '/health') {
    const ok = await dbReady();
    res.writeHead(ok ? 200 : 503).end(ok ? 'healthy' : 'unhealthy: db unreachable');
    return;
  }
  res.writeHead(404).end();
}).listen(8080);
