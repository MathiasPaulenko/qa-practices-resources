# Cómo Probar Aplicaciones Containerizadas — Companion Ejecutable

Companion de [Cómo Probar Aplicaciones Containerizadas](https://qapractices.com/es/documentation/containerized-applications-testing/) en QAPractices.

Una puerta mínima pero real — compilar la imagen, escanearla por CVEs críticos, desplegar a un stack descartable, probarla — que sigue el orden imagen → manifiesto → cluster de la guía.

```text
docker-compose.test.yml                  app + postgres 17 + probe curl, ordenado por healthcheck
app/Dockerfile                           node:22-alpine con instrucción HEALTHCHECK
app/server.js                            /ready (liveness) y /health (readiness sensible a db)
k8s/deployment.yaml                      2 réplicas, probes, requests/limits de recursos
k8s/service.yaml                         service ClusterIP para el smoke test
scripts/smoke-k8s.sh                     namespace, apply, kubectl wait, pod curl, limpieza
.github/workflows/container-tests.yml    build → escaneo trivy → smoke compose
```

## Correrlo — Compose

```bash
docker compose -f docker-compose.test.yml up --abort-on-container-exit
docker compose -f docker-compose.test.yml down -v
```

## Correrlo — Kubernetes (KinD)

```bash
docker build -t app:local ./app
kind load docker-image app:local
./scripts/smoke-k8s.sh
```

## Qué demuestra

- `depends_on: condition: service_healthy` — la app espera a `pg_isready`, y el contenedor smoke espera al `/health` de la propia app.
- Probes separados: `/ready` prueba que el proceso está arriba (liveness), `/health` prueba que las dependencias responden (readiness). Sin `DB_HOST` el endpoint reporta healthy, lo que mantiene liviano el smoke de k8s.
- Cierre prolijo: la app maneja SIGTERM y cierra conexiones antes de salir — probalo con `docker stop`.
- El orden de la puerta de CI de la guía: escaneo antes del smoke, teardown con `if: always()`.

Requiere Docker Engine 29.x con Compose v2, y KinD 0.33+ para el smoke test de cluster.
