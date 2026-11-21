#!/usr/bin/env bash
# Runs one Jest spec 10 times and prints how many runs failed.
# Usage: ./scripts/flaky_test_check.sh src/components/checkout.test.js
set -u

SPEC="${1:?usage: $0 <path-to-spec>}"

# Serial run first: surfaces ordering issues and open-handle leaks
npx jest --runInBand --detectOpenHandles "$SPEC"

failures=0
for i in {1..10}; do
  npx jest "$SPEC" --silent || { failures=$((failures + 1)); echo "FAILED run $i"; }
done

echo "flaky failures: $failures/10"
