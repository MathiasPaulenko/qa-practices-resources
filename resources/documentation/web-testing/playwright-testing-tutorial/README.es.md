# Tutorial de Playwright Testing — Companion Ejecutable

Proyecto inicial ejecutable del [Tutorial de Playwright: Setup, Selectores y Assertions](https://qapractices.com/es/documentation/playwright-testing-tutorial/) en QAPractices.

## Contenido

| Archivo | Paso del tutorial |
|---|---|
| `package.json` | Paso 1 — dependencia `@playwright/test` |
| `playwright.config.ts` | Pasos 2/10 — tres proyectos de navegador, reintentos, trace en primer reintento |
| `tests/first-test.spec.ts` | Paso 3 — assertion de título en playwright.dev |
| `tests/locators.spec.ts` | Paso 4 — localizadores por rol, texto y test-id |
| `tests/network-mock.spec.ts` | Paso 7 — intercepción con `page.route` y respuesta JSON simulada |
| `tests/auth-fixture.spec.ts` | Fixture de auth por API con inyección de token, y visual regression con `toHaveScreenshot` |
| `.github/workflows/playwright.yml` | Paso 10 — job de CI con instalación de navegadores, sharding y artefacto de reporte |

## Uso

```bash
npm install
npx playwright install --with-deps
npx playwright test
```

Los specs apuntan a `https://playwright.dev` para correr sin servidor local. Para apuntarlos a tu app, cambia las URLs y los localizadores — la estructura se mantiene igual.
