# API Load Testing con Postman y k6 — Companion

Este companion provee archivos ejecutables para la guía [API Load Testing con Postman y k6](https://qapractices.com/es/documentation/api-load-testing-postman-k6).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `test-plans/checkout-load.js` | Script de k6 v2.x para un flujo de checkout de e-commerce |
| `test-plans/api-collection.json` | Colección de Postman con smoke tests para endpoints de cart y checkout |
| `test-data/users.csv` | Dataset CSV con 10 usuarios de prueba para iteración con Newman |
| `test-data/users.json` | Dataset JSON para SharedArray de k6 |
| `scripts/assert-sla.py` | Script Python para asertar p95 y error rate desde la salida JSON de k6 |
| `.github/workflows/load-test.yml` | Workflow de GitHub Actions que corre k6 nocturno |

## Inicio Rápido

```bash
# Correr el load test de k6 localmente
k6 run test-plans/checkout-load.js

# Correr el smoke test de Postman con Newman
newman run test-plans/api-collection.json -d test-data/users.csv -n 100

# Asertar SLA desde la salida JSON de k6
python scripts/assert-sla.py results.json
```

## Integración CI

El workflow de GitHub Actions incluido corre el load test de k6 nocturno y sube los resultados como artifact.