# Chaos Engineering Guide — Companion

Este companion provee archivos ejecutables para la guía [Guía de Chaos Engineering](https://qapractices.com/es/documentation/chaos-engineering-testing-guide).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `chaos-experiments/pod-delete.yaml` | Litmus 3.31 ChaosEngine para experimento pod-delete |
| `chaos-experiments/network-latency.yaml` | Chaos Mesh 2.8.4 NetworkChaos para inyección de latencia de red |
| `scripts/verify-steady-state.sh` | Script de shell para verificar steady-state antes y después de experimentos |
| `.github/workflows/chaos.yml` | Workflow de GitHub Actions para experimentos semanales en staging |

## Inicio Rápido

```bash
# Aplicar experimento de Litmus
kubectl apply -f chaos-experiments/pod-delete.yaml
kubectl wait --for=condition=Completed chaosengine/payments-staging-chaos -n litmus --timeout=120s

# Aplicar experimento de Chaos Mesh
kubectl apply -f chaos-experiments/network-latency.yaml

# Verificar steady-state
bash scripts/verify-steady-state.sh
```

## Integración CI

El workflow de GitHub Actions corre semanalmente los lunes a las 3 AM en staging. Verifica steady-state, corre el experimento de Litmus y verifica la recuperación.