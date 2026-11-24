# Cypress Interview Questions — Companion

This companion provides runnable files for the [Cypress Interview Questions](https://qapractices.com/documentation/cypress-interview-questions) guide. Every example matches the Cypress 13.6 syntax used in the guide's GreenCart scenario.

## Files

| File | Purpose |
|------|---------|
| `src/cart-flake.spec.js` | The Black Friday flaky test: click, then assert before the API resolves |
| `src/cart-fixed.spec.js` | The fixed spec: intercept, alias, wait, then assert — plus `cy.session()` login |
| `src/login-command.js` | Custom `cy.login()` command backed by `cy.session()` |
| `src/intercept-mock.js` | `cy.intercept()` patterns: mock, modify, wait |
| `src/ci-workflow.yml` | GitHub Actions workflow: sharded `cypress run --record --parallel` |
| `src/retries-config.js` | `retries.runMode` / `openMode` configuration for `cypress.config.ts` |

## Quick Start

```bash
npm init -y && npm install cypress@13.6
npx cypress open
```

Drop the spec files into `cypress/e2e/` and the support command into `cypress/support/commands.js`. The cart specs assume a storefront exposing `POST /api/cart` and elements tagged with `data-cy` attributes — adapt the selectors to your own app.

## Notes

- `cart-flake.spec.js` is intentionally broken: it demonstrates the race condition where the assertion runs before `POST /api/cart` resolves. Expect it to fail intermittently in CI.
- `cart-fixed.spec.js` is the interview answer: alias the request, wait on the alias, assert against the updated DOM.
