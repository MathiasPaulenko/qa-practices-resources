# Troubleshooting de Accessibility Testing — Companion

Snippets ejecutables referenciados en la [Guía de Troubleshooting de Accessibility Testing](https://qapractices.com/es/documentation/accessibility-testing-troubleshooting/) de QAPractices.

## Archivos

| Archivo | Problema que resuelve |
|---|---|
| `contrast-tokens.css` | Design tokens con contraste verificado WCAG 2.2 AA + helper `.sr-only` (Problema 1) |
| `aria-labels.html` | Nombres accesibles para botones de solo icono y etiquetas de formulario (Problema 2) |
| `live-regions.html` | Patrones `aria-live` / `role="alert"` para contenido dinámico (Problema 4) |
| `focus-trap.js` | Trampa de foco en JS vanilla para diálogos modales (Problema 3) |
| `spa-focus.ts` | Gestión de foco con `NavigationEnd` de Angular para SPAs (Problema 5) |

## Uso

- `focus-trap.js`: llama `trapFocus(dialogElement)` al abrir un modal; devuelve el foco con `triggerElement.focus()` al cerrarlo.
- `spa-focus.ts`: incorpora la suscripción a `NavigationEnd` en tu componente raíz para que cada cambio de ruta mueva el foco al `h1`.
- `contrast-tokens.css`: verifica la relación de cada token con un comprobador de contraste antes de publicar; los comentarios listan las relaciones medidas sobre blanco.

Sin dependencias — todo corre en el navegador tal cual, salvo `spa-focus.ts`, que necesita `@angular/router` y `rxjs`.
