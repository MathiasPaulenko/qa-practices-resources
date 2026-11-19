#!/usr/bin/env bash
# Diff two API versions response-by-response to catch breaking changes.
# Usage: ./compare-api-versions.sh https://staging.example.com/api users/42 users/7
set -euo pipefail

BASE_URL="${1:?Usage: $0 <base-url> <path1> [path2 ...]}"
shift

for path in "$@"; do
  echo "=== $path ==="
  curl -sf "$BASE_URL/v1/$path" -o "/tmp/v1-${path//\//_}.json" || { echo "v1 request failed for $path"; continue; }
  curl -sf "$BASE_URL/v2/$path" -o "/tmp/v2-${path//\//_}.json" || { echo "v2 request failed for $path"; continue; }

  if diff -u "/tmp/v1-${path//\//_}.json" "/tmp/v2-${path//\//_}.json"; then
    echo "IDENTICAL — review manually anyway: a clean diff only proves field parity, not contract intent"
  else
    echo "DIFF FOUND — classify each change: breaking (rename/remove/type change) vs additive (new field/enum)"
  fi
  echo
done
