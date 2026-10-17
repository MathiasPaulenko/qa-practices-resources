# Cypress Best Practices — Companion Files

Companion for [Cypress: Core Automation Patterns](https://qapractices.com/documentation/cypress-best-practices/). A deterministic spec, a session-cached login command and a CI-ready config that show the five patterns from the guide working together.

## Files

| File | Purpose |
| ---- | ------- |
| `cypress/e2e/login.cy.js` | Login spec using `cy.intercept` + `data-cy` selectors: one happy-path test and one stubbed-401 test — no fixed waits anywhere. |
| `cypress/support/commands.js` | `cy.login()` with `cy.session` caching plus `cy.loginByApi()` for when the login page isn't under test. |
| `cypress.config.js` | `baseUrl`, `testIsolation`, `retries` split between `runMode`/`openMode`, video off, screenshots on failure. |

## Quick Start

```bash
npm install --save-dev cypress@14
# drop the files into your project, point baseUrl at your app, then:
npx cypress run --spec cypress/e2e/login.cy.js
```

The spec expects a `/login` page with `data-cy` attributes (`email`,
`password`, `submit-login`, `login-error`) and a `POST /api/login` endpoint.
Rename the attributes to match your markup if your convention differs.

## Requirements

- Node.js 18+
- Cypress 13+ (14 recommended)
