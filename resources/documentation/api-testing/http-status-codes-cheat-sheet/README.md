# HTTP Status Codes Cheat Sheet — Companion

Runnable files for the [HTTP Status Codes Cheat Sheet for Testers](https://qapractices.com/documentation/http-status-codes-cheat-sheet) guide.

## Files

| File | Purpose |
|------|---------|
| `data/status-code-matrix.csv` | Ready-to-import negative/positive status code matrix (12 scenarios) |
| `tests/test_status_codes.py` | pytest + requests 2.32 contract tests covering 200/201/204/401/403/404/405/422/429 |
| `postman/status-code-assertions.js` | Postman v11 / Newman 6.x Tests-tab snippets per expected code |
| `java/StatusCodeMatrixTest.java` | REST Assured 5.5 + JUnit 5 examples for the same matrix |

## Quick Start

```bash
# Python contract tests (Python 3.10+, pytest 8.x, requests 2.32)
pip install requests pytest
BASE_URL=https://staging.qapractices.com pytest tests/test_status_codes.py -v

# Postman snippets: paste into the Tests tab of each request,
# or run the collection with Newman 6.x
newman run your-collection.json --environment staging.json

# REST Assured (Maven/Gradle project with io.rest-assured:rest-assured:5.5.x)
mvn test -Dtest=StatusCodeMatrixTest -DBASE_URL=https://staging.qapractices.com
```

The CSV matrix can be imported into a test management tool or used as
data-driven input for the pytest file.

## Notes

- Point `BASE_URL` at a staging environment or a mock server
  (WireMock, Mockoon, Prism) — the tests assume a `/users` CRUD API.
- `test_rate_limit_returns_429_with_retry_after` is inherently
  environment-dependent; tune the request count to your real limit.
