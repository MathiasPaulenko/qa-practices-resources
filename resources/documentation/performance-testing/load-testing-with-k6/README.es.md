# Companion de Load Testing con k6

Scripts de load testing ejecutables con k6 v0.56 para la [guía de Load Testing con k6](https://qapractices.com/es/documentation/load-testing-with-k6/).

## Requisitos

- [k6 v0.56](https://k6.io/docs/get-started/installation/) o superior
- Node.js 18+ (para scripts de pre-procesamiento)
- Una API de staging contra la que testear

## Archivos

| Archivo | Descripción |
| --- | --- |
| `api-load.js` | Script principal de load test con flujo de login + búsqueda de órdenes, métricas custom y thresholds |
| `smoke-test.js` | Smoke test corto y con poca carga (5 VUs, 1 min) |
| `stress-test.js` | Ramp 0 a 400 VUs para encontrar el punto de ruptura |
| `spike-test.js` | Salto a 1000 VUs en 10s, sostener 1 min, bajar |
| `soak-test.js` | 100 rps por 4 horas para detectar memory leaks |
| `data/users.json` | Datos de ejemplo de usuarios para requests parametrizados |
| `.github/workflows/k6-load.yml` | Workflow de GitHub Actions para integración CI |

## Inicio rápido

```bash
# Instalar k6 (macOS)
brew install k6

# Instalar k6 (Windows)
choco install k6

# Ejecutar el load test principal
k6 run api-load.js

# Ejecutar contra otro entorno
BASE_URL=https://staging-02.qapractices.com/api/v1 k6 run api-load.js

# Ejecutar smoke test
k6 run smoke-test.js

# Ejecutar en Docker
docker run --rm -v $(pwd):/scripts -w /scripts grafana/k6:2.2.0 run api-load.js

# Ejecutar en k6 Cloud
k6 cloud run api-load.js
```

## Variables de entorno

| Variable | Default | Descripción |
| --- | --- | --- |
| `BASE_URL` | `https://staging.qapractices.com/api/v1` | URL base de la API target |
| `USER` | `qa-load@qapractices.com` | Email de login |
| `PASS` | `Str0ngP@ss!` | Password de login |
| `API_TOKEN` | (none) | Token pre-generado para el script de métricas custom |

## CI/CD

El workflow de GitHub Actions incluido corre un smoke test en cada push a `main` y los días hábiles a las 5 AM UTC. Ver `.github/workflows/k6-load.yml`.

## Origen

Este companion es parte del recurso de [QAPractices](https://qapractices.com): [Load Testing con k6: Escenarios, Métricas y k6 Cloud](https://qapractices.com/es/documentation/load-testing-with-k6/).
