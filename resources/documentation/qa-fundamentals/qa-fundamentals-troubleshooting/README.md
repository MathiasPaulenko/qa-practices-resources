# QA Fundamentals Troubleshooting — Companion

Runnable files for the [QA Fundamentals Troubleshooting Guide](https://qapractices.com/documentation/qa-fundamentals-troubleshooting).

## Files

| File | Purpose |
|------|---------|
| `js/flaky-cart-update.spec.js` | The flaky Playwright 1.48 spec from Problem 1 — fixed-duration wait that passes locally and fails in CI |
| `js/reliable-cart-update.spec.js` | The same spec fixed — explicit wait on the expected condition instead of `waitForTimeout` |
| `docker/docker-compose.yml` | Ephemeral test environment from Problem 3 — api + postgres:16 + redis:7 with healthchecks so dependencies fail fast |
| `templates/acceptance-criteria.txt` | Given/When/Then acceptance criteria template from Problem 2, ready to drop into your story format |

## Quick Start

```bash
# Playwright 1.48 specs
npm install --save-dev @playwright/test
npx playwright test js/flaky-cart-update.spec.js js/reliable-cart-update.spec.js

# Ephemeral environment
docker compose -f docker/docker-compose.yml up --abort-on-container-exit
```

## Notes

- The flaky spec is intentionally unreliable — use it to demo the failure mode, not as a pattern to copy.
- `docker-compose.yml` expects a Dockerfile for `api` in the repo root and a `/health` endpoint on port 3000; adapt names to your services.
- `POSTGRES_DB` uses `shopwave_test` as a placeholder database name.
