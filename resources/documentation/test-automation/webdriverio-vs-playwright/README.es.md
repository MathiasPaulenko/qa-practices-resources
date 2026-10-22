# WebDriverIO vs Playwright — Companion

Este companion contiene los archivos ejecutables de la guía de decisión [WebDriverIO 8 vs Playwright 1.45](https://qapractices.com/es/documentation/webdriverio-vs-playwright).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `tests/wdio.conf.ts` | Configuración de WebDriverIO 8: Mocha + TypeScript, 4 instancias en paralelo |
| `tests/appointments.wdio.spec.ts` | Test de reserva de turnos de VitaCare en WebDriverIO, incluido el stub de pagos con `browser.mock` |
| `tests/playwright.config.ts` | Configuración de Playwright 1.45: `fullyParallel`, proyectos chromium y webkit |
| `tests/appointments.pw.spec.ts` | El mismo test de reserva de turnos en Playwright, incluido el stub de pagos con `page.route` |

## Inicio rápido

```bash
# WebDriverIO 8
npm install -D @wdio/cli @wdio/local-runner @wdio/mocha-framework @wdio/spec-reporter tsx
npx wdio run tests/wdio.conf.ts

# Playwright 1.45
npm install -D @playwright/test@1.45
npx playwright install chromium webkit
npx playwright test -c tests/playwright.config.ts
```

## Notas

- `browser.mock` requiere soporte de WebDriver BiDi: Chromium y Firefox locales, Selenium Grid 4+ o un proveedor cloud con BiDi habilitado. En grids sin BiDi, cambia el spec a `page.route` en Playwright o a un stub a nivel de servicio.
- Los specs apuntan a `https://staging.vitacare.io`, la app de staging ficticia de la guía. Sustituye `baseURL` y la cuenta precargada `qa-patient@vitacare.io` por tu propio entorno y define `E2E_PASSWORD` antes de ejecutar.
