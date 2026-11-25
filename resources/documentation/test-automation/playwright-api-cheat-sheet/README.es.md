# Playwright API: Cheat Sheet — Companion Ejecutable

Snippets de `@playwright/test` 1.x listos para copiar, companion del [Cheat Sheet de la API de Playwright](https://qapractices.com/es/documentation/playwright-api-cheat-sheet/) en QAPractices.

## Contenido

`typescript/` contiene un archivo por sección del cheat sheet:

| Archivo | Cubre |
|---|---|
| `browser-context.ts` | Lanzar navegadores y `BrowserContext` aislados |
| `navigation.ts` | `goto`, historial, `waitForURL`, `waitForLoadState` |
| `locators.ts` | `page.locator()` y locators `getBy*`, encadenamiento, filtrado |
| `actions.ts` | Click, fill, press, select, check, drag, subida de archivos |
| `assertions.ts` | Aserciones `expect` con reintento (web-first) |
| `auto-waiting.ts` | Estados de `locator.waitFor()` y `setDefaultTimeout` |
| `network.ts` | `page.route`, `waitForResponse`, `page.request` |
| `dialogs.ts` | Handler `page.on('dialog')` (registrar antes de disparar) |
| `screenshots.ts` | Screenshots de página, página completa y elemento |
| `multiple-pages.ts` | Capturar pestañas nuevas vía `context.waitForEvent('page')` |
| `fixtures-hooks.ts` | Fixture `page` incorporado, `beforeEach`/`afterEach` |
| `playwright.config.ts` | Timeouts, reintentos, baseURL, artefactos en fallo |

## Uso

Son snippets de referencia, no una suite ejecutable — la mayoría operan sobre `page`/`context`/`browser` que provee tu test o sesión REPL. Para probarlos en un proyecto real:

```bash
npm init playwright@latest
npx playwright test
```

Mira el cheat sheet para las notas sobre cuándo aplica cada llamada y los errores comunes (auto-waiting, orden de diálogos, `networkidle`).
