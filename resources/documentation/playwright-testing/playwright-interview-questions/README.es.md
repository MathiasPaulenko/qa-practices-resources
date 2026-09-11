# Preguntas de Entrevista de Playwright — Companion

Este companion provee archivos ejecutables para la guía [Top 20 Preguntas de Entrevista de Playwright](https://qapractices.com/es/documentation/playwright-interview-questions).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `src/custom-fixture.js` | Fixture personalizado con página autenticada |
| `src/storage-state.js` | Guardar y restaurar estado del navegador |
| `src/network-mock.js` | Interceptar y mockear peticiones de red |
| `src/api-test.js` | Testing de API con el fixture request |
| `src/popup-handling.js` | Manejo de múltiples tabs y popups |
| `src/file-download.js` | Manejo de descarga de archivos |
| `src/file-upload.js` | Manejo de subida de archivos con setInputFiles() |
| `src/trace-config.js` | Configuración de Trace Viewer |
| `src/ci-workflow.yml` | Workflow de CI con GitHub Actions |
| `src/retries-config.js` | Configuración de retries de tests |
| `src/projects-config.js` | Configuración de proyectos de Playwright |

## Inicio Rápido

```bash
npm init -y && npm install @playwright/test
npx playwright install --with-deps
npx playwright test
```