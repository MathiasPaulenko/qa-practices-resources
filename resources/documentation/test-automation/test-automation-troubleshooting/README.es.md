# Diagnóstico de automatización de pruebas — Companion

Ejemplos ejecutables de Playwright para la [guía de diagnóstico de automatización de pruebas](https://qapractices.com/es/documentation/test-automation-troubleshooting/).

## Requisitos

- Node.js 26.13.1
- `@playwright/test` 1.65.1 (fijado en `package-lock.json`)
- Chromium instalado por Playwright

## Ejecución

```bash
npm ci
npx playwright install chromium
npm test
```

Las pruebas usan fixtures aislados de Playwright y una página inline; no necesitan servidor de aplicación, base de datos ni credenciales. `pipeline-status.spec.ts` muestra cómo esperar un estado observable en vez de dormir; `selector-contract.spec.ts` utiliza un localizador por rol.

El workflow de GitHub Actions fija las acciones mediante SHA completo. Sustituye la página inline por una ruta de staging solo después de configurar `baseURL`, los datos de prueba y la disponibilidad de servicios en tu proyecto.
