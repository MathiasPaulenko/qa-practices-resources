# Checklist de Pruebas de API — Companion

Recurso companion para [Checklist de Pruebas de API: 106 Checks REST, GraphQL y Webhooks](https://qapractices.com/es/checklists/api-testing-checklist).

## Contenido

- `tests/smoke_test.py` — Smoke test en Python con requests (Capa 1)
- `tests/json_schema_validation.py` — Validación de JSON Schema para respuestas REST
- `scripts/curl_contract_check.sh` — Verificación de contrato con curl para endpoints GET
- `tests/k6_load_smoke.js` — Prueba de carga con k6 (10 VUs, 30s)
- `tests/graphql_playwright_test.ts` — Query y mutation GraphQL con Playwright
- `server/apollo_depth_complexity.js` — Límites de profundidad y complejidad en Apollo Server
- `requirements.txt` — Dependencias de Python
- `package.json` — Dependencias de Node.js

## Requisitos

- Python 3.12+ con requests 2.32 y jsonschema 4.23
- Node.js 20+ con Playwright 1.48
- k6 0.53
- curl

## Uso

```bash
# Smoke tests en Python
pip install -r requirements.txt
python tests/smoke_test.py

# Validación de JSON Schema
python tests/json_schema_validation.py

# Verificación de contrato con curl
bash scripts/curl_contract_check.sh

# Load test con k6
k6 run tests/k6_load_smoke.js

# Test de GraphQL con Playwright
npx playwright test tests/graphql_playwright_test.ts

# Apollo Server depth/complexity (requiere typeDefs y resolvers)
node server/apollo_depth_complexity.js
```

## Versiones

- Python: 3.12+
- requests: 2.32
- jsonschema: 4.23
- k6: 0.53
- Playwright: 1.48
- Apollo Server: 4.x
- graphql-depth-limit: 1.1
- graphql-validation-complexity: 0.4
