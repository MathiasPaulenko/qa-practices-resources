# API Testing Checklist — Companion

Companion resource for [API Testing Checklist: 106 REST, GraphQL & Webhook Checks](https://qapractices.com/checklists/api-testing-checklist).

## Contents

- `tests/smoke_test.py` — Python smoke test with requests (Layer 1)
- `tests/json_schema_validation.py` — JSON Schema validation for REST responses
- `scripts/curl_contract_check.sh` — curl contract check for GET endpoints
- `tests/k6_load_smoke.js` — k6 load smoke test (10 VUs, 30s)
- `tests/graphql_playwright_test.ts` — GraphQL query and mutation with Playwright
- `server/apollo_depth_complexity.js` — Apollo Server depth and complexity limits
- `requirements.txt` — Python dependencies
- `package.json` — Node.js dependencies

## Requirements

- Python 3.12+ with requests 2.32 and jsonschema 4.23
- Node.js 20+ with Playwright 1.48
- k6 0.53
- curl

## Usage

```bash
# Python smoke tests
pip install -r requirements.txt
python tests/smoke_test.py

# JSON Schema validation
python tests/json_schema_validation.py

# curl contract check
bash scripts/curl_contract_check.sh

# k6 load test
k6 run tests/k6_load_smoke.js

# GraphQL Playwright test
npx playwright test tests/graphql_playwright_test.ts

# Apollo Server depth/complexity (requires typeDefs and resolvers)
node server/apollo_depth_complexity.js
```

## Versions

- Python: 3.12+
- requests: 2.32
- jsonschema: 4.23
- k6: 0.53
- Playwright: 1.48
- Apollo Server: 4.x
- graphql-depth-limit: 1.1
- graphql-validation-complexity: 0.4
