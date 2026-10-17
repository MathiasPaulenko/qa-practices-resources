# API Mock Server Setup Template — Companion Files

Runnable companion for the [API Mock Server Setup Template](https://qapractices.com/templates/api-mock-server-setup-template). Includes WireMock 3.13.2 stub mappings, a Docker Compose setup and MSW 2.x handlers covering the sample `/users` endpoints plus a fault-injection scenario.

## Files

| File | Purpose |
| --- | --- |
| `docker-compose.yml` | WireMock 3.13.2 standalone container on port 3001 with volume-mounted mappings. |
| `mappings/get-user-by-id.json` | `GET /users/{id}` happy path (200) using a URL path pattern. |
| `mappings/get-user-404.json` | `GET /users/99999` returns 404 with an error body. |
| `mappings/post-users.json` | `POST /users` returns 201 with `fixedDelayMs` latency simulation. |
| `mappings/get-users-rate-limited.json` | `GET /users` with `X-Simulate-Latency` header returns a 5-second slow response (fault injection example). |
| `msw/handlers.js` | MSW 2.x handlers for the same endpoints, for Node/browser test suites. |

## Usage

```bash
# Start the WireMock mock server (requires Docker)
docker compose up -d

# Verify endpoints
curl -i http://localhost:3001/users/1      # 200 + user JSON
curl -i http://localhost:3001/users/99999  # 404 + error body
curl -i -X POST http://localhost:3001/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@example.com","role":"user"}'   # 201 after ~100 ms
curl -i -H "X-Simulate-Latency: 5000" http://localhost:3001/users # 200 after ~5 s

# Stop
docker compose down
```

For MSW, import `msw/handlers.js` in your test setup and start the worker/server (`setupWorker` in the browser, `setupServer` in Node — see `msw` 2.x docs).

## Requirements

- Docker Desktop (WireMock 3.13.2 image)
- `msw` 2.x for the frontend handlers
