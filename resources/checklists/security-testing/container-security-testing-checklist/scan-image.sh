#!/usr/bin/env bash
# Container Security Testing — Image Scan Script
# Usage: ./scan-image.sh <image:tag>
# Requires: trivy 0.74.0+
set -euo pipefail

IMAGE="${1:?Usage: scan-image.sh <image:tag>}"
SEVERITY="${2:-HIGH,CRITICAL}"
OUTPUT_DIR="${3:-./evidence}"

mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT="$OUTPUT_DIR/scan-${TIMESTAMP}.txt"

echo "Scanning $IMAGE for $SEVERITY vulnerabilities..."
trivy image --severity "$SEVERITY" --exit-code 1 --format table "$IMAGE" 2>&1 | tee "$REPORT"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
  echo "PASS: No $SEVERITY vulnerabilities found in $IMAGE"
  echo "Report saved to $REPORT"
else
  echo "FAIL: $SEVERITY vulnerabilities found in $IMAGE"
  echo "Report saved to $REPORT"
  exit 1
fi
