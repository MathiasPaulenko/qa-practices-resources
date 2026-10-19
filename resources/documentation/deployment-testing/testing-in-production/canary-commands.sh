#!/usr/bin/env bash
# Manual operations for the checkout-api canary rollout (Argo Rollouts v1.8).
# Requires: kubectl + kubectl-argo-rollouts plugin.

set -euo pipefail

# Apply the manifests (AnalysisTemplate must exist before the rollout reaches it).
kubectl apply -f analysis-template.yaml
kubectl apply -f rollout.yaml

# Watch the rollout progress live.
kubectl argo rollouts get rollout checkout-api --watch

# Skip the current pause and continue to the next step.
kubectl argo rollouts promote checkout-api

# Abort the rollout and return all traffic to the stable version.
kubectl argo rollouts abort checkout-api
