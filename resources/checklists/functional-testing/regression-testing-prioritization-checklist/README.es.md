# Checklist de Priorización de Pruebas de Regresión — Companion

Companion ejecutable de la [Checklist de Priorización de Pruebas de Regresión](https://qapractices.com/es/checklists/regression-testing-prioritization-checklist).

## Contenido

- `prioritize_tests.py` — puntúa cada test de la suite desde impacto del cambio + historial de defectos + inestabilidad, asigna tiers must-run/should-run/can-skip y emite la lista ordenada con la línea de corte en tu presupuesto de tiempo.
- `sample_history.csv` — formato de ejemplo del historial (test, area, last_failed, fails_12w, flake_rate, runtime_s).

## Uso

```bash
git diff --name-only origin/main > changed.txt
python3 prioritize_tests.py changed.txt history.csv --budget-min 60
```

Alimenta `changed.txt` desde tu diff y `history.csv` desde tu export de resultados de CI. Meter historial de defectos real es lo que convierte esto de ordenar en priorizar.
