#!/bin/bash
# TLS validation for API gateway

BASE="https://api.staging.local"

echo "=== Reject old TLS (1.0) ==="
curl -s -o /dev/null -w "%{http_code}\n" --tls-max 1.0 "$BASE/api/v1/health"

echo "=== Check certificate and security headers ==="
curl -i -v "$BASE/api/v1/health" 2>&1 | grep -E "(SSL certificate|Strict-Transport-Security|X-Frame-Options|Content-Security-Policy)"

echo "=== HTTP to HTTPS redirect ==="
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "http://api.staging.local/api/v1/health"