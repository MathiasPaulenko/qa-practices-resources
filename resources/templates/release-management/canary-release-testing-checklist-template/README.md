# Canary Release Testing Checklist — Runnable Companion

Companion to [Canary Release Testing Checklist Template](https://qapractices.com/templates/canary-release-testing-checklist-template/) ([ES](https://qapractices.com/es/templates/canary-release-testing-checklist-template/)).

Working artifacts for the checklist's stage-gate logic, ready to adapt to a real Argo Rollouts setup.

## Contents

| File | Purpose |
|---|---|
| `rollout.yaml` | Argo Rollouts 1.8 manifest with the checklist's stages (5 → 10 → 25 → 50 → 100) and per-stage analysis runs |
| `analysis-template.yaml` | AnalysisTemplate with Prometheus queries: request volume, error-rate delta, p95 delta — missing data counts as failure |
| `evaluate-stage.mjs` | Node 20+ gate evaluator implementing the checklist's rules: same-window baseline deltas, absolute floors, minimum request count, missing data fails closed |
| `tests/evaluate-stage.test.mjs` | `node:test` suite covering promote / hold / rollback decisions |

## Run the tests

```bash
node --test tests/*.test.mjs
```

All 7 tests should pass — they cover the failure modes the checklist warns about: broken baselines that pass delta checks, low-traffic canaries promoting on noise, and metric gaps being read as zero errors.

## Use the evaluator standalone

```bash
node evaluate-stage.mjs baseline.json canary.json
# prints PROMOTE | HOLD | ROLLBACK with a reason, exit code 0 only on PROMOTE
```

Both JSON files take the shape `{"errorRate": 0.0028, "p95Ms": 120, "requests": 1250}`.

## Notes

- The YAML targets Argo Rollouts 1.8 + Istio 1.27 + Prometheus 3.x on Kubernetes 1.34 — adjust names and addresses to your environment.
- The PromQL queries compare the canary cohort against the stable cohort measured in the same window, matching the checklist's same-day baseline rule.
- `evaluate-stage.mjs` deliberately treats absent metrics as a failed gate; a Prometheus gap is not a clean bill of health.
