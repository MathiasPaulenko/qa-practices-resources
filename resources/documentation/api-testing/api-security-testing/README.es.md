# Guía de Testing de Seguridad en APIs — Companion

Este companion contiene archivos ejecutables para la guía [Testing de Seguridad en APIs: OWASP Top 10](https://qapractices.com/es/documentation/api-security-testing).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `scripts/bola-idor-test.sh` | Sonda BOLA/IDOR: repite una petición con otro ID de recurso, espera 403/404 |
| `scripts/jwt-tampering-test.sh` | Envía un token con payload alterado/firma inválida, espera 401 |
| `scripts/rate-limit-probe.sh` | Lanza 100 peticiones rápidas, espera 429 + Retry-After tras el umbral |
| `scripts/zap-baseline.sh` | Ejecuta el escaneo baseline de OWASP ZAP 2.15 en Docker y genera un informe HTML |

## Inicio rápido

```bash
# Configura el entorno primero — nunca ejecutar contra producción
export BASE_URL="https://staging.example.com"
export USER_A_TOKEN="<token-de-usuario-de-prueba>"
export TAMPERED_TOKEN="<token-alterado>"

bash scripts/bola-idor-test.sh
bash scripts/jwt-tampering-test.sh
bash scripts/rate-limit-probe.sh
bash scripts/zap-baseline.sh
```

## Integración CI

Ejecuta `bola-idor-test.sh` y `jwt-tampering-test.sh` en cada deploy a staging; son rápidos y deterministas. Deja `rate-limit-probe.sh` y `zap-baseline.sh` para ejecuciones nocturnas — son ruidosos y más lentos.
