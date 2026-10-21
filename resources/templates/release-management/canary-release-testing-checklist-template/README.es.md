# Checklist de Testing de Canary Release — Companion Ejecutable

Companion de la [Plantilla de Checklist de Testing de Canary Release](https://qapractices.com/es/templates/canary-release-testing-checklist-template/) ([EN](https://qapractices.com/templates/canary-release-testing-checklist-template/)).

Artefactos funcionales para la lógica de gates por etapa del checklist, listos para adaptar a un setup real de Argo Rollouts.

## Contenido

| Archivo | Propósito |
|---|---|
| `rollout.yaml` | Manifiesto de Argo Rollouts 1.8 con las etapas del checklist (5 → 10 → 25 → 50 → 100) y análisis por etapa |
| `analysis-template.yaml` | AnalysisTemplate con queries de Prometheus: volumen de peticiones, delta de error rate, delta de p95 — los datos ausentes cuentan como fallo |
| `evaluate-stage.mjs` | Evaluador de gates en Node 20+ que implementa las reglas del checklist: deltas contra baseline de la misma ventana, suelos absolutos, mínimo de peticiones, datos ausentes = fallo |
| `tests/evaluate-stage.test.mjs` | Suite `node:test` que cubre las decisiones promote / hold / rollback |

## Correr los tests

```bash
node --test tests/*.test.mjs
```

Los 7 tests deben pasar — cubren los modos de fallo que el checklist advierte: baselines rotos que pasan los deltas, canaries de poco tráfico que promueven con ruido, y gaps de métricas leídos como cero errores.

## Usar el evaluador por separado

```bash
node evaluate-stage.mjs baseline.json canary.json
# imprime PROMOTE | HOLD | ROLLBACK con una razón, exit code 0 solo en PROMOTE
```

Ambos JSON tienen la forma `{"errorRate": 0.0028, "p95Ms": 120, "requests": 1250}`.

## Notas

- El YAML apunta a Argo Rollouts 1.8 + Istio 1.27 + Prometheus 3.x sobre Kubernetes 1.34 — ajusta nombres y direcciones a tu entorno.
- Las queries PromQL comparan la cohorte canary contra la cohorte estable medida en la misma ventana, como exige la regla de baseline del checklist.
- `evaluate-stage.mjs` trata deliberadamente las métricas ausentes como gate fallido; un gap en Prometheus no es un certificado de salud.
