# Checklist de Readiness para Deploy — Scripts Companion

> Repositorio companion para el [Checklist de Readiness para Deploy: Go-Live](https://qapractices.com/es/checklists/deployment-readiness-checklist) en QAPractices.com.

## Qué incluye

- **Scripts de verificación** para los gates de deployment readiness
- **Scripts en Bash y Python** para env vars, smoke tests y tráfico canary

## Scripts

| Script | Lenguaje | Propósito |
| --- | --- | --- |
| `scripts/check-env-vars.sh` | Bash | Verificar que todas las variables de entorno requeridas estén seteadas antes del deploy |
| `scripts/post-deploy-smoke-test.py` | Python | Check de health endpoint y versión después del deploy |
| `scripts/check-canary-traffic.sh` | Bash | Verificar que el tráfico canary esté dentro del rango esperado (1-10%) |

## Requisitos

| Herramienta | Versión |
| --- | --- |
| Bash | 5.0+ |
| Python | 3.10+ |
| requests | 2.31+ |
| jq | 1.6+ |
| curl | cualquiera |

## Uso

```bash
# Verificar variables de entorno
chmod +x scripts/check-env-vars.sh
./scripts/check-env-vars.sh

# Smoke test post-deploy
pip install requests
python scripts/post-deploy-smoke-test.py

# Verificación de tráfico canary
chmod +x scripts/check-canary-traffic.sh
./scripts/check-canary-traffic.sh
```

## Recursos relacionados

- [Checklist de Readiness para Deploy](https://qapractices.com/es/checklists/deployment-readiness-checklist)
- [Checklist de Pruebas de Release](https://qapractices.com/es/checklists/release-testing-checklist)
- [Checklist de Despliegue sin Tiempo de Inactividad](https://qapractices.com/es/checklists/zero-downtime-deployment-checklist)
- [Checklist de Verificación Post-Deploy](https://qapractices.com/es/checklists/post-deployment-verification-checklist)

## Licencia

MIT
