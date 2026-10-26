# Scalability Testing Companion

Runnable files for the QAPractices guide [Scalability Testing Guide](https://qapractices.com/documentation/scalability/) ([versión en español](https://qapractices.com/es/documentation/scalability/)).

## Contents

| File | Purpose |
|---|---|
| `scalability-test.js` | k6 v2.3 stepped-load script: ramps to 100 → 500 → 1,000 → 2,000 → 5,000 VUs with 10-minute holds at each plateau to locate the saturation point. |
| `hpa.yaml` | Kubernetes HorizontalPodAutoscaler (`autoscaling/v2`, Kubernetes 1.26+) scaling on CPU at 70% plus a per-pod request-rate metric. |
| `observe-scaling.sh` | Applies the HPA, runs the k6 test in the background and watches the autoscaler react with `kubectl get hpa --watch`. |

## Requirements

- [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/) v2.3 or newer.
- `kubectl` 1.26+ with access to a cluster running the app you want to scale.
- For the `http_requests_per_second` pod metric in `hpa.yaml`: a metrics adapter such as the [Prometheus Adapter](https://github.com/kubernetes-sigs/prometheus-adapter). With no adapter installed, drop the `Pods` metric block and keep the CPU metric only.

## Usage

```bash
# 1. Point the script at your staging environment
export BASE_URL=https://staging.qapractices.com

# 2. Run the stepped load test (~66 minutes total)
k6 run scalability-test.js

# 3. On Kubernetes, apply the autoscaler and watch it react instead
chmod +x observe-scaling.sh
./observe-scaling.sh
```

The stage where throughput stops growing while VUs keep climbing is the saturation point. Record P95/P99 latency, error rate and per-node CPU at each plateau — that is the data a scalability test exists to produce.
