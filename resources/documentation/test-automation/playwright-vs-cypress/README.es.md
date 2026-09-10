# Playwright vs Cypress — Companion

Este companion provee archivos ejecutables para la guía [Playwright vs Cypress: Matriz de Decisión E2E](https://qapractices.com/es/documentation/playwright-vs-cypress).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `tests/playwright-3ds.spec.ts` | Test de Playwright 1.61.1 para flujo 3DS de Adyen |
| `tests/cypress-3ds.cy.js` | Test de Cypress 15.18.1 para flujo 3DS de Adyen |
| `tests/playwright.config.ts` | Config de Playwright con proyectos para chromium, firefox, webkit y mobile |
| `.github/workflows/playwright-e2e.yml` | Workflow de GitHub Actions con 4 shards paralelos |
| `.github/workflows/cypress-e2e.yml` | Workflow de GitHub Actions para Cypress (máquina única) |

## Inicio Rápido

```bash
# Instalar dependencias
npm install -D @playwright/test cypress

# Correr test 3DS de Playwright
npx playwright test tests/playwright-3ds.spec.ts

# Correr test 3DS de Cypress
npx cypress run --spec tests/cypress-3ds.cy.js

# Correr Playwright con sharding (CI)
npx playwright test --shard=1/4 --workers=4
```

## Integración CI

Los workflows de GitHub Actions incluidos corren Playwright (4 shards) y Cypress (máquina única) en cada push y pull request.