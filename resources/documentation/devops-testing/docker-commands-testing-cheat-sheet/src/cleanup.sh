#!/usr/bin/env bash
# Remove test containers and images left behind by a run.
set -euo pipefail

docker rm -f $(docker ps -aq --filter "name=test") 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=*test*") 2>/dev/null || true

echo "test resources cleaned"
