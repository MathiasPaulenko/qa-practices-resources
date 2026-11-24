# Checklist de Preparación para Producción — Companion

Companion ejecutable de la [Checklist de Preparación para Producción](https://qapractices.com/es/checklists/production-readiness-testing-checklist).

## Contenido

- `release_gate_workflow.yml` — puerta go/no-go en GitHub Actions: identidad del artefacto, suite smoke en producción, cobertura de monitoreo/alertas, compatibilidad de rollback de migraciones, antigüedad del drill y margen de capacidad. Cada paso bloquea el release si falla.
- `rollback_drill.sh` — script de simulacro de rollback: cronometra cada paso del runbook (revertir artefacto, contrato de esquema, smoke, alertas) y registra resultados; también sirve como puerta CI de antigüedad (`--check-recency --max-days 90`).

## Uso

```bash
# Ensayar el rollback en staging y medir el tiempo real
./rollback_drill.sh --rehearse staging

# Puerta CI: bloquear el release si el último drill tiene más de 90 días
./rollback_drill.sh --check-recency --max-days 90
```

El workflow asume scripts auxiliares (`check_alert_coverage.py`, `check_migration_compat.py`, `check_capacity.py`) — impleméntalos contra tu tooling de observabilidad y migraciones, o reemplaza los pasos por equivalentes.
