# Testing in Production — Canary Rollout Companion

Kubernetes manifests and commands for the canary deployment example from
[How to Test in Production Safely](https://qapractices.com/documentation/testing-in-production/).

## What's inside

- `rollout.yaml` — an Argo Rollouts `Rollout` for `checkout-api` that steps canary
  traffic through 5% → 25% → 50% with pauses, and runs a metric analysis before
  continuing past 25%.
- `analysis-template.yaml` — an `AnalysisTemplate` named `canary-health` that fails
  the rollout if the 5xx rate measured by Prometheus stays above 1% for two
  consecutive one-minute intervals.
- `canary-commands.sh` — the `kubectl argo rollouts` operations for watching,
  promoting and aborting the rollout.

## Requirements

- A Kubernetes cluster (kind, minikube or a real cluster).
- [Argo Rollouts](https://argo-rollouts.readthedocs.io/en/stable/) v1.8 installed
  in the cluster, plus the `kubectl argo rollouts` plugin.
- A Prometheus instance reachable at `http://prometheus.monitoring:9090`
  (adjust the `address` field in `analysis-template.yaml` to your setup).
- Your own container image — `registry.internal/checkout-api:2.4.1` is a
  placeholder; replace it with yours.

## Usage

```bash
kubectl apply -f analysis-template.yaml
kubectl apply -f rollout.yaml
kubectl argo rollouts get rollout checkout-api --watch
```

If the Prometheus gate fails twice, the rollout aborts automatically and traffic
returns to the stable version. To drive it manually, use the commands in
`canary-commands.sh`.
