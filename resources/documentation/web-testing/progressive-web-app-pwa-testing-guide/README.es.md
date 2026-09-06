# Guía de Testing PWA — Scripts Companion

Scripts companion para la [Guía de Testing de PWA](https://qapractices.com/es/documentation/progressive-web-app-pwa-testing-guide).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `scripts/manifest.json` | Web app manifest válido con `id`, íconos y display standalone. |
| `scripts/workbox-config.js` | Configuración de Workbox 7 con estrategias CacheFirst, NetworkFirst y StaleWhileRevalidate. |
| `scripts/playwright-offline-test.js` | Test de Playwright 1.48: verifica que el app shell carga offline después de la primera visita. |
| `scripts/playwright-install-prompt-test.js` | Test de Playwright 1.48: verifica que `beforeinstallprompt` es diferible. |
| `scripts/lighthouse-ci-config.json` | Config de Lighthouse 12 CI con threshold de PWA score en 90. |

## Uso

```bash
# Instalar dependencias
npm install workbox-routing@7 workbox-strategies@7
npm install -D @playwright/test@1.48 lighthouse@12

# Correr tests de PWA con Playwright
npx playwright test scripts/playwright-offline-test.js
npx playwright test scripts/playwright-install-prompt-test.js

# Correr Lighthouse CI
npx lighthouse-ci --config=scripts/lighthouse-ci-config.json https://pwa.qa.local
```

## Requisitos

- Node.js 20+
- Playwright 1.48+
- Lighthouse 12+
- Workbox 7+
