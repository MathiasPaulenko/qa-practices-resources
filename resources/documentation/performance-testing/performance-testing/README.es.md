# Pruebas de Rendimiento: Fundamentos — Ejemplos ejecutables

Código compañero de [Pruebas de Rendimiento: Web Vitals y Presupuestos](https://qapractices.com/es/documentation/performance-testing/) ([en](https://qapractices.com/documentation/performance-testing/)).

## Contenido

| Archivo | Qué hace |
|---|---|
| `lighthouse-budget.json` | Presupuestos de rendimiento: tamaños de recursos (script/image/document/font/stylesheet), conteo de terceros, timings LCP e interactivo |
| `check-budget.js` | Script de Node sin dependencias que verifica un reporte JSON de Lighthouse contra el presupuesto y sale con error si se viola alguna regla |
| `sample-report.json` | Reporte mínimo con la forma del resultado de Lighthouse; viola dos presupuestos a propósito para que veas la salida de fallo |
| `web-vitals-collector.js` | Colector RUM de LCP/INP/CLS con `web-vitals` 5.x (API `on*`) y sendBeacon |
| `github-actions/perf.yml` | Gate de CI: Lighthouse CI con el presupuesto, más una alternativa sin token usando `check-budget.js` |

## Inicio rápido

Verificá el reporte de ejemplo contra el presupuesto (sin instalar Lighthouse):

```bash
node check-budget.js sample-report.json lighthouse-budget.json
```

Salida esperada — el ejemplo viola `size:script` (380 KB > 300) y `timing:largest-contentful-paint` (3100 ms > 2500):

```text
PASS  size:document                41 KB  (budget 50 KB)
FAIL  size:script                  380 KB  (budget 300 KB)
PASS  size:image                   402 KB  (budget 500 KB)
PASS  size:font                    86 KB   (budget 100 KB)
PASS  size:stylesheet              57 KB   (budget 60 KB)
PASS  count:third-party            3 items (budget 10 items)
FAIL  timing:largest-contentful-paint 3100 ms (budget 2500 ms)
PASS  timing:interactive           2800 ms (budget 3500 ms)

2 budget(s) breached.
```

Verificar un reporte real:

```bash
npx lighthouse https://staging.tu-app.example --output=json --output-path=./report.json
node check-budget.js ./report.json ./lighthouse-budget.json
```

Requiere Node 18+; sin dependencias de npm.

## Colector web-vitals

```bash
npm install web-vitals@^5
```

Importá `web-vitals-collector.js` desde el entry point de tu app y apuntá `ENDPOINT` a tu colector de analytics.
