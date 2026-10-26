#!/usr/bin/env bash
# Smoke test for an auto-update feed: the manifest must contain
# version, url and signature. Replace updates.example.com with your feed.
set -euo pipefail

FEED_URL="${1:-https://updates.example.com/latest.json}"

curl -fsS "$FEED_URL" | jq -e '.version and .url and .signature' && echo "Feed OK"
