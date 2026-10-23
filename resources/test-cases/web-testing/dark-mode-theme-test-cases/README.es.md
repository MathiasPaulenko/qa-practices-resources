# Casos de Prueba de Dark Mode y Cambio de Tema — Companion

Recurso companion de [Casos de Prueba de Dark Mode y Cambio de Tema](https://qapractices.com/es/test-cases/dark-mode-theme-test-cases/).

## Contenido

- `theme.mjs` — modelo de resolución de tema sin dependencias: preferencia guardada → `prefers-color-scheme` → tema por defecto, con fallback ante valores corruptos en vez de excepción. `ThemeStore` envuelve un `Map` compartido para que persistencia y sync entre pestañas sean testeables sin navegador.
- `contrast.mjs` — matemática de contraste WCAG 2.2 (sRGB → luminancia relativa → ratio de contraste) para las aserciones de SC 1.4.3 y SC 1.4.11.
- `scan-hardcoded.mjs` — detecta literales hex asignados a propiedades CSS reales, es decir, colores que saltan el sistema de tokens y quedan iguales en todos los temas.
- `tests/dark-mode.test.mjs` — subconjunto ejecutable de los casos del artículo: preferencia del sistema en primera visita (TC-001), guardado-vence-sistema (TC-002), persistencia (TC-003), fallback ante valor corrupto (TC-006), cobertura de tokens + scanner de hex (TC-007), contraste AA en ambos temas (TC-008), anillo de foco 3:1 (TC-009), orden de elevación en oscuro (TC-011), sync del OS en vivo sin override manual (TC-014) y sync de storage entre pestañas (TC-015).

## Requisitos

- Node.js 20+ (usa el runner `node:test` integrado — no necesita npm install)

## Uso

```bash
node --test tests/*.test.mjs
```

Salida esperada: `15 passed`.

Los casos a nivel de navegador (TC-004 toggle, TC-005 FOIT, TC-010 media, TC-012 impresión, TC-013 embeds, TC-016 colores forzados) se ejecutan como chequeos Playwright/manuales según el artículo — la spec del cuerpo del artículo cubre la aserción del toggle.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/dark-mode-theme-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/dark-mode-theme-test-cases/
- Companion de la checklist hermana: [dark-mode-theme-switching-testing-checklist](../../checklists/quality-assurance/dark-mode-theme-switching-testing-checklist) (spec Playwright de resolución/FOIT/toggle)
