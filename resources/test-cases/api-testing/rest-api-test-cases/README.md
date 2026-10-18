# REST API Test Cases: HTTP & Security — Companion

Runnable companion for [REST API Test Cases: HTTP & Security](https://qapractices.com/test-cases/rest-api-test-cases/).

## Contents

| File | Tool | What it covers |
|---|---|---|
| `test_rest_api.py` | pytest 8.3 + requests 2.32 | TC-001, TC-002, TC-003, TC-006, TC-007, TC-008, TC-011, TC-013, TC-015 |
| `rest-api-contract.feature` | Gherkin | Contract scenarios: created resources, idempotent PUT, 404, malformed JSON, 401, BOLA, 429 |
| `postman-collection.json` | Postman / Newman | Importable collection with test scripts for the core cases |

## Setup

```bash
pip install pytest requests
export API_BASE_URL="https://your-api.example.com/api/v1"
export API_TOKEN="your-test-token"
```

## Run

```bash
pytest test_rest_api.py -v
newman run postman-collection.json
```

Set `API_RATE_LIMIT` to enable the rate-limit test (it skips otherwise).
Point `API_BASE_URL` at your environment — `api.example.com` is a placeholder.
