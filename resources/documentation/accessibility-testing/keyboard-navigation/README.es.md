# Pruebas de Navegación por Teclado — Suite Playwright ejecutable

Repositorio companion de la guía de QAPractices
[Guía de Pruebas de Navegación por Teclado](https://qapractices.com/es/documentation/keyboard-navigation/)
([English version](https://qapractices.com/documentation/keyboard-navigation/)).

Autocontenida: cada fixture se renderiza inline con `page.setContent()` — no
se necesita sitio externo ni backend.

## Estructura

```text
playwright/   @playwright/test 1.48.2
```

## Ejecutar

```bash
cd playwright
npm install
npx playwright test
```

La config usa `channel: 'chrome'` — corre sobre tu Chrome instalado, sin
descargar navegador. Para CI, quita la opción `channel` y corre
`npx playwright install chromium` para usar el navegador empaquetado.

## Qué cubre la suite

- **El orden de tabulación sigue el orden del DOM** — expectativa base.
- **`tabindex` positivo reordena el foco** — el anti-patrón a detectar en review.
- **Focus trap en modal** — Enter abre, Tab/Shift+Tab ciclan dentro, Escape
  cierra y devuelve el foco al activador.
- **Enlaces enfocables fuera de pantalla** — `left:-9999px` los deja alcanzables
  por Tab; demuestra un bug de teclado real.
- **Skip link** — primera parada de Tab, al activarse mueve el foco a `main`.

Los cinco tests pasan en Chrome estable con Playwright 1.48.
