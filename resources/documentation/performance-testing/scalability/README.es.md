# Companion de Pruebas de Escalabilidad

Archivos ejecutables de la guía de QAPractices [Guía de Pruebas de Escalabilidad](https://qapractices.com/es/documentation/scalability/) ([English version](https://qapractices.com/documentation/scalability/)).

## Contenido

| Archivo | Propósito |
|---|---|
| `scalability-test.js` | Script de k6 v2.3 con carga escalonada: rampas a 100 → 500 → 1.000 → 2.000 → 5.000 VUs con mesetas de 10 minutos para ubicar el punto de saturación. |
| `hpa.yaml` | HorizontalPodAutoscaler de Kubernetes (`autoscaling/v2`, Kubernetes 1.26+) que escala por CPU al 70% más una métrica de requests por pod. |
| `observe-scaling.sh` | Aplica el HPA, corre la prueba de k6 en segundo plano y observa la reacción del autoescalador con `kubectl get hpa --watch`. |

## Requisitos

- [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/) v2.3 o más reciente.
- `kubectl` 1.26+ con acceso a un clúster que corra la app a escalar.
- Para la métrica `http_requests_per_second` por pod en `hpa.yaml`: un adaptador de métricas como el [Prometheus Adapter](https://github.com/kubernetes-sigs/prometheus-adapter). Sin adaptador, quitá el bloque de métrica `Pods` y dejá solo la de CPU.

## Uso

```bash
# 1. Apuntar el script a tu entorno de staging
export BASE_URL=https://staging.qapractices.com

# 2. Correr la prueba de carga escalonada (~66 minutos en total)
k6 run scalability-test.js

# 3. En Kubernetes, aplicar el autoescalador y observar la reacción
chmod +x observe-scaling.sh
./observe-scaling.sh
```

El escalón donde el throughput deja de crecer mientras los VUs siguen subiendo es el punto de saturación. Registrá latencia P95/P99, tasa de errores y CPU por nodo en cada meseta — esos son los datos que una prueba de escalabilidad existe para producir.
