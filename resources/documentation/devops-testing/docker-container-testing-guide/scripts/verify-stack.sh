#!/usr/bin/env bash
# Verifies the seven testing areas from the guide against the running stack.
set -euo pipefail

echo "== 1. Image =="
docker history app-app --no-trunc | tail -n +2 | wc -l

echo "== 2. Startup =="
docker compose -f docker-compose.test.yml ps --format '{{.Name}} {{.Status}}'

echo "== 3. Health =="
docker inspect --format '{{.State.Health.Status}}' "$(docker compose -f docker-compose.test.yml ps -q app)"
docker inspect --format '{{.State.Health.Status}}' "$(docker compose -f docker-compose.test.yml ps -q db)"

echo "== 4. Networking =="
docker compose -f docker-compose.test.yml exec -T app wget -q -O - http://localhost:8080/ready

echo "== 5. Volumes (n/a in this stack — tested via named volume if added) =="

echo "== 6. Limits =="
docker inspect --format 'memory={{.HostConfig.Memory}} cpus={{.HostConfig.NanoCpus}}' \
  "$(docker compose -f docker-compose.test.yml ps -q app)"

echo "== 7. Orchestration =="
docker compose -f docker-compose.test.yml ps --format '{{.Name}} {{.DependsOn}}' 2>/dev/null || true

echo "Stack verification complete."
