# API Integration Tests — Companion

Runnable companion for [How to Write API Integration Tests](https://qapractices.com/documentation/how-to-write-api-integration-tests/) ([versión en español](https://qapractices.com/es/documentation/how-to-write-api-integration-tests/)).

## What's inside

- `js/` — a minimal Express 5 app with in-memory stores plus a Jest 30 + supertest 7 suite covering the CRUD chain, token auth, per-test data, contract assertions, request chaining and error paths from the guide.
- `python/` — a FastAPI app plus a pytest 8 suite with the same CRUD flow through `TestClient` and a `yield` fixture for setup/teardown.
- `ci/` — a GitHub Actions workflow with a Postgres 16 service and `pg_isready` health checks, matching the CI section of the guide.

## Run the JavaScript suite

Requires Node 20+.

```bash
cd js
npm install
npm test
```

The in-memory auth accepts any non-empty password for the seeded test users (`test.user@test.dev`, `buyer@test.dev`, `admin@test.dev`), so `TEST_USER_PASSWORD` and `TEST_ADMIN_PASSWORD` can be set to anything or left unset.

## Run the Python suite

Requires Python 3.10+.

```bash
cd python
pip install -r requirements.txt
pytest
```

## Notes

The apps keep all state in memory — restart the process and the data resets. That's the point: each test run starts from a clean store, the same guarantee the guide asks from a dedicated test database.
