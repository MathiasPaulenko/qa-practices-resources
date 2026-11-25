# QA Fundamentals Troubleshooting — Companion

Archivos ejecutables para la [Guía de Troubleshooting de Fundamentos de QA](https://qapractices.com/es/documentation/qa-fundamentals-troubleshooting).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `js/flaky-cart-update.spec.js` | El spec flaky de Playwright 1.48 del Problema 1 — wait de duración fija que pasa en local y falla en CI |
| `js/reliable-cart-update.spec.js` | El mismo spec corregido — wait explícito sobre la condición esperada en lugar de `waitForTimeout` |
| `docker/docker-compose.yml` | Entorno de pruebas efímero del Problema 3 — api + postgres:16 + redis:7 con healthchecks para que las dependencias fallen rápido |
| `templates/acceptance-criteria.txt` | Plantilla de acceptance criteria Given/When/Then del Problema 2, lista para tu formato de story |

## Quick Start

```bash
# Specs de Playwright 1.48
npm install --save-dev @playwright/test
npx playwright test js/flaky-cart-update.spec.js js/reliable-cart-update.spec.js

# Entorno efímero
docker compose -f docker/docker-compose.yml up --abort-on-container-exit
```

## Notas

- El spec flaky es intencionalmente poco confiable — úsalo para demostrar el modo de fallo, no como patrón a copiar.
- `docker-compose.yml` espera un Dockerfile para `api` en la raíz del repo y un endpoint `/health` en el puerto 3000; adapta los nombres a tus servicios.
- `POSTGRES_DB` usa `shopwave_test` como nombre de base de datos de ejemplo.
