# Hotfix Deployment Testing Checklist — Companion

Runnable scripts for the [Hotfix Deployment Testing Checklist](https://qapractices.com/checklists/hotfix-deployment-testing-checklist/) on QAPractices.

## Scripts

### `scripts/hotfix-scope-check.sh`

Verifies a hotfix branch contains **only the fix** — one commit on top of the production tag. Fails if the branch was cut from the wrong base or carries extra commits.

```bash
./scripts/hotfix-scope-check.sh v1.2.3 hotfix/1.2.4
```

### `scripts/post-deploy-verify.sh`

Verifies the hotfix actually landed: endpoint reachable, `version` field matches the deployed build, and latency inside baseline. A green health check on the old artifact is the most common false positive in hotfix verification — this checks the version, not just the status.

```bash
./scripts/post-deploy-verify.sh https://api.acme-corp.test/health 1.2.4-hotfix
```

## Requirements

- `bash`, `curl`, `jq`
- `git` (for the scope check)

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All checks pass |
| 1 | Usage error or endpoint unreachable |
| 2 | Verification failed — start the rollback clock |
