# Docker Commands for Testers — Companion

Runnable files from the [Docker Commands Cheat Sheet for Testers](https://qapractices.com/documentation/docker-commands-testing-cheat-sheet/) on QAPractices.com.

## Contents

| File | What it is |
|---|---|
| `src/docker-compose.test.yml` | Test stack: app + Postgres 16 with healthcheck + Selenium Chrome |
| `src/Dockerfile.test` | Multi-stage build that produces a test-runner image |
| `src/spin-up-test-env.sh` | Disposable Postgres with a `pg_isready` wait loop — no fixed sleeps |
| `src/cleanup.sh` | Removes test containers and images by name/reference filter |

## Usage

```bash
chmod +x src/*.sh
./src/spin-up-test-env.sh          # Postgres ready on :5432
docker compose -f src/docker-compose.test.yml up -d
./src/cleanup.sh                    # wipe test resources
```
