# Testing de iframes y Widgets de Terceros — companion Playwright

Companion de [Casos de Prueba de iframes y Widgets de Terceros](https://qapractices.com/es/test-cases/iframe-third-party-widget-testing/).

- `fixture-widget.html` — el "widget de terceros": una página que postea mensajes al padre.
- `fixture-host.html` — la página host: iframe en sandbox + allowlist de `event.origin` (acepta `null` para el demo `file://`; cambialo por tu origen real del widget).
- `hostile-embed.html` — embed con overlay transparente para el caso TC-04 de clickjacking.
- `iframe.spec.ts` — specs de Playwright 1.48 para TC-01/07 (sandbox + title) y TC-02 (origen forjado rechazado, legítimo aceptado).

## Ejecutar

```bash
npm install
npx playwright install chromium   # primera vez
npm test
```

Para testear en un origen real (y verificar `X-Frame-Options`/`frame-ancestors` del TC-04), serví la carpeta (`npx serve .`) en lugar de `file://` — el embed hostil choca así contra headers reales.
