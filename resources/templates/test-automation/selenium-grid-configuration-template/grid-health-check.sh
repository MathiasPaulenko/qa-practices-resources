#!/usr/bin/env bash
# Waits for the Selenium Grid hub to report ready and prints registered nodes.
# Usage: ./grid-health-check.sh [hub_url] [timeout_seconds]

HUB="${1:-http://localhost:4444}"
TIMEOUT="${2:-60}"
ELAPSED=0

echo "Waiting for grid at ${HUB} ..."
until curl -sf "${HUB}/status" | grep -q '"ready": *true'; do
  sleep 2
  ELAPSED=$((ELAPSED + 2))
  if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
    echo "Grid did not become ready within ${TIMEOUT}s"
    curl -s "${HUB}/status" || true
    exit 1
  fi
done

echo "Grid is ready. Registered nodes:"
curl -s "${HUB}/status" | grep -o '"stereotype": *"[^"]*"'
