# Guía de Puppeteer Testing — Companion Ejecutable

Ejemplos JavaScript ejecutables de la [Guía de Puppeteer Testing para Headless Chrome](https://qapractices.com/es/documentation/puppeteer-testing-guide/) en QAPractices. Escritos para **Puppeteer 24.x** y **jest-puppeteer 10**.

## Contenido

| Archivo | Cubre |
|---|---|
| `javascript/verify-install.js` | Smoke check mínimo: launch → goto → title → close |
| `javascript/first-test.js` | Spec de login: `type`, `click`, `waitForSelector`, `$eval` |
| `javascript/selectors.js` | CSS, `::-p-xpath`, `::-p-text`, `$$`, `page.evaluate` |
| `javascript/screenshots.js` | Página completa, elemento y screenshot-en-fallo |
| `javascript/waits.js` | `waitForSelector`, `waitForNavigation`, `networkidle0`, `waitForFunction` |
| `javascript/network-interception.js` | Bloqueo de imágenes, mocks de API, log de llamadas |
| `javascript/pdf.js` | `page.pdf` con A4, márgenes y `printBackground` |
| `javascript/jest.config.js` | Preset `jest-puppeteer` + timeout de 60s |
| `pages/LoginPage.js` | Clase Page Object del flujo de login |
| `pages/login.test.js` | Spec que consume el Page Object |
| `.github/workflows/puppeteer-tests.yml` | Job de CI: `npm ci` → `npx jest --ci` → subir screenshots |

## Setup

```bash
npm install puppeteer@24
npm install --save-dev jest jest-puppeteer@10
```

`staging.myapp.com` es un placeholder — reemplázalo con tu URL de staging y tus credenciales.

## Notas

- `page.$x` y `page.waitForTimeout` se eliminaron en Puppeteer 22; los ejemplos usan `page.locator('::-p-xpath(...)')` / `::-p-text` y promesas `setTimeout` comunes.
- En CI, prefiere `puppeteer-core` más `executablePath` si tu imagen ya trae Chrome — salta la descarga de Chromium.
- Los screenshots caen en `screenshots/` y el workflow los sube como artifacts en cada corrida (`if: always()`).
