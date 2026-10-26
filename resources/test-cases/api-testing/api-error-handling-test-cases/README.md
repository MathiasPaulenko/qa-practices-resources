# API Error Handling Test Cases — Companion

Runnable companion for [API Error Handling Test Cases: 4xx, 5xx & Contracts](https://qapractices.com/test-cases/api-error-handling-test-cases/).

## Contents

| File | Tool | What it covers |
|---|---|---|
| `test_error_handling.py` | pytest 8.3 + requests 2.32 | TC-001, TC-002, TC-006, TC-009, TC-017 — auth challenge, method `Allow`, rate-limit `Retry-After`, problem-details shape |
| `problem-details-schema.json` | jsonschema 4.x | JSON Schema for the RFC 9457 `application/problem+json` contract used by TC-017 |

## Setup

```bash
pip install pytest requests jsonschema
export API_BASE_URL="https://api.staging.example.com/api/v1"
```

`api.staging.example.com` is a placeholder — point it at your own environment. Never run the rate-limit test against a production endpoint without coordinating it first.

## Run

```bash
pytest test_error_handling.py -v
```

Set `API_BASE_URL` before running; tests skip gracefully if it is not set.
