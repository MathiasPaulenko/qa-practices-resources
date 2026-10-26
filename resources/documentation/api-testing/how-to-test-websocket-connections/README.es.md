# Cómo Probar Conexiones WebSocket — Companion Ejecutable

Lab ejecutable de la guía de QAPractices [Cómo Probar Conexiones WebSocket](https://qapractices.com/es/documentation/how-to-test-websocket-connections/). Cubre el ciclo de vida completo: conexión, intercambio echo/broadcast, códigos de cierre, payloads malformados, reconexión y una corrida de carga con k6.

## Setup

```bash
npm install   # ws 8.x + jest 29
npm start     # servidor en ws://localhost:8080/ws
npm test      # suite jest (6 casos)
k6 run k6-load.js   # opcional: chequeo de carga con 100 VUs
```

## Qué incluye

- `server.js` — servidor `ws` 8.x con echo/broadcast/ping; responde `error` ante JSON inválido.
- `tests/client.test.js` — ack de subscribe, echo, broadcast a un segundo cliente, código de cierre 1000, payload malformado, reconexión.
- `k6-load.js` — handshake `101` + round-trip de pong bajo 100 VUs concurrentes.
