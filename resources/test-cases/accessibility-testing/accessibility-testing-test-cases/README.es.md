# Casos de Prueba de Accesibilidad — companion Playwright

Companion de [Casos de Prueba de Accesibilidad: Ejemplos WCAG](https://qapractices.com/es/test-cases/accessibility-testing-test-cases/).

- `fixture-modal.html` — un modal real con trampa de foco correcta según WCAG (patrón TC-A11Y-012): el foco entra al abrir, Tab cicla adentro, Escape cierra y devuelve el foco al disparador.
- `a11y.spec.ts` — la spec de Playwright 1.48 + `@axe-core/playwright` 4.10 del recurso, apuntando al fixture vía `file://` así no hace falta servidor.

## Ejecutar

```bash
npm install
npx playwright install chromium   # primera vez
npm test
```

Para ver una trampa *rota*, borrá el handler `keydown` del fixture y mirá cómo falla la aserción de fuga de foco — eso es TC-A11Y-002 detectando un bug real.
