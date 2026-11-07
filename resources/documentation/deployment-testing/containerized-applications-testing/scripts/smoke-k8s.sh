#!/usr/bin/env bash
# Smoke test from the guide: wait for readiness, then hit the service
# through cluster DNS from a throwaway curl pod.
set -euo pipefail

NS=qa

kubectl create namespace "$NS" --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n "$NS" -f k8s/

kubectl wait --for=condition=ready pod -l app=web -n "$NS" --timeout=90s

kubectl run smoke -n "$NS" --image=curlimages/curl:8.23.0 --rm -i --restart=Never -- \
  curl -sf --retry 10 --retry-delay 2 http://web.qa.svc.cluster.local/health

kubectl delete namespace "$NS" --ignore-not-found
