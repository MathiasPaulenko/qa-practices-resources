# Guía de Cypress — Companion

Ejemplos ejecutables de la [Guía de Cypress](https://qapractices.com/es/documentation/cypress-testing-guide/) en QAPractices.com.

## Contenido

| Archivo | Qué muestra |
|---|---|
| `src/cypress.config.js` | `baseUrl` de E2E más el bloque `component.devServer` para React 18 + Vite 5 |
| `src/login.cy.js` | Spec E2E de login: camino feliz más un test de error con `cy.intercept` |
| `src/submit-button.cy.jsx` | Test de componente con `cy.mount`, estados por props y un spy con `cy.stub` |

## Uso

Requiere Cypress 13 y un proyecto React 18 + Vite.

```bash
npm install -D cypress@13.13.0
npx cypress run --spec "cypress/e2e/login.cy.js"   # E2E
npx cypress run --component                          # tests de componentes
```
