# Playwright Test Fixture Template — Companion Resources

Runnable companion files for the [Playwright Test Fixture Template](https://qapractices.com/templates/playwright-test-fixture-template/) on QAPractices.com.

## Contents

| File | Description |
| --- | --- |
| `fixtures/base.fixture.ts` | Base fixture: `testUser`, `apiContext` (authenticated request context) and `cleanDb` teardown. |
| `fixtures/data.fixture.ts` | Test data fixtures (`testProduct`, `createdOrder`) seeded via API with teardown. |
| `fixtures/page.fixture.ts` | `DashboardPage` page-object fixture. |
| `global-setup.ts` | One-time UI login that writes `storageState` JSON for reuse across tests. |
| `auth.spec.ts` | Example spec consuming the saved storage state — zero logins per test. |
| `playwright.config.ts` | Projects, retries, reporters and `globalSetup` wiring. |

## Requirements

- `@playwright/test` 1.x (`npm install -D @playwright/test` + `npx playwright install`)
- Node.js 20 LTS
- An app under test exposing `/login` and the API endpoints referenced by the fixtures (or adapt them).

## Quick Start

1. Copy `fixtures/`, `global-setup.ts` and `playwright.config.ts` into your `tests/` tree.
2. Set `BASE_URL`, `API_BASE_URL`, `API_TOKEN`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` env vars.
3. Point the login selectors and seeding endpoints at your app.
4. Run `npx playwright test`.
