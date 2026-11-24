# Troubleshooting de API Testing — Snippets complementarios

Código ejecutable de la [Guía de Troubleshooting de API Testing](https://qapractices.com/es/documentation/api-testing-troubleshooting/).

| Archivo | Propósito | Herramienta |
|---|---|---|
| `test-isolation.js` | Cada test crea y limpia sus propios datos (corrige tests flaky por estado) | supertest 7 |
| `schema-validation.js` | Valida una respuesta de pago contra el schema JSON derivado de OpenAPI | Ajv 8 |
| `k6-perf-test.js` | Test de carga con umbrales de SLA (p95 < 200ms, p99 < 500ms) | k6 0.54 |

## Uso

```bash
# Ejemplos Jest / Vitest
npm i supertest@7 ajv@8
npx jest test-isolation.js

# k6
k6 run -e API_TOKEN=tu-token k6-perf-test.js
```
