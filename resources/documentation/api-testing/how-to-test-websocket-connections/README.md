# How to Test WebSocket Connections — Runnable Companion

Runnable lab for the QAPractices guide [How to Test WebSocket Connections](https://qapractices.com/documentation/how-to-test-websocket-connections/). Covers the whole lifecycle: connect, echo/broadcast exchange, close codes, malformed payloads, reconnect and a k6 load run.

## Setup

```bash
npm install   # ws 8.x + jest 29
npm start     # server on ws://localhost:8080/ws
npm test      # jest suite (6 cases)
k6 run k6-load.js   # optional: 100-VU load check
```

## What's inside

- `server.js` — `ws` 8.x echo/broadcast/ping server; replies `error` on invalid JSON.
- `tests/client.test.js` — subscribe ack, echo, broadcast to a second client, close code 1000, malformed payload, reconnect.
- `k6-load.js` — handshake `101` + pong round-trip under 100 concurrent VUs.
