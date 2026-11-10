# Testing de Performance Frontend — Budgets en CI y ejemplos de RUM

Compañero de [Testing de performance frontend: métricas y budgets](https://qapractices.com/es/documentation/frontend-performance-testing-guide/).

Un gate de budgets de performance mínimo y ejecutable: Lighthouse CI asserta los Core Web Vitals en cada pull request, y el snippet de `web-vitals` envía métricas de usuarios reales desde producción.

## Archivos

```text
ci/
├── lighthouserc.json        # Config de @lhci/cli 0.16: URLs, 3 corridas, assertions de budget
└── performance-budget.yml   # Workflow de GitHub Actions que corre `lhci autorun` en PRs
rum/
└── web-vitals.js            # Colector RUM de web-vitals 6.x (onLCP/onINP/onCLS/onFCP/onTTFB)
```

## Inicio rápido

```bash
npm install -g @lhci/cli@0.16
# Apuntá lighthouserc.json a tus URLs de preview/staging primero
lhci autorun --config=ci/lighthouserc.json
```

Para GitHub Actions: copiá `ci/performance-budget.yml` a `.github/workflows/` y configurá el secreto `LHCI_GITHUB_APP_TOKEN` (o quitá el bloque `env` para no comentar el estado).

Para RUM: buildeá `rum/web-vitals.js` (npm `web-vitals@^6`) y apuntá `sendBeacon` a tu propio endpoint de analytics — `/rum` en el snippet es una ruta placeholder.

## Versiones

| Pieza | Versión pinneada |
|---|---|
| @lhci/cli | 0.16.x |
| Lighthouse (bajo lhci) | 13.x |
| web-vitals | 6.x (API `on*`; `get*`/`onFID` eliminadas en v4/v5) |
| Node | 20+ |
