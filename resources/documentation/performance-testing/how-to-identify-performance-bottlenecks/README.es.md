# Identificar Cuellos de Botella — Companion

Artefactos ejecutables para [Cómo Identificar Cuellos de Botella de Performance](https://qapractices.com/es/documentation/how-to-identify-performance-bottlenecks/) de QAPractices.

## Contenido

| Archivo | Propósito | Sección relacionada |
|---|---|---|
| `scripts/k6-load-isolation.js` | Cargar la app mientras mirás las métricas de cada capa — la que se degrada primero es el cuello | Checklists por Capa |
| `scripts/pg_stat_statements-top-queries.sql` | Encontrar las queries más lentas y frecuentes de PostgreSQL | Base de Datos |
| `scripts/web-vitals-rum.js` | Recolectar LCP/INP/CLS/FCP/TTFB de usuarios reales hacia tu endpoint | Frontend |

## Requisitos

- k6 (https://k6.io/docs/get-started/installation/) para el script de carga.
- PostgreSQL 15+ con `pg_stat_statements` habilitado para el SQL.
- `web-vitals` 4.x instalado para el snippet de RUM.

## Uso

```bash
# Aislar la capa bajo carga
k6 run scripts/k6-load-isolation.js

# Encontrar queries lentas
psql -d tu_db -f scripts/pg_stat_statements-top-queries.sql

# Recolectar Web Vitals en producción
# agregar scripts/web-vitals-rum.js a tu bundle
```

English version: [README.md](README.md)
