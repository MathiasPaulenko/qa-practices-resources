# Guía de Pruebas de Rendimiento — Companion

Archivos companion para la [Guía de Pruebas de Rendimiento: Tipos y Planificación](https://qapractices.com/es/documentation/performance-testing-guide).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `product-load-test.js` | Prueba de carga k6: sube a 100 VUs, estado estable, umbrales p95 < 500ms y tasa de error < 1%. |

## Requisitos

- k6 v0.51.0 (`k6 version`) o Docker para `grafana/k6:0.51.0`

## Uso

1. Apunta el script a tu staging (reemplaza `https://staging.qapractices.com/api/v1/products`).
2. Corre localmente: `k6 run product-load-test.js`.
3. Corre en Docker: `docker run --rm -v $(pwd):/k6 grafana/k6:0.51.0 run /k6/product-load-test.js`.
4. Ajusta `stages` y `thresholds` a tu SLA antes de gatear el CI con los resultados.

## Integración en CI

```yaml
- run: docker run --rm -v ${{ github.workspace }}:/k6 grafana/k6:0.51.0 run /k6/product-load-test.js
```
