#!/usr/bin/env bash
# Retry a flaky suite up to 3 times — no third-party action needed (Q15)
# Companion file for: https://qapractices.com/documentation/devops-interview-questions-qa
# Usage in CI: bash retry-flaky.sh
set -u

attempt=1
max=3

until npm test; do
  if [ "$attempt" -eq "$max" ]; then
    echo "Still failing after $max attempts — this is a real failure, not flakiness"
    exit 1
  fi
  echo "Retry $attempt/$max — resetting test DB"
  npm run reset:db
  attempt=$((attempt + 1))
done
