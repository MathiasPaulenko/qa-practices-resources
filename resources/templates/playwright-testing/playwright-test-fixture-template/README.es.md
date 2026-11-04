# Plantilla de Fixtures para Tests de Playwright — Recursos Complementarios

Archivos ejecutables complementarios para la [Plantilla de Fixtures para Tests de Playwright](https://qapractices.com/es/templates/playwright-test-fixture-template/) en QAPractices.com.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `fixtures/base.fixture.ts` | Fixture base: `testUser`, `apiContext` (request context autenticado) y teardown `cleanDb`. |
| `fixtures/data.fixture.ts` | Fixtures de test data (`testProduct`, `createdOrder`) sembrados por API con teardown. |
| `fixtures/page.fixture.ts` | Fixture de page object `DashboardPage`. |
| `global-setup.ts` | Login por UI una sola vez que escribe el JSON de `storageState` para reutilizar entre tests. |
| `auth.spec.ts` | Spec de ejemplo consumiendo el storage state guardado — cero logins por test. |
| `playwright.config.ts` | Proyectos, retries, reporters y wiring de `globalSetup`. |

## Requisitos

- `@playwright/test` 1.x (`npm install -D @playwright/test` + `npx playwright install`)
- Node.js 20 LTS
- Una app bajo test que exponga `/login` y los endpoints de API referenciados por los fixtures (o adaptalos).

## Inicio Rápido

1. Copiá `fixtures/`, `global-setup.ts` y `playwright.config.ts` en tu árbol `tests/`.
2. Seteá las env vars `BASE_URL`, `API_BASE_URL`, `API_TOKEN`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
3. Apuntá los selectores de login y los endpoints de seeding a tu app.
4. Corré `npx playwright test`.
