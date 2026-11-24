#!/usr/bin/env bash
# Spin up the test stack, run the suite, always clean up.
set -euo pipefail

cleanup() {
  docker compose -f docker-compose.test.yml down -v
}
trap cleanup EXIT

docker compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from tests
