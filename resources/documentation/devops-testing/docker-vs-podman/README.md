# Docker vs Podman — Companion

Runnable files from the guide [Docker vs Podman: Container Tools](https://qapractices.com/documentation/docker-vs-podman/).

## Files

- `src/docker-compose.test.yml` — app + Postgres 15 test stack with a health check; runs on `docker compose` and (with caveats) `podman-compose` 1.x.
- `src/Containerfile` — minimal image for the app under test; builds identically with `docker build` and `podman build`.
- `src/qa-stack-pod.yaml` — Kubernetes-style pod manifest (Postgres + app) for `podman kube play`.
- `src/start-podman-pod.sh` — creates the QA pod, waits for Postgres, prints teardown commands.
- `src/ci-podman-tests.yml` — GitHub Actions workflow that runs the stack rootless on Podman.

## Usage — Docker

```bash
docker compose -f src/docker-compose.test.yml up -d
docker compose -f src/docker-compose.test.yml down -v
```

## Usage — Podman

```bash
chmod +x src/start-podman-pod.sh
./src/start-podman-pod.sh
```

Or replay the pod manifest directly:

```bash
podman kube play src/qa-stack-pod.yaml
podman pod rm -f qa-stack
```

On Podman 4.x the equivalent legacy commands are `podman generate kube` / `podman play kube`.
