# Chaos Engineering Guide — Companion

This companion provides runnable files for the [Chaos Engineering Guide](https://qapractices.com/documentation/chaos-engineering-testing-guide) guide.

## Files

| File | Purpose |
|------|---------|
| `chaos-experiments/pod-delete.yaml` | Litmus 3.31 ChaosEngine for pod-delete experiment |
| `chaos-experiments/network-latency.yaml` | Chaos Mesh 2.8.4 NetworkChaos for network latency injection |
| `scripts/verify-steady-state.sh` | Shell script to verify steady-state before and after experiments |
| `.github/workflows/chaos.yml` | GitHub Actions workflow for weekly chaos experiments in staging |

## Quick Start

```bash
# Apply Litmus experiment
kubectl apply -f chaos-experiments/pod-delete.yaml
kubectl wait --for=condition=Completed chaosengine/payments-staging-chaos -n litmus --timeout=120s

# Apply Chaos Mesh experiment
kubectl apply -f chaos-experiments/network-latency.yaml

# Verify steady-state
bash scripts/verify-steady-state.sh
```

## CI Integration

The GitHub Actions workflow runs weekly on Monday 3 AM in staging. It verifies steady-state, runs the Litmus experiment, and verifies recovery.