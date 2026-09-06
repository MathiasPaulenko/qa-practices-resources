#!/bin/bash
set -e

# Environment Variables Check
# Verifies that all required environment variables are set before deployment.
# Usage: ./check-env-vars.sh

required_vars=("DATABASE_URL" "API_KEY" "JWT_SECRET" "S3_BUCKET")
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Missing required environment variable: $var"
    exit 1
  fi
done
echo "All required environment variables are set"
