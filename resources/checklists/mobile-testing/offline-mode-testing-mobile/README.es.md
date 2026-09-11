# Checklist de Testing Offline PWA — Companion

Este companion provee archivos ejecutables para el checklist [Checklist de Testing Offline](https://qapractices.com/es/checklists/offline-mode-testing-mobile).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `src/workbox-register.js` | Registro de service worker con Workbox y prompt de skip-waiting |
| `src/indexeddb-read.js` | Ejemplo de lectura de IndexedDB para acceso offline |
| `src/network-transition-test.ts` | Test de Playwright para transición de red (online a offline) |
| `src/background-sync-register.js` | Registro de Background Sync para requests encolados |

## Inicio Rápido

```bash
# Instalar Playwright
npm init -y && npm install @playwright/test

# Correr el test de transición de red
npx playwright test src/network-transition-test.ts

# Servir la PWA localmente y testear el registro de Workbox
npx http-server . && open http://localhost:8080
```