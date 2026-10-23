#!/bin/bash
# env-check.sh — week-1 environment verification for a new QA hire.
# Exits on the first missing/broken tool so fixes happen before the first standup.
set -e

echo "== QA onboarding environment check =="

echo "Node $(node -v)"
echo "Git $(git --version)"
echo "Python $(python3 --version 2>/dev/null || python --version)"

docker run hello-world

if command -v npx >/dev/null 2>&1; then
  npx playwright install chromium
else
  echo "npx not found — install Node.js LTS first" >&2
  exit 1
fi

echo "All checks passed."
