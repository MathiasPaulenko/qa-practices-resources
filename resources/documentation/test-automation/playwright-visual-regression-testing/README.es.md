# Playwright Visual Regression Testing — Companion

Archivos companion para la [guía de Playwright Visual Regression Testing](https://qapractices.com/es/documentation/playwright-visual-regression-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `playwright.config.js` | Config de Playwright con snapshotPathTemplate, defaults de toHaveScreenshot y 3 proyectos de viewport. |
| `tests/visual-homepage.spec.js` | Test de regresión visual de página completa para homepage. |
| `tests/visual-checkout.spec.js` | Test visual a nivel de componente para checkout summary con mock de API y mask. |
| `tests/visual-button.spec.js` | Test visual a nivel de componente para un botón primario en Storybook. |
| `.github/workflows/visual-regression-tests.yml` | Workflow de GitHub Actions para correr tests visuales en CI. |

## Requisitos

- Node.js 20+
- Playwright 1.48+

## Uso

1. Copiá `playwright.config.js` a la raíz de tu proyecto.
2. Copiá los archivos de test a tu directorio `tests/`.
3. Copiá el workflow de GitHub Actions a `.github/workflows/`.
4. Ejecutá `npx playwright install --with-deps` para instalar navegadores.
5. Ejecutá `npx playwright test` para correr los tests visuales.
6. En la primera ejecución, se generan los baselines. Revisalos y commitealos.
7. En ejecuciones siguientes, Playwright compara contra los baselines almacenados.

## Actualización de Baselines

Cuando un cambio visual es intencional:

```bash
npx playwright test --update-snapshots
```

Revisá el diff en `playwright-report/index.html` antes de commitear los baselines actualizados.
