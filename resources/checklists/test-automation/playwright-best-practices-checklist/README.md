# Playwright Best Practices Checklist — Companion

Runnable scaffolding for the [Playwright Best Practices Checklist](https://qapractices.com/checklists/playwright-best-practices-checklist).

## Files

- `playwright.config.ts` — CI-aware config: `retries`/`forbidOnly`/`workers` keyed to `process.env.CI`, `trace: 'on-first-retry'`, screenshot+video on failure, env-driven `baseURL`, `testIdAttribute`, and a Chromium/WebKit/mobile project matrix behind a `setup` project that produces `storageState`.
- `fixtures.ts` — shared setup via `test.extend`: an `authedPage` fixture that skips UI login, and a `data` fixture that creates an isolated project per test through the API and cleans it up in fixture teardown.
- `github_actions_playwright.yml` — 4-way shard with `blob` reporters merged into one HTML report via `merge-reports`.

## Usage

```bash
cp playwright.config.ts <repo>/playwright.config.ts
cp fixtures.ts <repo>/tests/fixtures.ts
cp github_actions_playwright.yml <repo>/.github/workflows/playwright.yml
npm ci && npx playwright install --with-deps
npx playwright test
```

Expectations: `BASE_URL` and `API_URL` set per environment; a `*.setup.ts` project performs login once and writes `playwright/.auth/user.json`.
