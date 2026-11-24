# Docker vs Podman — Companion

Archivos ejecutables de la guía [Docker vs Podman: Herramientas de Contenedores](https://qapractices.com/es/documentation/docker-vs-podman/).

## Archivos

- `src/docker-compose.test.yml` — stack de pruebas app + Postgres 15 con health check; corre con `docker compose` y (con matices) `podman-compose` 1.x.
- `src/Containerfile` — imagen mínima de la app bajo prueba; se construye igual con `docker build` y `podman build`.
- `src/qa-stack-pod.yaml` — manifiesto de pod estilo Kubernetes (Postgres + app) para `podman kube play`.
- `src/start-podman-pod.sh` — crea el pod de QA, espera a Postgres e imprime los comandos de limpieza.
- `src/ci-podman-tests.yml` — workflow de GitHub Actions que ejecuta el stack en Podman rootless.

## Uso — Docker

```bash
docker compose -f src/docker-compose.test.yml up -d
docker compose -f src/docker-compose.test.yml down -v
```

## Uso — Podman

```bash
chmod +x src/start-podman-pod.sh
./src/start-podman-pod.sh
```

O reproduce el manifiesto de pod directamente:

```bash
podman kube play src/qa-stack-pod.yaml
podman pod rm -f qa-stack
```

En Podman 4.x los comandos antiguos equivalentes son `podman generate kube` / `podman play kube`.
