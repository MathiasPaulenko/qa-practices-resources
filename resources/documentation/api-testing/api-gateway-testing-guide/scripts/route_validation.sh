#!/bin/bash
# Route validation for API gateway

BASE="https://api.staging.local"

echo "=== Exact path match ==="
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/api/v1/users"

echo "=== Path prefix match ==="
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/api/v1/users/123"

echo "=== Method restriction (DELETE should fail) ==="
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE "$BASE/api/v1/users/123"

echo "=== Wildcard path ==="
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/api/v1/users/123/orders"