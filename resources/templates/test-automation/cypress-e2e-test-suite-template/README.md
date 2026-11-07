# Cypress E2E Test Suite Template — Companion

Runnable Cypress 16 project scaffold for the [Cypress E2E Test Suite Template](https://qapractices.com/templates/cypress-e2e-test-suite-template/) on QAPractices.

## What's inside

```text
cypress/
├── e2e/
│   ├── auth/login.cy.js          # smoke-tagged login spec (5 tests)
│   └── users/user-management.cy.js  # regression-tagged CRUD spec (5 tests)
├── fixtures/
│   ├── users.json                # fake users on the reserved .test TLD
│   └── products.json             # valid / out-of-stock / invalid products
└── support/
    ├── commands.js               # cy.login (cy.session), fillForm, apiLogin, apiRequest…
    ├── e2e.js                    # support file — deliberately no storage-clearing hooks
    └── page_objects/
        ├── LoginPage.js
        └── DashboardPage.js
cypress.config.js                 # Cypress 16 config with env-driven baseUrl + mochawesome
.github/workflows/cypress-e2e.yml # smoke on PR (browser matrix), regression nightly (parallel)
package.json                      # pinned deps: cypress ^16.2.1, grep ^7, mochawesome ^5
```

## Quick start

```bash
npm install
CYPRESS_BASE_URL=http://localhost:3000 npm run cy:open    # interactive
npm run cy:run:smoke                                     # headless smoke run
```

Set `CYPRESS_BASE_URL` to point at your app — it overrides `baseUrl` per environment without editing the config.

## Notes

- **No `cy.clearCookies()`/`cy.clearLocalStorage()`** in `e2e.js`: a global `beforeEach` that wipes storage destroys the `cy.session` login cache.
- **No `cypress-xpath`**: every selector is `data-testid`, ARIA or stable ID — the plugin is unmaintained and buys nothing here.
- **Emails use `@yourapp.test`** — RFC 2606 reserved TLD, safe to commit.
- **Parallel execution** is a Cypress Cloud feature wired in the workflow (`--record --parallel` + `CYPRESS_RECORD_KEY`), not an npm script with a hardcoded key.

## Related

- Resource (EN): <https://qapractices.com/templates/cypress-e2e-test-suite-template/>
- Resource (ES): <https://qapractices.com/es/templates/cypress-e2e-test-suite-template/>
