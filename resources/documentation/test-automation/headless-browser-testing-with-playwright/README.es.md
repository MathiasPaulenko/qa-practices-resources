# Companion de Testing Headless con Playwright

Configuración ejecutable de Playwright v1.61 headless, auth setup, Dockerfile, workflow de GitHub Actions y tests de ejemplo para la [Guía de Testing Headless con Playwright](https://qapractices.com/es/documentation/headless-browser-testing-with-playwright/).

## Contenidos

| Archivo | Qué hace |
| --- | --- |
| `playwright.config.ts` | Proyectos headless para Chromium, Firefox y WebKit con tracing y screenshots |
| `auth.setup.ts` | Setup de autenticación que guarda `auth.json` para reutilizar |
| `Dockerfile.test` | Imagen Docker de Playwright pineada para CI |
| `tests/login.spec.ts` | Test de login de ejemplo con selectores `data-testid` |
| `.github/workflows/playwright.yml` | Workflow de GitHub Actions con upload de artefactos on failure |

## Quick Start

```bash
# 1. Instalar dependencias
npm init -y && npm install -D @playwright/test@1.61.1
npx playwright install --with-deps

# 2. Copiá los archivos de configuración de este companion
# 3. Corré los tests headless
npx playwright test --project=chromium-headless --trace=on

# 4. Visualizá el trace en caso de falla
npx playwright show-trace test-results/trace.zip
```

## Docker

```bash
docker build -f Dockerfile.test -t playwright-tests .
docker run --rm --ipc=host playwright-tests
```

Usá `--ipc=host` cuando corras 4+ workers para prevenir OOM kills por límites de memoria compartida.

## CI

El archivo `.github/workflows/playwright.yml` ejecuta tests headless en cada push y pull request, subiendo el reporte de Playwright y los test results como artefactos on failure.

## Licencia

MIT — ver el repositorio principal para detalles.
