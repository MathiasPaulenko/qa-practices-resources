#!/bin/bash
# ETag and Last-Modified conditional requests

BASE="https://api.staging.local/products/123"

# First request
FIRST=$(curl -s -i "$BASE")
ETAG=$(echo "$FIRST" | grep -i ETag | awk '{print $2}' | tr -d '\r')
LAST=$(echo "$FIRST" | grep -i Last-Modified | cut -d' ' -f2- | tr -d '\r')

echo "=== First request ==="
echo "$FIRST"
echo ""
echo "ETag: $ETAG"
echo "Last-Modified: $LAST"

# Matching ETag should return 304
echo ""
echo "=== Conditional GET with matching ETag ==="
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "If-None-Match: $ETAG" \
  "$BASE"

# After mutation, same ETag should return 200
echo ""
echo "=== Mutation ==="
curl -X PUT -H "Content-Type: application/json" \
  -d '{"price": 19.99}' \
  "$BASE"

echo ""
echo "=== Conditional GET after mutation ==="
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "If-None-Match: $ETAG" \
  "$BASE"

# Last-Modified match
echo ""
echo "=== Conditional GET with If-Modified-Since ==="
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "If-Modified-Since: $LAST" \
  "$BASE"