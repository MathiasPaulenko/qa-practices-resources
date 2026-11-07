# How to Test Containerized Applications — Runnable Companion

Companion for [How to Test Containerized Applications](https://qapractices.com/documentation/containerized-applications-testing/) on QAPractices.

A minimal but real gate — build the image, scan it for critical CVEs, deploy to a throwaway stack, probe it — mirroring the image → manifest → cluster order from the guide.

```text
docker-compose.test.yml                  app + postgres 17 + curl probe, healthcheck-ordered
app/Dockerfile                           node:22-alpine with HEALTHCHECK instruction
app/server.js                            /ready (liveness) and /health (db-aware readiness)
k8s/deployment.yaml                      2 replicas, probes, resource requests/limits
k8s/service.yaml                         ClusterIP service for the smoke test
scripts/smoke-k8s.sh                     namespace, apply, kubectl wait, curl pod, cleanup
.github/workflows/container-tests.yml    build → trivy scan → compose smoke
```

## Run it — Compose

```bash
docker compose -f docker-compose.test.yml up --abort-on-container-exit
docker compose -f docker-compose.test.yml down -v
```

## Run it — Kubernetes (KinD)

```bash
docker build -t app:local ./app
kind load docker-image app:local
./scripts/smoke-k8s.sh
```

## What it demonstrates

- `depends_on: condition: service_healthy` — the app waits for `pg_isready`, and the smoke container waits for the app's own `/health`.
- Split probes: `/ready` proves the process is up (liveness), `/health` proves dependencies are reachable (readiness). Without `DB_HOST` the endpoint reports healthy, which keeps the k8s smoke lean.
- Graceful shutdown: the app handles SIGTERM and closes connections before exiting — test it with `docker stop`.
- The CI gate order from the guide: scan before smoke, teardown under `if: always()`.

Requires Docker Engine 29.x with Compose v2, and KinD 0.33+ for the cluster smoke test.
