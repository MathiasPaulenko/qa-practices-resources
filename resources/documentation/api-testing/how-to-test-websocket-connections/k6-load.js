// k6 0.5x+ WebSocket load test — 100 concurrent connections, 30s.
// Run: k6 run k6-load.js
import ws from 'k6/ws';
import { check } from 'k6';

export const options = { vus: 100, duration: '30s' };

export default function () {
  const res = ws.connect('ws://localhost:8080/ws', {}, (socket) => {
    socket.on('open', () => socket.send(JSON.stringify({ type: 'ping', message: 'k6' })));
    socket.on('message', (data) => {
      check(JSON.parse(data), { 'pong received': (m) => m.type === 'pong' });
      socket.close();
    });
    socket.on('error', (e) => console.log('error: ' + e.error()));
  });
  check(res, { 'status is 101': (r) => r && r.status === 101 });
}
