# Testing de Performance Frontend con Lighthouse — Ejemplos ejecutables

Versiones ejecutables de los ejemplos de [Performance Frontend con Lighthouse: LCP, INP, CLS](https://qapractices.com/es/documentation/frontend-performance-testing-with-lighthouse/).

## Contenido

| Ruta | Qué hace |
|---|---|
| `scripts/lighthouse-audit.js` | Corre Lighthouse 12 a través de Puppeteer 24 e imprime el score de performance más las cinco métricas ponderadas. |
| `scripts/package.json` | Dependencias pinneadas: `lighthouse@12`, `puppeteer@24`. |
| `ci/lighthouserc.json` | Config de Lighthouse CI 0.14: 3 corridas por URL, performance ≥ 0.9, LCP ≤ 2500ms, CLS ≤ 0.1, warning de TBT en 300ms. |
| `ci/lighthouse-ci.yml` | Workflow de GitHub Actions que corre `treosh/lighthouse-ci-action@v12` en pull requests. |

## Uso

```bash
cd scripts
npm install
npm run audit -- https://staging.example.com
```

Para el gate de CI, copiá `ci/lighthouserc.json` a tu repo, apuntá `collect.url` a tu entorno de preview y ubicá `ci/lighthouse-ci.yml` en `.github/workflows/lighthouse-ci.yml`.

## Notas

- `numberOfRuns: 3` reporta la mediana por URL — una sola corrida es demasiado ruidosa para servir de gate.
- INP es una métrica de campo y nunca aparece en el score de lab; assertá `total-blocking-time` como su proxy.
- Ajustá los budgets a tu propio baseline antes de gatear en `error`.
