# APIs de Terceros

> Companion imprimible y ejemplos ejecutables de [Casos de Prueba de APIs de Terceros](https://qapractices.com/es/test-cases/third-party-api-integration-testing).

Este repositorio contiene una versión imprimible del conjunto de casos de prueba más scripts de ejemplo para adaptar a tu proyecto.

## Archivos

- `third-party-api-integration-testing.es.md` — Versión en Markdown, lista para pegar en una herramienta de test management.
- `third-party-api-integration-testing.json` — JSON estructurado con todos los casos, casos de borde y prioridades.
- `scripts/` — Scripts de ejemplo:
  - `test_auth.py` — pytest + requests para credenciales válidas e inválidas.
  - `test_rate_limit.py` — pytest + requests para headers de rate limit.
  - `test_webhook_signature.py` — Flask test client para validación de firma de webhook.
  - `wiremock_stubs.json` — Stubs de WireMock para escenarios de 503 y timeout.

## Cómo usar

1. Abrí `third-party-api-integration-testing.es.md` en tu herramienta de test management.
2. Copiá `wiremock_stubs.json` en una instancia de WireMock para simular fallos del proveedor.
3. Ejecutá `pytest scripts/test_auth.py` para testear validación de credenciales.
4. Ejecutá `pytest scripts/test_webhook_signature.py` para verificar integridad de webhooks.

## Requisitos

- Python 3.11+
- pytest 8.3+
- requests 2.32+
- Flask 3.0+
- WireMock (standalone o testcontainer)
