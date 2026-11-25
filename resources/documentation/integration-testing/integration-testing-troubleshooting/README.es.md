# Troubleshooting de Integration Testing — Companion

Archivos ejecutables para la [Guía de Troubleshooting de Integration Testing](https://qapractices.com/es/documentation/integration-testing-troubleshooting).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `js/nock-salesforce-stub.js` | Stub de nock 13.x para la API de Salesforce — CI nunca toca el endpoint real |
| `js/rate-limited-caller.js` | Llamador con throttling de Bottleneck 2.x para llamadas en vivo inevitables |
| `js/transform-edge-cases.spec.js` | Specs de Jest para campos nulos, normalización UTC y entradas vacías en la capa de transformación |
| `docker/Dockerfile` | Entorno de pruebas fijado con Node 20 Alpine compartido por local, CI y staging |
| `js/oauth-token-refresh.spec.js` | Refresco de token client-credentials en el setup `beforeAll` |
| `js/parallel-safe-uuid-test.spec.js` | Datos de prueba con namespace uuid 11.x y teardown — seguros para workers en paralelo |

## Inicio Rápido

```bash
# Node 20+ con Jest 29.x
npm install --save-dev jest nock bottleneck uuid
npx jest js/transform-edge-cases.spec.js js/parallel-safe-uuid-test.spec.js

# Construir el entorno fijado
docker build -f docker/Dockerfile -t integration-tests .
```

## Notas

- `nock-salesforce-stub.js` y `rate-limited-caller.js` exportan helpers — conectalos a tus propios specs.
- `transform-edge-cases.spec.js` espera un `transform.js` que exporte `transformStripeToSalesforce`; adaptá los nombres de campos a tu mapeo.
- El spec de OAuth usa `https://auth.staging.internal/oauth/token` como placeholder — reemplazalo por el token endpoint de tu proveedor e inyectá `API_CLIENT_ID`/`API_CLIENT_SECRET` por variables de entorno.
