# Deployment Testing — Companion

Runnable scripts for the [Deployment Testing guide](https://qapractices.com/documentation/deployment-testing/) on QAPractices.

## Scripts

### `scripts/post-deploy-smoke.sh`

Post-deploy smoke test that asserts on response **bodies**, not just status codes — a 200 serving a stale build is a false green. Checks health marker, real token issue, and an authenticated call; optionally verifies the deployed version matches `EXPECTED_VERSION`.

```bash
SMOKE_EMAIL=smoke@acme-corp.test SMOKE_PASSWORD=*** \
  ./scripts/post-deploy-smoke.sh https://staging.acme-corp.test
```

### `scripts/rollback-drill.sh`

Timed rollback rehearsal. Executes your `ROLLBACK_CMD`, polls until the service is healthy again, and fails if the recovery time exceeds the budget — that budget is your incident duration floor.

```bash
ROLLBACK_CMD='kubectl rollout undo deploy/api -n prod' \
  ./scripts/rollback-drill.sh https://staging.acme-corp.test 120
```

## Requirements

- `bash`, `curl`, `jq` 1.6+
- A dedicated smoke-test account (env vars, never committed)
- For the drill: a working rollback command for your stack (`kubectl rollout undo`, Argo Rollouts, `helm rollback`, your pipeline's revert job)

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Checks pass |
| 1 | Usage error or endpoint unreachable |
| 2 | A check failed / budget exceeded |
