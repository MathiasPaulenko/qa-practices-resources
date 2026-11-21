# Testing de Core Web Vitals — Lighthouse CI + Snippets RUM

Companion de la [Guía de Testing de Core Web Vitals: Lab, Field y CI/CD](https://qapractices.com/es/documentation/core-web-vitals-testing-guide/).

Una puerta de CWV mínima y ejecutable: Lighthouse CI evalúa los budgets de LCP y CLS en cada pull request, y el snippet de `web-vitals` envía métricas de usuarios reales desde producción.

## Archivos

```text
lighthouserc.json    # config de @lhci/cli 0.16: URLs, 3 ejecuciones, aserciones LCP/CLS/TBT
lighthouse-ci.yml    # workflow de GitHub Actions que corre `lhci autorun` en PRs
cwv-report.js        # colector RUM con web-vitals 6.x (onLCP/onINP/onCLS)
```

## Inicio rápido

```bash
npm install -D @lhci/cli@0.16.0
# Apunta lighthouserc.json a tus URLs de staging/preview primero (placeholders)
npx lhci autorun
```

Para GitHub Actions: copia `lighthouse-ci.yml` a `.github/workflows/` y configura el secret `LHCI_GITHUB_APP_TOKEN`, o elimina el bloque env para omitir los comentarios de estado.

Para RUM: integra `cwv-report.js` (npm `web-vitals@^6`) y apunta `sendBeacon` a tu propio endpoint de analytics — `/rum` en el snippet es una ruta de placeholder.

## Versiones

- @lhci/cli: 0.16.x
- Lighthouse: 12.x (incluido con @lhci/cli)
- web-vitals: 6.x
- Node.js: 20 (GitHub Actions)
