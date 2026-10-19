# Testing en Producción — Companion de Canary Rollout

Manifiestos de Kubernetes y comandos para el ejemplo de canary deployment de
[Cómo Probar en Producción de Manera Segura](https://qapractices.com/es/documentation/testing-in-production/).

## Qué contiene

- `rollout.yaml` — un `Rollout` de Argo Rollouts para `checkout-api` que sube el
  tráfico canary por pasos 5% → 25% → 50% con pausas, y ejecuta un análisis de
  métricas antes de continuar más allá del 25%.
- `analysis-template.yaml` — un `AnalysisTemplate` llamado `canary-health` que
  hace fallar el rollout si la tasa de errores 5xx medida por Prometheus se mantiene
  por encima del 1% durante dos intervalos consecutivos de un minuto.
- `canary-commands.sh` — las operaciones de `kubectl argo rollouts` para observar,
  promover y abortar el rollout.

## Requisitos

- Un clúster de Kubernetes (kind, minikube o un clúster real).
- [Argo Rollouts](https://argo-rollouts.readthedocs.io/en/stable/) v1.8 instalado
  en el clúster, más el plugin `kubectl argo rollouts`.
- Una instancia de Prometheus alcanzable en `http://prometheus.monitoring:9090`
  (ajusta el campo `address` de `analysis-template.yaml` a tu setup).
- Tu propia imagen de contenedor — `registry.internal/checkout-api:2.4.1` es un
  placeholder; reemplázala por la tuya.

## Uso

```bash
kubectl apply -f analysis-template.yaml
kubectl apply -f rollout.yaml
kubectl argo rollouts get rollout checkout-api --watch
```

Si la compuerta de Prometheus falla dos veces, el rollout se aborta solo y el
tráfico vuelve a la versión estable. Para operarlo manualmente, usa los comandos
de `canary-commands.sh`.
