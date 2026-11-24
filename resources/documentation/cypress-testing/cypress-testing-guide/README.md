# Cypress Testing Guide — Companion

Runnable examples from the [Cypress Testing Guide](https://qapractices.com/documentation/cypress-testing-guide/) on QAPractices.com.

## Contents

| File | What it shows |
|---|---|
| `src/cypress.config.js` | E2E `baseUrl` plus the `component.devServer` block for React 18 + Vite 5 |
| `src/login.cy.js` | E2E login spec: happy path plus a `cy.intercept` error-state test |
| `src/submit-button.cy.jsx` | Component test with `cy.mount`, prop states, and a `cy.stub` spy |

## Usage

Requires Cypress 13 and a React 18 + Vite project.

```bash
npm install -D cypress@13.13.0
npx cypress run --spec "cypress/e2e/login.cy.js"   # E2E
npx cypress run --component                          # component tests
```
