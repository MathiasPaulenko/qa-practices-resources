# Companion de la Guía de Testing PWA

Recurso companion de la [Guía de Testing PWA](https://qapractices.com/es/documentation/pwa-testing-guide). Incluye una configuración runnable de Workbox, tests de PWA con Playwright, un web app manifest válido, y un workflow de CI.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `workbox-config.js` | Configuración de Workbox 7.4.1 para generar un service worker |
| `sw.js` | Service worker personalizado con estrategias NetworkFirst, CacheFirst y StaleWhileRevalidate |
| `manifest.json` | Web app manifest válido con iconos 192x192 y 512x512 |
| `playwright.config.ts` | Config de Playwright pineada a Chromium con `serviceWorkers: 'allow'` |
| `tests/offline.spec.ts` | Smoke test offline — verifica que el app shell cargue sin red |
| `tests/installability.spec.ts` | Test de installability — verifica que `beforeinstallprompt` se dispare |
| `.github/workflows/pwa-tests.yml` | Workflow de CI que compila, genera SW, levanta túnel HTTPS y corre Playwright |

## Inicio Rápido

```bash
npm install --save-dev workbox-cli@7.4.1 @playwright/test
npx workbox generateSW workbox-config.js
npx playwright test tests/
```

## CI

El workflow incluido de GitHub Actions corre en cada push y PR:

1. Instala dependencias
2. Compila el proyecto
3. Genera el service worker con Workbox
4. Levanta un túnel HTTPS con `localtunnel`
5. Corre los tests de PWA con Playwright

## Requisitos

- Node.js 22+
- Workbox CLI 7.4.1
- Playwright 1.50+
- Un build output en `dist/`
