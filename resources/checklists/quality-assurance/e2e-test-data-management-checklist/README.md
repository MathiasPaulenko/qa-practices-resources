# E2E Test Data Management Checklist — Runnable Companion

Companion code for the [E2E Test Data Management Checklist](https://qapractices.com/checklists/e2e-test-data-management-checklist/) on QAPractices.

## What this is

A minimal, runnable data layer for E2E suites built on the checklist's three pillars: unique creation, isolated execution, guaranteed cleanup.

| File | What it shows |
|---|---|
| `user.factory.ts` | Factory with unique-per-invocation emails (`qa-{ts}-{seq}@test.qapractices.dev`) and an API-based cleanup helper. |
| `seeded-account.fixture.ts` | Playwright 1.49 worker fixture: seeds via `request.post`, yields the account to the test, deletes it afterwards — including on failure. |
| `seed.sql` | Transactional seed for baseline data; `ON_ERROR_STOP` + `BEGIN/COMMIT` means a broken seed never leaves partial rows. Commented cleanup deletes by deterministic prefix. |
| `example.spec.ts` | A test consuming the fixture. |

## Run it

```bash
npm install -D @playwright/test@1.49
npx playwright test example.spec.ts   # against a baseURL exposing /api/accounts
psql -d e2e_staging -v ON_ERROR_STOP=1 -f seed.sql
```

Point `baseURL` in `playwright.config.ts` at a dedicated environment — never at production data.

## Design notes

- Unique data per invocation means N parallel workers never touch the same row.
- The fixture's cleanup runs after `use()` regardless of test outcome — no orphaned rows.
- The SQL seed wraps inserts in a transaction; a failed statement rolls the batch back.
