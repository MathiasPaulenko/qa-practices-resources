# Best API Testing Tools — Companion

Fixtures for [Best API Testing Tools for QA Teams](https://qapractices.com/documentation/best-api-testing-tools/). The mock API runs locally; the example does not send requests to a public service.

## Contents

| File | Purpose |
|---|---|
| `decision-matrix.csv` | Shortlist by team workflow, category, fit, and trade-off |
| `scripts/mock_api.py` | Python 3.12+ standard-library API fixture on `127.0.0.1:8080` |
| `postman/api-smoke.postman_collection.json` | Postman Collection v2.1 with a health-check request and assertions |
| `postman/local.postman_environment.json` | Local `baseUrl` variable for the collection |

## Run the sample

In one terminal, start the local mock:

```bash
python3 scripts/mock_api.py
```

In another terminal, from this directory, run the collection with Newman 6.x:

```bash
npx --yes newman@6 run postman/api-smoke.postman_collection.json \
  --environment postman/local.postman_environment.json \
  --reporters cli,junit \
  --reporter-junit-export newman-api-smoke.xml
```

The collection checks `GET /v1/health` for HTTP 200 and `{"status":"ok"}`. Stop the mock with Ctrl+C. Keep real credentials in CI secrets; the fixture uses none.

Spanish guide: [README.es.md](README.es.md)
