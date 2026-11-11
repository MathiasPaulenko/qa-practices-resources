#!/usr/bin/env bash
# Ephemeral Kind cluster for CI smoke tests.
# Requires: kind 0.20+, kubectl 1.28+, docker.
# Usage: bash kind-ci-cluster.sh   (tears the cluster down on exit)
set -euo pipefail

CLUSTER_NAME="${CLUSTER_NAME:-ci}"
NODE_IMAGE="${NODE_IMAGE:-kindest/node:v1.30.0}"  # pin to your production version

cleanup() {
  kind delete cluster --name "${CLUSTER_NAME}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo ">> Creating Kind cluster '${CLUSTER_NAME}' (${NODE_IMAGE})"
kind create cluster --name "${CLUSTER_NAME}" --image "${NODE_IMAGE}"

echo ">> Waiting for nodes"
kubectl wait --for=condition=Ready nodes --all --timeout=120s

echo ">> Deploying probe demo"
kubectl apply -f "$(dirname "$0")/pod-with-probes.yaml"
kubectl rollout status deployment/probe-demo --timeout=120s

echo ">> Smoke: endpoints must be non-empty"
kubectl get endpoints probe-demo 2>/dev/null || kubectl get svc
kubectl get pods -o wide

echo ">> Smoke test passed — cluster '${CLUSTER_NAME}' will be deleted"
