#!/usr/bin/env bash
# Drive sustained load so the HPA scales, then watch it react.
# Requires: kubectl 1.28+, a running HPA + Service named $SERVICE,
#           metrics-server installed in the cluster.
# Usage: SERVICE=my-service NAMESPACE=default bash hpa-load-test.sh
set -euo pipefail

SERVICE="${SERVICE:-my-service}"
NAMESPACE="${NAMESPACE:-default}"
CONCURRENCY="${CONCURRENCY:-100}"
DURATION="${DURATION:-120s}"

echo ">> Prereq check: metrics-server and CPU requests"
kubectl top pods -n "${NAMESPACE}" >/dev/null 2>&1 || {
  echo "!! metrics-server not reachable — HPA cannot read CPU metrics." >&2
  echo "   Minikube: minikube addons enable metrics-server | Kind: install it manually." >&2
  exit 1
}

echo ">> Starting fortio load generator (${CONCURRENCY} conns for ${DURATION})"
kubectl run load-test -n "${NAMESPACE}" --image=fortio/fortio:latest_release \
  --restart=Never -- load -c "${CONCURRENCY}" -t "${DURATION}" -qps 0 \
  "http://${SERVICE}.${NAMESPACE}.svc.cluster.local/endpoint"

echo ">> Watching HPA — Ctrl+C to stop (load continues in background)"
kubectl get hpa -n "${NAMESPACE}" --watch

echo ">> Load generator pod logs (rerun after the watch):"
echo "   kubectl logs load-test -n ${NAMESPACE}"
