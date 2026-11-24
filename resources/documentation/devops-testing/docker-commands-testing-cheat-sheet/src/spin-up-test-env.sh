#!/usr/bin/env bash
# Disposable Postgres for integration tests.
set -euo pipefail

docker run -d --name test-postgres \
  -e POSTGRES_PASSWORD=qa \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 postgres:16

# Wait until Postgres accepts connections (no fixed sleeps).
until docker exec test-postgres pg_isready -U postgres -d testdb >/dev/null 2>&1; do
  sleep 1
done

echo "test-postgres ready on localhost:5432"
