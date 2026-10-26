# Load vs Stress vs Spike Testing — Runnable Profiles

Companion code for [Stress Testing vs Load Testing vs Spike Testing](https://qapractices.com/documentation/stress-testing-vs-load-testing-vs-spike-testing/) on QAPractices.

## What is inside

| File | Tool | Version | Load shape |
|------|------|---------|------------|
| `k6/load-test.js` | k6 | 1.x | Ramp to 50 VUs, 5-minute plateau, ramp down — with `p(95)<500ms` and error-rate thresholds. |
| `k6/stress-test.js` | k6 | 1.x | `ramping-vus` climbing 50 → 800 VUs with no abort thresholds — the point of a stress test is reaching failure, then watching recovery. |
| `k6/spike-test.js` | k6 | 1.x | `ramping-arrival-rate`: 100 rps baseline, 10-second jump to 1,000 rps, 2-minute hold, drop back to observe recovery. |
| `jmeter/test-plan.jmx` | JMeter | 5.6.3 | Minimal headless plan: 50 threads, 120 s ramp, 420 s duration, status assertion, 1 s think time. |

All scripts hit the same placeholder endpoint (`https://api.staging.acme-shop.dev/api/v1/products`, overridable via `BASE_URL`). Same target, different load shape — that is what separates the three test types, not the tool.

## Run them

```bash
# k6 (requires k6 v1.x)
k6 run --env BASE_URL=https://your-staging.dev k6/load-test.js
k6 run --env BASE_URL=https://your-staging.dev k6/stress-test.js
k6 run --env BASE_URL=https://your-staging.dev k6/spike-test.js

# JMeter 5.6.3 (headless, HTML report)
jmeter -n -t jmeter/test-plan.jmx -l results.jtl -e -o report/
```

Notes:

- The stress script deliberately declares no thresholds — aborting on error would stop the test before the breaking point it exists to find.
- For stepped or instant load in JMeter, install the Ultimate Thread Group plugin (`jpgc-plugins`); the bundled plan covers the load profile.
- Scripts were authored against the documented k6 1.x and JMeter 5.6.3 APIs but not executed here — no load-testing binaries in this environment.

## Related resource

- [Stress Testing vs Load Testing vs Spike Testing](https://qapractices.com/documentation/stress-testing-vs-load-testing-vs-spike-testing/) — objectives, methodology, key metrics and the comparison matrix these scripts support.
