# Guía de Testing OWASP Top 10 2025 — Companion

> Repositorio companion para [10 Escenarios de Testing OWASP Top 10 para LumaPay 2025](https://qapractices.com/es/documentation/owasp-top-10-testing-guide-2025/)

## Requisitos

- Python 3.10+
- GitHub Actions
- Un entorno de staging con logs firmados con HMAC

## Archivos

| Archivo | Propósito |
| --- | --- |
| `security.yml` | Workflow de GitHub Actions con gates de SAST, dependency scan y container scan |
| `log_integrity_check.py` | Script de verificación de firmas HMAC para tests de logging A09 |
| `meta.json` | Metadata del recurso |
| `sample-log.txt` | Archivo de log de ejemplo con firmas HMAC para testear el script |

## Uso

### Chequeo de integridad de logs (A09)

```bash
# Seteá el secret HMAC (usá el mismo secret que tu app usa para firmar logs)
export LOG_HMAC_SECRET="your-secret-key"

# Corré el chequeo
python log_integrity_check.py evidence/batch327/a09-login.log
```

Output:

```text
Log integrity check for: evidence/batch327/a09-login.log
  Total lines: 150
  Verified:     150
  Failed:       0

  RESULT: PASS — all lines verified
```

### Workflow de GitHub Actions

Copiá `security.yml` a `.github/workflows/security.yml` en tu repositorio. El workflow corre:

- SAST con SonarQube 10.6
- Dependency scan con npm audit
- Container scan con Trivy 0.57.1

## Licencia

MIT — Mathias Paulenko
