# Mejores Prácticas de Cypress — Archivos Companion

Companion de [Cypress: Patrones de Automatización](https://qapractices.com/es/documentation/cypress-best-practices/). Un spec determinístico, un comando de login con sesión cacheada y una config lista para CI que muestran los cinco patrones de la guía funcionando juntos.

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `cypress/e2e/login.cy.js` | Spec de login con `cy.intercept` + selectores `data-cy`: un test feliz y otro con 401 mockeado — sin waits fijos. |
| `cypress/support/commands.js` | `cy.login()` con caché de `cy.session` más `cy.loginByApi()` para cuando la página de login no es lo que se testea. |
| `cypress.config.js` | `baseUrl`, `testIsolation`, `retries` divididos entre `runMode`/`openMode`, video apagado, screenshots en fallo. |

## Inicio Rápido

```bash
npm install --save-dev cypress@14
# copiá los archivos a tu proyecto, apuntá baseUrl a tu app, después:
npx cypress run --spec cypress/e2e/login.cy.js
```

El spec espera una página `/login` con atributos `data-cy` (`email`,
`password`, `submit-login`, `login-error`) y un endpoint `POST /api/login`.
Renombrá los atributos para que coincidan con tu markup si tu convención es otra.

## Requisitos

- Node.js 18+
- Cypress 13+ (14 recomendado)
