# Casos de Test de API REST: HTTP y Seguridad — Companion

Companion ejecutable de [Casos de Test de API REST: HTTP y Seguridad](https://qapractices.com/es/test-cases/rest-api-test-cases/).

## Contenido

| Archivo | Herramienta | Qué cubre |
|---|---|---|
| `test_rest_api.py` | pytest 8.3 + requests 2.32 | TC-001, TC-002, TC-003, TC-006, TC-007, TC-008, TC-011, TC-013, TC-015 |
| `rest-api-contract.feature` | Gherkin | Escenarios del contrato: recursos creados, PUT idempotente, 404, JSON malformado, 401, BOLA, 429 |
| `postman-collection.json` | Postman / Newman | Colección importable con scripts de test para los casos centrales |

## Setup

```bash
pip install pytest requests
export API_BASE_URL="https://your-api.example.com/api/v1"
export API_TOKEN="your-test-token"
```

## Ejecutar

```bash
pytest test_rest_api.py -v
newman run postman-collection.json
```

Define `API_RATE_LIMIT` para activar el test de limitación de velocidad (se salta si no está). Apunta `API_BASE_URL` a tu entorno — `api.example.com` es un placeholder.
