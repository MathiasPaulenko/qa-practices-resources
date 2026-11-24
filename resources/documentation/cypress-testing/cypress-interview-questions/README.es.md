# Preguntas de Entrevista de Cypress — Companion

Este companion incluye archivos ejecutables para la guía [Preguntas de Entrevista de Cypress](https://qapractices.com/es/documentation/cypress-interview-questions). Cada ejemplo usa la sintaxis de Cypress 13.6 del escenario GreenCart de la guía.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `src/cart-flake.spec.js` | El test flaky de Black Friday: clic y luego aserción antes de que la API resuelva |
| `src/cart-fixed.spec.js` | El spec arreglado: intercept, alias, wait y luego aserción — más login con `cy.session()` |
| `src/login-command.js` | Comando personalizado `cy.login()` respaldado por `cy.session()` |
| `src/intercept-mock.js` | Patrones de `cy.intercept()`: mockear, modificar, esperar |
| `src/ci-workflow.yml` | Workflow de GitHub Actions: `cypress run --record --parallel` en shards |
| `src/retries-config.js` | Configuración `retries.runMode` / `openMode` para `cypress.config.ts` |

## Inicio Rápido

```bash
npm init -y && npm install cypress@13.6
npx cypress open
```

Copia los specs en `cypress/e2e/` y el comando de soporte en `cypress/support/commands.js`. Los specs del carrito asumen un storefront que expone `POST /api/cart` y elementos con atributos `data-cy` — adapta los selectores a tu app.

## Notas

- `cart-flake.spec.js` está roto a propósito: demuestra la race condition donde la aserción corre antes de que `POST /api/cart` se resuelva. Espera que falle de forma intermitente en CI.
- `cart-fixed.spec.js` es la respuesta de entrevista: alias a la petición, espera sobre el alias, aserción contra el DOM actualizado.
