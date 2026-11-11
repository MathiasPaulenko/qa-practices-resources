# Guía de Testing en Kubernetes — Companion

Manifiestos y scripts ejecutables de la guía
[Guía de Testing en Kubernetes: Apps y Clusters](https://qapractices.com/es/documentation/kubernetes-testing-guide).

## Archivos

| Archivo | Sección | Qué hace |
|---|---|---|
| `pod-with-probes.yaml` | §1, §7, §8 | Deployment con los tres probes, hook `preStop`, `securityContext` endurecido (no-root, FS de solo lectura, drop ALL caps), requests/límites + un `PodDisruptionBudget` |
| `kind-ci-cluster.sh` | Clusters Locales y de CI | Levanta un cluster `kindest/node` fijado por versión, despliega el demo de probes y corre un smoke check de endpoints; se desmonta al salir |
| `hpa-load-test.sh` | §5 | Verifica metrics-server, lanza un pod de carga fortio 1.x con concurrencia sostenida y observa al HPA reaccionar |
| `helm-test-pod.yaml` | §6 | Manifiesto de Pod de test de Helm (`helm.sh/hook: test`) para copiar en `templates/tests/` |

## Uso

```bash
# Cluster descartable + smoke test (necesita kind 0.20+, kubectl 1.28+, docker)
bash kind-ci-cluster.sh

# Probes + PDB en un cluster existente
kubectl apply -f pod-with-probes.yaml
kubectl rollout status deployment/probe-demo

# HPA bajo carga (necesita metrics-server + un HPA sobre $SERVICE)
SERVICE=my-service NAMESPACE=staging bash hpa-load-test.sh

# Test de Helm — copiar primero dentro de tu chart
cp helm-test-pod.yaml my-chart/templates/tests/test-connection.yaml
helm test my-release
```

Notas:

- `kindest/node:v1.30.0` en `kind-ci-cluster.sh` está fijado como ejemplo — definí `NODE_IMAGE` con tu versión de Kubernetes en producción.
- Los paths de los probes (`/health/*`) siguen los ejemplos de la guía; apuntalos a los endpoints reales de tu app.
- `helm-test-pod.yaml` usa los helpers `my-chart.fullname` / `my-chart.labels` — renombralos según el `_helpers.tpl` de tu chart.
