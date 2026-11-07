#!/usr/bin/env bash
# Post-deploy health check — verifies the health endpoint returns 200
# and required components report "up".
#
# Usage:
#   BASE_URL=https://api.yourdomain.com ./health-check.sh
#
# Requires: curl, jq
set -euo pipefail

BASE_URL="${BASE_URL:?Set BASE_URL to your API host, e.g. https://api.yourdomain.com}"

echo "Checking $BASE_URL/health ..."
response=$(curl -fsS "$BASE_URL/health" -H "Accept: application/json")
echo "$response" | jq .

status=$(echo "$response" | jq -r '.status')
if [ "$status" != "healthy" ]; then
  echo "FAIL: status is '$status', expected 'healthy'"
  exit 1
fi

# Verify each required component is up
for component in database cache; do
  value=$(echo "$response" | jq -r ".$component // \"missing\"")
  if [ "$value" != "up" ]; then
    echo "FAIL: component '$component' is '$value'"
    exit 1
  fi
done

echo "PASS: health endpoint healthy, all components up."
