#!/usr/bin/env bash
# Container Security Testing — Kubernetes RBAC Check
# Usage: ./check-rbac.sh <namespace> <service-account>
# Requires: kubectl
set -euo pipefail

NAMESPACE="${1:?Usage: check-rbac.sh <namespace> <service-account>}"
SA="${2:?Usage: check-rbac.sh <namespace> <service-account>}"
OUTPUT_DIR="${3:-./evidence}"

mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT="$OUTPUT_DIR/rbac-${TIMESTAMP}.txt"

SA_FQN="system:serviceaccount:${NAMESPACE}:${SA}"

echo "Checking RBAC permissions for $SA_FQN..."
echo "=== RBAC Audit Report ===" > "$REPORT"
echo "Service Account: $SA_FQN" >> "$REPORT"
echo "Timestamp: $(date -u)" >> "$REPORT"
echo "" >> "$REPORT"

echo "--- Secrets access ---" | tee -a "$REPORT"
kubectl auth can-i list secrets --as="$SA_FQN" 2>&1 | tee -a "$REPORT"
kubectl auth can-i get secrets --as="$SA_FQN" 2>&1 | tee -a "$REPORT"
echo "" >> "$REPORT"

echo "--- Cluster-wide access ---" | tee -a "$REPORT"
kubectl auth can-i list pods --all-namespaces --as="$SA_FQN" 2>&1 | tee -a "$REPORT"
kubectl auth can-i create pods --all-namespaces --as="$SA_FQN" 2>&1 | tee -a "$REPORT"
echo "" >> "$REPORT"

echo "--- Privileged operations ---" | tee -a "$REPORT"
kubectl auth can-i create privilegedpods --as="$SA_FQN" 2>&1 | tee -a "$REPORT"
kubectl auth can-i exec into pods --as="$SA_FQN" 2>&1 | tee -a "$REPORT"
echo "" >> "$REPORT"

echo "Report saved to $REPORT"
echo "Review the report for any unexpected 'yes' answers."
