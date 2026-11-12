# QA Metrics and KPIs — Companion

Este companion provee archivos ejecutables para la guía [Métricas y KPIs de QA: Qué Medir y Por Qué](https://qapractices.com/es/documentation/qa-metrics-kpis).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `data/bugs.csv` | Export de bug tracker de ejemplo (60 filas: environment, priority, module, fechas creado/cerrado) |
| `scripts/metrics_report.py` | Calcula defect escape rate y MTTR para defectos P1/P2 |
| `scripts/defect_density.py` | Densidad de defectos por módulo (defectos por KLOC) — el detector de hotspots |
| `requirements.txt` | solo `pandas` |

## Inicio Rápido

```bash
pip install -r requirements.txt
python scripts/metrics_report.py
python scripts/defect_density.py
```

Salida esperada (con los datos de ejemplo):

```text
Defect Escape Rate: 20.0%  (12/60 bugs llegaron a producción)
MTTR (P1/P2): 1.6 días  (n=43)

Density by module:
  auth       3.38 defectos/KLOC (27 defectos)  <- hotspot
  profile    1.33 defectos/KLOC (8 defectos)   <- hotspot
  checkout   0.87 defectos/KLOC (13 defectos)
  search     0.55 defectos/KLOC (12 defectos)
```

## Notas

Cambia `data/bugs.csv` por un export real de Jira, Linear o Azure DevOps —
mantén los mismos nombres de columna (`environment`, `priority`, `module`,
`created_date`, `closed_date`) y ambos scripts funcionan sin cambios.

Los números del escenario NorthLoop de la guía son ilustrativos; estos
archivos son la maquinaria real y ejecutable detrás del dashboard.
