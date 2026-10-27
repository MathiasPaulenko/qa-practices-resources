# Casos de Prueba de Diseño Responsive — companion Playwright

Companion de [Casos de Prueba de Diseño Responsive: Breakpoints y Viewport](https://qapractices.com/es/test-cases/responsive-design-test-cases/).

- `responsive-fixture.html` — una página con breakpoint real en 768px: botón `.hamburger` abajo, `.desktop-nav` arriba, más una tabla de 8 columnas dentro de `overflow-x: auto`.
- `responsive.spec.ts` — spec de matriz de viewports de Playwright 1.48 cubriendo TC-01/10 (colapso del nav en N-1/N/N+1) y TC-05/06 (sin scroll horizontal en el body a 320px).

## Ejecutar

```bash
npm install
npx playwright install chromium   # primera vez
npm test
```

Los 7 tests pasan tal cual. Rompé el fixture a propósito — p. ej., quitá `overflow-x: auto` — y mirá cómo falla la aserción de scroll (eso es TC-06 detectando un bug real).
