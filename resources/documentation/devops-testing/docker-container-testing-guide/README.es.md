# Guía de Testing de Contenedores Docker — Companion ejecutable

Companion de la [Guía de Testing de Contenedores Docker](https://qapractices.com/es/documentation/docker-container-testing-guide/) en QAPractices.

Un stack mínimo con Compose v2: Postgres 15 con un `pg_isready` real como healthcheck, más una app Node 20 cuyo `/health` solo reporta healthy cuando la base responde — el patrón de health check consciente de dependencias de la guía.

```text
docker-compose.test.yml   el stack (healthchecks + service_healthy + límites)
app/Dockerfile            node:20-alpine, instrucción HEALTHCHECK
app/server.js             endpoints /health (db-aware) y /ready (liveness)
scripts/verify-stack.sh   recorre las siete áreas de testing de la guía
```

## Ejecución

```bash
docker compose -f docker-compose.test.yml up -d
./scripts/verify-stack.sh
docker compose -f docker-compose.test.yml down -v
```

## Qué demuestra

- `depends_on: condition: service_healthy` — la app espera a `pg_isready`, no solo a que el contenedor arranque.
- Salud real vs. fingida: `/health` chequea la conexión a la DB; `/ready` solo prueba que el proceso vive. Comparalos con la fila "guarda de falsos positivos".
- Límites de recursos: `memory: 512M`, `cpus: "1.0"` — dispará OOM con un script de carga para verificar la tabla de la §6.
- Sin `--link` ni tag `latest`: red definida por el usuario + `postgres:15` pineado.

Requiere Docker Engine 29.x y Compose v2.
