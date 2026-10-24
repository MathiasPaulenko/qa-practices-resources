# Integration Testing Test Cases

> Runnable examples for [Integration Testing Test Cases](https://qapractices.com/test-cases/integration-testing-test-cases).

This companion contains executable examples covering the most common integration scenarios: API-to-database writes, service-to-service calls, and an end-to-end order flow with side-effect assertions.

## Files

- `docker-compose.yml` — App plus Postgres for local integration runs.
- `scripts/test_api_db_integration.py` — pytest + requests: POST via API, verify the row in the database (TC-001).
- `scripts/test_order_flow.spec.ts` — Playwright test: order flow asserting inventory state on both sides of the seam (TC-009).

## How to use

1. `docker compose up -d` to start the app and database.
2. `pytest scripts/test_api_db_integration.py -v` for the API-to-database check.
3. `npx playwright test scripts/test_order_flow.spec.ts` for the E2E order flow (needs Playwright 1.48+ and a running app at `BASE_URL`).

## Requirements

- Docker + Docker Compose
- Python 3.10+ with `pytest` and `requests` 2.x
- Node.js 18+ with `@playwright/test` 1.48+
