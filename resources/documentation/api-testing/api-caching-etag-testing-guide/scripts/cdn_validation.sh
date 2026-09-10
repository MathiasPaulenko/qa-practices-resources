#!/bin/bash
# CDN cache validation

CDN="https://cdn.staging.local/products/123"

echo "=== Three requests through CDN ==="
for i in 1 2 3; do
  echo "Request $i:"
  curl -s -o /dev/null -w "  HTTP %{http_code} | Time: %{time_total}s | Age: %{header_json}\n" \
    "$CDN"
done

echo ""
echo "=== Vary header check ==="
echo "Accept-Language: en"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -H "Accept-Language: en" \
  "$CDN"

echo "Accept-Language: es"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -H "Accept-Language: es" \
  "$CDN"

echo ""
echo "=== Cache-busting with query string ==="
curl -s -o /dev/null -w "  HTTP %{http_code} | Time: %{time_total}s\n" \
  "$CDN?bust=$(date +%s)"