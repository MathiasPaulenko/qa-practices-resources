#!/usr/bin/env bash
# Container Security Testing — Image Signature Verification
# Usage: ./verify-signature.sh <image:tag> <cosign-key>
# Requires: cosign 2.6.5+
set -euo pipefail

IMAGE="${1:?Usage: verify-signature.sh <image:tag> <cosign-key>}"
KEY="${2:?Usage: verify-signature.sh <image:tag> <cosign-key>}"
OUTPUT_DIR="${3:-./evidence}"

mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT="$OUTPUT_DIR/signature-${TIMESTAMP}.txt"

echo "Verifying signature for $IMAGE with key $KEY..."
if cosign verify --key "$KEY" "$IMAGE" 2>&1 | tee "$REPORT"; then
  echo "PASS: Signature verified for $IMAGE"
  echo "Report saved to $REPORT"
else
  echo "FAIL: Signature verification failed for $IMAGE"
  echo "Report saved to $REPORT"
  exit 1
fi
