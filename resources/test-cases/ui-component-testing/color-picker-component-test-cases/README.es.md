# Casos de Prueba de Color Picker — ejemplos ejecutables

Companion de [Casos de Prueba de Color Picker: Selección, Preview, Input](https://qapractices.com/es/test-cases/color-picker-component-test-cases/).

## Contenido

- `color-utils.js` — luminancia relativa y ratio de contraste WCAG 2.x, parseo y validación de hex.
- `color-utils.test.mjs` — checks con el test runner de Node (`node --test`), sin dependencias.
- `color-picker.spec.ts` — spec de Playwright 1.48: input hex, hex inválido, portapapeles, escaneo axe-core 4.10.

## Ejecutar

```bash
npm install
npm test            # unitarios: contraste + parseo hex
npm run test:e2e    # requiere una app con /editor/palette y los hooks data-testid
```

El spec apunta a un picker con hooks `data-testid` (`color-picker-trigger`, `hex-input`, `color-preview`, `copy-color`, `hex-error`). Adaptá los selectores a tu implementación.
