// Minimal app for the containerized-app testing smoke suite.
// /ready returns 200 when the process is up (liveness).
// /health returns 200 only when dependencies are reachable (readiness):
// with DB_HOST set it checks a TCP connect to Postgres; without it the
// endpoint reports healthy on its own so the k8s smoke test stays lean.
const http = require('http');
const net = require('net');

const dbReady = () =>
  new Promise((resolve) => {
    if (!process.env.DB_HOST) return resolve(true);
    const s = net.connect(5432, process.env.DB_HOST);
    s.on('connect', () => { s.end(); resolve(true); });
    s.on('error', () => { s.destroy(); resolve(false); });
    s.setTimeout(2000, () => { s.destroy(); resolve(false); });
  });

const server = http.createServer(async (req, res) => {
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
});

server.listen(8080);

// Drain on SIGTERM like the guide's graceful-shutdown test expects.
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 10000).unref();
});
