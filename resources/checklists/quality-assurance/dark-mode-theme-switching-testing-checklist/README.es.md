# Pruebas de Dark Mode y Cambio de Tema — Compañero Ejecutable

Spec de Playwright 1.48+ que cubre las partes automatizables del [Checklist de Pruebas de Dark Mode y Cambio de Tema](https://qapractices.com/es/checklists/dark-mode-theme-switching-testing-checklist/): orden de resolución del tema, persistencia, detección de FOIT y comportamiento del toggle.

## Contenido

| Archivo | Propósito |
|---|---|
| `dark-mode.spec.ts` | Tests de resolución de tema, FOIT, toggle y persistencia |
| `meta.json` | Metadata del recurso |

## Requisitos

- Node.js 20+
- `@playwright/test` 1.48+ (`npm i -D @playwright/test` y `npx playwright install chromium`)

## Uso

```bash
BASE_URL=https://tu-app.com npx playwright test dark-mode.spec.ts --reporter=list
```

## Supuestos a adaptar

El spec asume tres convenciones — cámbialas para que coincidan con tu app:

| Convención | Default | Dónde cambiarla |
|---|---|---|
| Clase de tema en `<html>` | `dark` / `light` | `appliedTheme()` |
| Clave de storage | `localStorage['theme']` | `THEME_KEY` |
| Nombre accesible del toggle | `/theme|modo|tema/i` | `getByRole('button', ...)` |

## Qué no cubre

Los ratios de contraste, el modo forced-colors y el tema de widgets de terceros necesitan revisión manual o herramientas dedicadas (axe-core, visual regression). Las assertions a nivel DOM de aquí complementan, no reemplazan, la pasada visual del checklist.
