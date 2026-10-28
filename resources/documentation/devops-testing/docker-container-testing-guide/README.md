# Docker Container Testing Guide — Runnable Companion

Companion for the [Docker Container Testing Guide](https://qapractices.com/documentation/docker-container-testing-guide/) on QAPractices.

A minimal Compose v2 test stack: Postgres 15 with a real `pg_isready` healthcheck, plus a Node 20 app under test whose `/health` endpoint only reports healthy when the database is reachable — the dependency-aware health check pattern from the guide.

```text
docker-compose.test.yml   the stack (healthchecks + service_healthy + resource limits)
app/Dockerfile            node:20-alpine, HEALTHCHECK instruction
app/server.js             /health (db-aware) and /ready (liveness) endpoints
scripts/verify-stack.sh   walks the seven testing areas from the guide
```

## Run it

```bash
docker compose -f docker-compose.test.yml up -d
./scripts/verify-stack.sh
docker compose -f docker-compose.test.yml down -v
```

## What it demonstrates

- `depends_on: condition: service_healthy` — the app waits for `pg_isready`, not just for the container to start.
- Real vs fake health: `/health` checks the DB connection; `/ready` only proves the process is up. Compare both against the guide's "false-positive guard" row.
- Resource limits: `memory: 512M`, `cpus: "1.0"` — trigger OOM with a load script to verify the §6 table.
- No `--link`, no `latest` tag: user-defined network + pinned `postgres:15`.

Requires Docker Engine 29.x and Compose v2.
