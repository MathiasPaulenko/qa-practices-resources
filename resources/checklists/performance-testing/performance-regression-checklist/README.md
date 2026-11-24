# Performance Regression Checklist — Companion

Runnable artifacts for the [Performance Regression Checklist](https://qapractices.com/checklists/performance-regression-checklist/) on QAPractices.com.

## Files

| File | Purpose |
|------|---------|
| `k6_thresholds.js` | k6 script with per-endpoint p95 thresholds, absolute error-rate ceiling and throughput floor — exits non-zero on breach. |
| `compare_baseline.py` | Compares a candidate metrics JSON against a stored baseline; fails on >10% latency regression or error-rate ceiling. |
| `perf_gate_workflow.yml` | GitHub Actions gate: warm-up run, measured run, baseline comparison, artifact upload. |

## Quick start

```bash
# 1. Run the k6 gate directly
k6 run --env BASE_URL=https://staging.example.internal k6_thresholds.js

# 2. Compare a candidate run against a stored baseline
python compare_baseline.py \
  --baseline baselines/v1.9.0.json \
  --candidate results/candidate.json \
  --max-degradation 0.10 --max-error-rate 0.005

# 3. Wire into CI
#    copy perf_gate_workflow.yml to .github/workflows/perf-gate.yml
```

## The rule that matters

A gate that never blocks a deploy is decoration. Thresholds must be tighter than your environment noise allows — measure run-to-run variance first, then set bands above it.
