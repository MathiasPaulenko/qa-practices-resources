// WebSocket delivery assertions — Node 20+, dependency: ws
// Usage: WS_URL=wss://ws.staging.example.com/v1 TOKEN=xxx node delivery-assertions.mjs
import WebSocket from 'ws';

const WS_URL = process.env.WS_URL || 'ws://localhost:3001/v1';
const TOKEN = process.env.TOKEN || 'dev-token';
const CONV = process.env.CONV_ID || 'CONV-5001';

const connect = (name) => new WebSocket(WS_URL, { headers: { Authorization: `Bearer ${TOKEN}` } });
const next = (ws, type, timeout = 5000) => new Promise((resolve, reject) => {
  const timer = setTimeout(() => reject(new Error(`timeout waiting ${type}`)), timeout);
  const onMsg = (raw) => {
    const ev = JSON.parse(raw.toString());
    if (ev.type === type) { clearTimeout(timer); ws.off('message', onMsg); resolve(ev); }
  };
  ws.on('message', onMsg);
});
const send = (ws, ev) => ws.send(JSON.stringify(ev));
const open = (ws) => new Promise((r) => ws.on('open', r));

async function main() {
  const results = [];
  const check = (name, ok, detail) => { results.push({ name, ok, detail }); console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ' — ' + detail : ''}`); };

  const alice = connect('alice'), bob = connect('bob');
  await Promise.all([open(alice), open(bob)]);

  // TC001: send → received ≤1s
  const msgId = `m-${Date.now()}`;
  const recv = next(bob, 'message');
  send(alice, { type: 'message', id: msgId, conversation: CONV, text: 'hello from alice' });
  const t0 = Date.now();
  const ev = await recv;
  check('TC001 message delivered ≤1s', Date.now() - t0 <= 1000 && ev.id === msgId, `${Date.now() - t0}ms`);

  // TC025: reconnect → no duplicate delivery
  let dup = 0;
  bob.on('message', (raw) => { const e = JSON.parse(raw.toString()); if (e.type === 'message' && e.id === msgId) dup++; });
  await send(bob, { type: 'reconnect' }).catch(() => {});
  await new Promise((r) => setTimeout(r, 2000));
  check('TC025 no duplicate after reconnect', dup === 0, `dups=${dup}`);

  // TC004: typing indicator clears ≤5s after last keystroke
  send(alice, { type: 'typing', conversation: CONV });
  await next(bob, 'typing');
  const cleared = await next(bob, 'typing_stop', 6000).catch(() => null);
  check('TC004 typing clears after idle', cleared !== null);

  alice.close(); bob.close();
  const fails = results.filter((r) => !r.ok).length;
  console.log(`\n${results.length - fails}/${results.length} assertions passed`);
  process.exit(fails ? 1 : 0);
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(2); });
