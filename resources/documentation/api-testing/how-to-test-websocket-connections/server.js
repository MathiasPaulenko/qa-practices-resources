// Minimal WebSocket test server: ping/pong, echo, broadcast.
// ws 8.x — same behaviors the guide tests exercise.
const { WebSocketServer } = require('ws');

const wss = new WebSocketServer({ port: 8080, path: '/ws' });

wss.on('connection', (socket) => {
  socket.on('message', (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw);
    } catch {
      socket.send(JSON.stringify({ type: 'error', reason: 'invalid JSON' }));
      return;
    }

    if (msg.type === 'ping') {
      socket.send(JSON.stringify({ type: 'pong', message: msg.message }));
    } else if (msg.type === 'echo') {
      socket.send(JSON.stringify({ type: 'echo', text: msg.text }));
    } else if (msg.type === 'subscribe') {
      socket.send(JSON.stringify({ type: 'subscribed', channel: msg.channel }));
    } else if (msg.type === 'broadcast') {
      wss.clients.forEach((client) => {
        if (client !== socket && client.readyState === 1) {
          client.send(JSON.stringify({ type: 'broadcast', text: msg.text }));
        }
      });
      socket.send(JSON.stringify({ type: 'broadcast-ack' }));
    } else {
      socket.send(JSON.stringify({ type: 'error', reason: 'unknown type' }));
    }
  });
});

console.log('WebSocket test server on ws://localhost:8080/ws');
