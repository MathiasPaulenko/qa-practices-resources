#!/usr/bin/env bash
# Starts the QA stack as a Podman pod (rootless). Requires Podman 4.x or 5.x.
set -euo pipefail

POD=qa-stack

podman pod exists "$POD" && podman pod rm -f "$POD"

podman pod create --name "$POD" -p 8080:8080

podman run -d --pod "$POD" --name test-postgres \
  -e POSTGRES_PASSWORD=qa \
  -e POSTGRES_DB=testdb \
  docker.io/library/postgres:15

podman build -t app-under-test:latest -f Containerfile .
podman run -d --pod "$POD" --name app app-under-test:latest

echo "Waiting for Postgres..."
for i in $(seq 1 20); do
  if podman exec test-postgres pg_isready -U postgres -d testdb >/dev/null 2>&1; then
    echo "qa-stack is up: app on http://localhost:8080, db on localhost:5432 (inside the pod)"
    echo "Tear down with: podman pod rm -f $POD"
    exit 0
  fi
  sleep 2
done

echo "Postgres did not become ready in time" >&2
exit 1
