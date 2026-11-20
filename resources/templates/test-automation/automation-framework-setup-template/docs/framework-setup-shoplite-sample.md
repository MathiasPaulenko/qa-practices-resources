# Framework Setup Document — ShopLite (completed sample)

## 1. Header

| Field | Value |
|---|---|
| **Project** | ShopLite Storefront |
| **Framework codename** | shoplite-e2e |
| **Owner** | Ana Gómez, QA Lead |
| **Created / Last review** | 2026-10-02 / 2026-11-14 |
| **Status** | Active |

## 2. Scope

- **Application under test:** ShopLite web app (React SPA) plus checkout REST API
- **Test types in scope:** UI E2E smoke + regression; load and visual testing excluded (owned by the platform team)
- **Browsers / environments:** Chromium and Firefox against `staging.shoplite.internal`

## 3. Stack Decision

| Layer | Choice | Version | Rationale |
|---|---|---|---|
| Language | TypeScript | 5.4 | Team already writes TS; type-safe fixtures |
| Test runner | Playwright Test | 1.44 | Auto-waiting, trace viewer, first-class parallelism |
| Assertion library | Playwright `expect` | bundled | Web-first assertions reduce flake |
| Reporting | Playwright HTML report | bundled | Enough for now; Allure evaluated and postponed |
| CI runner | GitHub Actions | ubuntu-latest | Same platform the app deploys on |

## 4. Repository Layout

```text
shoplite-e2e/
├── tests/
│   └── e2e/
│       ├── auth/
│       └── checkout/
├── pages/
│   ├── LoginPage.ts
│   └── CheckoutPage.ts
├── core/
│   ├── config/
│   │   └── environment.ts
│   └── fixtures/
│       └── users.ts
├── infra/
│   ├── playwright.config.ts
│   └── Dockerfile
├── .github/workflows/e2e-tests.yml
└── docs/framework-setup.md
```

## 5. Configuration Files

- `infra/playwright.config.ts` — projects (chromium, firefox), one retry on CI, `baseURL` read from `BASE_URL`
- `.env.example` — committed template listing `BASE_URL`, `TEST_USER_EMAIL` and `API_TOKEN`
- `.github/workflows/e2e-tests.yml` — smoke suite on pull requests, full regression nightly
- `eslint.config.mjs` — blocks `waitForTimeout` and CSS selectors under `tests/`

## 6. Environment Variables

| Variable | Purpose | Example |
|---|---|---|
| `BASE_URL` | Target environment | `https://staging.shoplite.internal` |
| `TEST_USER_EMAIL` | Seeded QA account | `qa-bot@shoplite.test` |
| `API_TOKEN` | Auth for API seeding | CI secret, never committed |

## 7. Coding Standards

- Spec files `feature-name.spec.ts` under `tests/e2e/`; page objects `PascalCase.ts` under `pages/`
- Selectors: `data-testid` attributes only; no CSS or XPath selectors in specs
- Test data from factories in `core/fixtures/`; no hardcoded user IDs or emails in specs
- Web-first assertions only; `waitForTimeout` is blocked by the lint rule

## 8. Setup Definition of Done

- [x] Repo scaffolded; `tests/e2e/auth/login.spec.ts` smoke spec passing
- [x] Config files committed: `playwright.config.ts`, `.env.example`, `eslint.config.mjs`
- [x] CI job green on `main` and required check on pull requests
- [x] First real test, `checkout/happy-path.spec.ts`, merged via PR
- [x] Document reviewed by QA and dev leads, merged with the scaffold PR
