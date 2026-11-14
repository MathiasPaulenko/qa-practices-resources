#!/usr/bin/env bash
# Fail if pipeline logs contain unmasked credential assignments.
# Usage: check-unmasked-secrets.sh <logs-dir>
set -euo pipefail

LOGS_DIR="${1:-./logs}"

if grep -rEl '(password|api[_-]?key|token)\s*[:=]\s*[^\s]+' "$LOGS_DIR" 2>/dev/null; then
  echo "ERROR: unmasked credential-like strings found in pipeline logs" >&2
  exit 1
fi

echo "OK: no unmasked secrets found in $LOGS_DIR"
