# Chat Messaging Feature Test Cases — Companion

Runnable companion for the [Chat and Messaging Feature Test Cases](https://qapractices.com/test-cases/chat-messaging-feature-test-cases/) on QAPractices.

Covers the real-time assertions that are awkward to script from the checklist alone: WebSocket send/receive round-trip with a deduplication check (TC001/TC025), typing-indicator timeout (TC004), and the REST endpoints used in the Example Commands section.

## Files

- `delivery-assertions.mjs` — Node 20 script using `ws` (no other deps): connects two clients, asserts message arrives ≤1s, asserts typing indicator clears within 5s of idle, verifies no duplicate delivery after a forced reconnect. Point it at a staging endpoint: `node delivery-assertions.mjs --url wss://ws.staging.example.com/v1`.
- `send-message.sh` — curl examples for the REST API calls: send message, fetch history with pagination, mark as read.
- `package.json` — declares `ws` dependency.

## Run

```bash
npm install
WS_URL=wss://ws.staging.example.com/v1 TOKEN=$API_TOKEN node delivery-assertions.mjs
```

Requires Node 20+ and a staging environment with seeded users — see the test cases for the preconditions each assertion maps to.
