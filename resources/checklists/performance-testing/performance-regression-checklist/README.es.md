# Checklist de Regresión de Rendimiento — Companion

Artefactos ejecutables para la [Checklist de Regresión de Rendimiento](https://qapractices.com/es/checklists/performance-regression-checklist/) de QAPractices.com.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `k6_thresholds.js` | Script de k6 con umbrales de p95 por endpoint, techo absoluto de tasa de error y piso de throughput — sale con error si se violan. |
| `compare_baseline.py` | Compara un JSON de métricas del candidato contra el baseline guardado; falla si la latencia retrocede >10% o se supera el techo de error. |
| `perf_gate_workflow.yml` | Puerta en GitHub Actions: corrida de warm-up, corrida medida, comparación contra baseline y subida de artefactos. |

## Inicio rápido

```bash
# 1. Corre la puerta de k6 directamente
k6 run --env BASE_URL=https://staging.example.internal k6_thresholds.js

# 2. Compara una corrida candidata contra el baseline guardado
python compare_baseline.py \
  --baseline baselines/v1.9.0.json \
  --candidate results/candidate.json \
  --max-degradation 0.10 --max-error-rate 0.005

# 3. Enchufa en CI
#    copia perf_gate_workflow.yml a .github/workflows/perf-gate.yml
```

## La regla que importa

Una puerta que nunca bloquea un deploy es decoración. Los umbrales deben ser más ajustados que el ruido de tu ambiente — mide primero la varianza entre corridas y pon las bandas por encima.
