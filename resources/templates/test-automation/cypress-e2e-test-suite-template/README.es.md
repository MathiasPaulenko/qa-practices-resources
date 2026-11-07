# Plantilla de Suite de Pruebas E2E con Cypress — Companion

Scaffold ejecutable de proyecto Cypress 16 para la [Plantilla de Suite de Pruebas E2E con Cypress](https://qapractices.com/es/templates/cypress-e2e-test-suite-template/) de QAPractices.

## Qué incluye

```text
cypress/
├── e2e/
│   ├── auth/login.cy.js          # spec de login etiquetado smoke (5 tests)
│   └── users/user-management.cy.js  # spec CRUD etiquetado regression (5 tests)
├── fixtures/
│   ├── users.json                # usuarios falsos en el TLD reservado .test
│   └── products.json             # producto válido / sin stock / inválido
└── support/
    ├── commands.js               # cy.login (cy.session), fillForm, apiLogin, apiRequest…
    ├── e2e.js                    # support file — sin hooks que limpien storage a propósito
    └── page_objects/
        ├── LoginPage.js
        └── DashboardPage.js
cypress.config.js                 # config de Cypress 16 con baseUrl por env + mochawesome
.github/workflows/cypress-e2e.yml # smoke en PR (matriz de navegadores), regresión nightly (paralelo)
package.json                      # deps pineadas: cypress ^16.2.1, grep ^7, mochawesome ^5
```

## Inicio rápido

```bash
npm install
CYPRESS_BASE_URL=http://localhost:3000 npm run cy:open    # interactivo
npm run cy:run:smoke                                     # smoke headless
```

Seteá `CYPRESS_BASE_URL` para apuntar a tu app — pisa el `baseUrl` por entorno sin editar la config.

## Notas

- **Sin `cy.clearCookies()`/`cy.clearLocalStorage()`** en `e2e.js`: un `beforeEach` global que limpia el storage destruye el caché de login de `cy.session`.
- **Sin `cypress-xpath`**: todos los selectores son `data-testid`, ARIA o ID estable — el plugin no está mantenido y acá no suma nada.
- **Los emails usan `@yourapp.test`** — TLD reservado por la RFC 2606, seguro para commitear.
- **La ejecución paralela** es una feature de Cypress Cloud cableada en el workflow (`--record --parallel` + `CYPRESS_RECORD_KEY`), no un script npm con una key hardcodeada.

## Relacionados

- Recurso (ES): <https://qapractices.com/es/templates/cypress-e2e-test-suite-template/>
- Recurso (EN): <https://qapractices.com/templates/cypress-e2e-test-suite-template/>
