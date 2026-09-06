# Lighthouse Performance Testing — Scripts Companion

Scripts companion para la [Guía de Lighthouse Performance Testing](https://qapractices.com/es/documentation/lighthouse-performance-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `scripts/lighthouserc.js` | Config de Lighthouse CI 0.14 con thresholds de performance, accesibilidad y SEO. |
| `scripts/lighthouse-ci-workflow.yml` | Workflow de GitHub Actions que corre Lighthouse CI en cada push. |
| `scripts/run-lighthouse-programmatic.js` | Script de Node.js que corre Lighthouse 12 programáticamente y loguea LCP, INP y performance score. |
| `scripts/web-vitals-collector.js` | Collector RUM de producción usando la librería `web-vitals` 4. |
| `scripts/assert-lighthouse.js` | Script de assert que falla un build si LCP excede 2500ms. |

## Uso

```bash
# Instalar dependencias
npm install -g lighthouse@12 @lhci/cli@0.14
npm install web-vitals@4 chrome-launcher lighthouse

# Correr Lighthouse CI
lhci autorun --config=scripts/lighthouserc.js

# Correr auditoría programática
node scripts/run-lighthouse-programmatic.js https://staging.qa.local

# Assert sobre una métrica específica
node scripts/assert-lighthouse.js ./report.json
```

## Requisitos

- Node.js 20+
- Lighthouse 12+
- Lighthouse CI 0.14+
- web-vitals 4+ (para collector RUM)
