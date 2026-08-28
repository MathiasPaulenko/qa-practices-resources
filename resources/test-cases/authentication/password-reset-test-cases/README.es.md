# Casos de Prueba de Reset de Contraseña — Companion Ejecutable

Recurso complementario para [Casos de Prueba de Reset de Contraseña: Token y Email](https://qapractices.com/es/test-cases/password-reset-test-cases/) en QAPractices.com.

## Qué incluye

- `tests/` — Scripts de pytest 8.3 que cubren los 16 casos de prueba del recurso.
- `postman/` — Collection de Postman con los endpoints reset-request y reset-confirm, lista para correr contra un API de staging.

## Requisitos

- Python 3.10+
- pytest 8.3+
- requests 2.32+
- Un API de staging que exponga `/auth/reset-request` y `/auth/reset-confirm`
- MailHog v1.0 (o similar) para captura de emails en staging

Instalá las dependencias:

```bash
pip install -r tests/requirements.txt
```

## Ejecutar los tests

```bash
pytest tests/ -v --json-report --json-report-file=reports/report.json
```

Los tests usan la variable de entorno `BASE_URL` (default: `https://demo-api.qapractices.test`). Apuntala a tu API de staging antes de correr:

```bash
export BASE_URL=https://your-staging-api.example.com
pytest tests/ -v
```

## Collection de Postman

Importá `postman/password-reset-test-cases.postman_collection.json` en Postman v11+. La collection incluye:

- Reset request (email válido)
- Reset request (email no registrado)
- Reset confirm (token válido)
- Reset confirm (token expirado)
- Reset confirm (token reusado)
- Rate limit burst (6 requests rápidos)

## Cobertura de tests

| Script | Casos cubiertos |
| --- | --- |
| `test_reset_request.py` | TC-001, TC-006, TC-007 |
| `test_reset_confirm.py` | TC-002, TC-004, TC-005, TC-013 |
| `test_token_security.py` | TC-008, TC-009, TC-012, TC-014, TC-015 |
| `test_password_policy.py` | TC-003, TC-010 |
| `test_rate_limiting.py` | TC-011 |
| `test_audit_log.py` | TC-016 |

## Recurso relacionado

- [Casos de Prueba de Reset de Contraseña: Token y Email](https://qapractices.com/es/test-cases/password-reset-test-cases/)
- [Checklist de Pruebas de Autenticación](https://qapractices.com/es/checklists/authentication-checklist)
- [Topic de Autenticación](https://qapractices.com/es/topics/authentication)
