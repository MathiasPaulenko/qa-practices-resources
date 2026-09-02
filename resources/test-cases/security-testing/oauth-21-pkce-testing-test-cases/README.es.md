# Casos de Test de OAuth 2.1 y PKCE — Companion

> Framework de pytest para el recurso [Casos de Test de OAuth 2.1 y PKCE](https://qapractices.com/es/test-cases/oauth-21-pkce-testing-test-cases/) en QAPractices.com

## Qué incluye

- `pkce_utils.py` — Generación de pares PKCE (S256 y plain para tests negativos)
- `mock_auth_server.py` — Mock en memoria de un servidor de autorización OAuth 2.1 con enforcement de S256, ciclo de vida de codes, rotación de refresh y validación de scope
- `conftest.py` — Fixtures de pytest para todos los casos de test
- `test_oauth_pkce.py` — TC-01 a TC-10 como tests de pytest parametrizados

## Inicio rápido

```bash
pip install pytest 8.3
pytest test_oauth_pkce.py -v
```

## Casos de test

| Test | Descripción |
| ---- | ----------- |
| TC-01 | Authorization code flow válido con PKCE S256 |
| TC-02 | `code_challenge` faltante rechazado |
| TC-03 | Método `plain` rechazado, `S256` aceptado |
| TC-04 | Verifier no coincidente rechazado |
| TC-05 | Authorization code expirado rechazado |
| TC-06 | Replay de authorization code rechazado |
| TC-07 | Validación estricta de redirect URI (trailing slash falla) |
| TC-08 | Protección CSRF con parámetro `state` |
| TC-09 | Rotación de refresh token invalida el token viejo |
| TC-10 | Enforcement de scope (scope no concedido rechazado) |

## Uso contra un servidor real

`mock_auth_server.py` es una implementación de referencia. Para testear contra un servidor de autorización real, reemplazá el mock con llamadas `requests` a los endpoints de tu servidor. La estructura de los tests es la misma.

## Requisitos

- Python 3.10+
- pytest 8.3+

## Licencia

MIT — ver [QAPractices.com](https://qapractices.com) para los términos.
