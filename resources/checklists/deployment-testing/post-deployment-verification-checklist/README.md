# Post-Deployment Verification Checklist — Companion

Runnable companion for the [Post-Deployment Verification Checklist](https://qapractices.com/checklists/post-deployment-verification-checklist) resource.

The three scripts cover the executable part of the checklist: the health probe, the k6 smoke pass and a minimal Playwright spec for the critical journey — all driven by a `BASE_URL` environment variable so nothing points at a hardcoded host.

## Files

| File | Contents |
|---|---|
| `health-check.sh` | curl + jq check that the `/health` endpoint returns 200 and required components report `up` |
| `smoke-test.js` | k6 smoke test (5 VUs, 30s) with p95 latency and error-rate thresholds |
| `post-deployment-verification.spec.ts` | Playwright spec covering the health endpoint and a critical page render |

## Usage

- `BASE_URL=https://api.yourdomain.com ./health-check.sh` — run right after deploy; fails on non-200 or any component not `up`.
- `k6 run -e BASE_URL=https://api.yourdomain.com smoke-test.js` — short load pass; the build fails if p95 > 500ms or errors > 1%.
- `BASE_URL=https://app.yourdomain.com npx playwright test post-deployment-verification.spec.ts --reporter=list` — critical journey check.
- Wire `health-check.sh` and `smoke-test.js` into the pipeline as post-deploy gates; keep the Playwright spec for releases that touch the UI.
- Thresholds here are starting points — set your own rollback numbers before deploy, per the checklist's section 9.

Site resource: [qapractices.com/checklists/post-deployment-verification-checklist](https://qapractices.com/checklists/post-deployment-verification-checklist)
