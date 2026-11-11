# Kubernetes Testing Guide — Companion

Runnable manifests and scripts from the guide
[Kubernetes Testing Guide: Containerized Apps & Cluster](https://qapractices.com/documentation/kubernetes-testing-guide).

## Files

| File | Section | What it does |
|---|---|---|
| `pod-with-probes.yaml` | §1, §7, §8 | Deployment with all three probes, preStop hook, hardened `securityContext` (non-root, read-only FS, drop ALL caps), resource requests/limits + a `PodDisruptionBudget` |
| `kind-ci-cluster.sh` | Local and CI Clusters | Spins up a pinned `kindest/node` cluster, deploys the probe demo and runs an endpoint smoke check; tears down on exit |
| `hpa-load-test.sh` | §5 | Checks metrics-server, launches a fortio 1.x load pod with sustained concurrency and watches the HPA react |
| `helm-test-pod.yaml` | §6 | Helm test Pod manifest (`helm.sh/hook: test`) to drop into `templates/tests/` |

## Usage

```bash
# Disposable cluster + smoke test (needs kind 0.20+, kubectl 1.28+, docker)
bash kind-ci-cluster.sh

# Probes + PDB on an existing cluster
kubectl apply -f pod-with-probes.yaml
kubectl rollout status deployment/probe-demo

# HPA under load (needs metrics-server + an HPA on $SERVICE)
SERVICE=my-service NAMESPACE=staging bash hpa-load-test.sh

# Helm test — copy into your chart first
cp helm-test-pod.yaml my-chart/templates/tests/test-connection.yaml
helm test my-release
```

Notes:

- `kindest/node:v1.30.0` in `kind-ci-cluster.sh` is pinned as an example — set `NODE_IMAGE` to your production Kubernetes version.
- The probe paths (`/health/*`) match the guide's examples; point them at your app's real endpoints.
- `helm-test-pod.yaml` uses `my-chart.fullname` / `my-chart.labels` template helpers — rename to match your chart's `_helpers.tpl`.
