# Guía de Regresión Visual — Companion

Ejemplos ejecutables de la [guía Pruebas de Regresión Visual: Baselines y Diff de Screenshots](https://qapractices.com/es/documentation/visual-regression-testing-guide). Cada carpeta cubre una herramienta para que elijas la que encaje con tu equipo.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `tests/visual-baseline.spec.js` | Baselines con `toHaveScreenshot` de Playwright, opciones de tolerancia y máscaras de regiones. |
| `percy/percy-visual.spec.js` | Snapshots de Percy dentro de un test de Playwright, ejecutados con `percy exec`. |
| `percy/.percy.yml` | Configuración de snapshots de Percy: anchos móvil + desktop, supresión de spinners. |
| `backstopjs/backstop.json` | Configuración self-hosted: dos viewports, selectores de escenario, umbral de 0.1%. |
| `applitools/applitools-eyes.spec.js` | Applitools Eyes con `ClassicRunner`, configuración de batch y `closeAsync`. |
| `.github/workflows/visual-regression-tests.yml` | Workflow de PR que corre tests `@visual` y sube los diffs como artefactos si falla. |

## Requisitos

- Node.js 20+
- `@playwright/test` 1.63+ (ejemplos de Playwright)
- `@percy/cli` 1.32+ y `@percy/playwright` 1.1+ (ejemplo de Percy)
- `backstopjs` 6.3+ (ejemplo de BackstopJS)
- `@applitools/eyes-playwright` 1.49+ y `APPLITOOLS_API_KEY` (ejemplo de Applitools)

## Uso

### Playwright

1. Copia `tests/visual-baseline.spec.js` a la carpeta `tests/` de tu proyecto.
2. Reemplaza `BASE_URL` por tu URL de staging.
3. Corre `npx playwright test` una vez para generar las baselines, revísalas y commitea los PNG.
4. Actualiza baselines tras cambios intencionales con `npx playwright test --update-snapshots`.

### Percy

1. Copia `percy/percy-visual.spec.js` y `percy/.percy.yml` a tu proyecto.
2. Exporta `PERCY_TOKEN` desde la configuración de tu proyecto Percy.
3. Corre `npx percy exec -- playwright test percy/percy-visual.spec.js`.
4. Revisa y aprueba los diffs en el dashboard de Percy.

### BackstopJS

1. Copia `backstopjs/backstop.json` a la raíz de tu proyecto como `backstop.json`.
2. Corre `npx backstop reference` para capturar baselines y `npx backstop test` para comparar.
3. Aprueba los cambios revisados con `npx backstop approve` y commitea `backstop_data/`.

### Applitools

1. Copia `applitools/applitools-eyes.spec.js` a tu carpeta `tests/`.
2. Exporta `APPLITOOLS_API_KEY` como variable de entorno o secret de CI.
3. Corre `npx playwright test applitools/applitools-eyes.spec.js` y revisa los diffs en el dashboard de Applitools.

### CI

Copia `.github/workflows/visual-regression-tests.yml` a `.github/workflows/` de tu repo. Las baselines deben generarse en el mismo SO que el runner (`ubuntu-latest` aquí) o cada ejecución difundirá por el renderizado de fuentes.

## Disciplina de Baselines

Nunca apruebes ni regenere una baseline sin revisar el diff primero — ese único hábito es lo que separa las pruebas visuales del ruido de screenshots.
