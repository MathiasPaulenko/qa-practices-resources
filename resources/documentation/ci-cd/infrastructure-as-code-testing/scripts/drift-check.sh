#!/usr/bin/env bash
# Minimal drift check — run on a schedule (cron or CI).
# terraform plan -detailed-exitcode: 0 = no changes, 1 = error, 2 = drift.
set -euo pipefail

cd "$(dirname "$0")/../terraform" 2>/dev/null || true

terraform plan -detailed-exitcode > /dev/null || status=$?
status=${status:-0}

if [ "$status" -eq 2 ]; then
  echo "Drift detected: infrastructure changed outside of Terraform."
  exit 1
elif [ "$status" -eq 1 ]; then
  echo "terraform plan errored — check credentials and state lock."
  exit 1
fi

echo "No drift detected."
