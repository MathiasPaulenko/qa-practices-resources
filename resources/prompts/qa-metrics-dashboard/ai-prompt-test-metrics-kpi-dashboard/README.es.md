# Prompt de IA: Dashboard de métricas y KPIs — pack de output de ejemplo

Companion del recurso de QAPractices [Prompt de IA: Dashboard de KPIs y métricas de pruebas](https://qapractices.com/es/prompts/ai-prompt-test-metrics-kpi-dashboard/).

El output de referencia que el prompt debería producir para el Example Input de la guía (equipo de API de salud: 4 QA, 12 devs, 2 SDETs, releases semanales, GitHub Actions, Playwright 1.42, Jira Cloud, Datadog, Grafana 10).

## Archivos

```text
├── grafana-dashboard.json   # Esqueleto de dashboard Grafana 10: 5 paneles, targets, umbrales, ventana de 4 semanas
├── executive-summary.md     # Resumen ejecutivo de una página completo según el template de la guía
├── meta.json
└── README.md
```

## Mapeo con la guía

| Sección de la guía | Archivo | Qué muestra |
|---|---|---|
| Ejemplo de Output — tabla de métricas | `grafana-dashboard.json` | Las 5 métricas como paneles de Grafana con umbrales y ventana de tendencia de 28 días |
| Ejemplo de Output — resumen ejecutivo | `executive-summary.md` | El formato narrativo: riesgos principales, acciones recomendadas, historia en lenguaje simple |

## Uso

Importa `grafana-dashboard.json` en Grafana (Dashboards → New → Import) y recablea los campos `expr` a tus fuentes reales — las expresiones son placeholders con forma de métricas de Jira/GitHub Actions/Datadog. `executive-summary.md` está pensado para copiar y rellenar por sprint.

## Notas

- Versiones alineadas con el artículo: Grafana 10, Playwright 1.42.
