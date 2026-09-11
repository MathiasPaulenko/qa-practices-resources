# API Gateway Guide — Companion

Este companion provee archivos ejecutables para la guía [Guía de API Gateway](https://qapractices.com/es/documentation/api-gateway-testing-guide).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `scripts/route_validation.sh` | Script de curl para testear rutas exact, prefix, host-based y method-restricted |
| `scripts/rate_limit_test.sh` | Script de curl para testear thresholds de rate limiting y headers de respuesta |
| `scripts/tls_validation.sh` | Script de curl para validar versiones TLS, certificados y security headers |
| `tests/k6_gateway_load_test.js` | Test de carga k6 a través del gateway con stages de ramp-up y thresholds |

## Inicio Rápido

```bash
# Correr validación de rutas
bash scripts/route_validation.sh

# Correr test de rate limit
bash scripts/rate_limit_test.sh

# Correr validación TLS
bash scripts/tls_validation.sh

# Correr test de carga k6
k6 run tests/k6_gateway_load_test.js
```