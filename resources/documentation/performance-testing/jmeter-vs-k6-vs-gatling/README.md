# JMeter vs k6 vs Gatling — Comparable Load Test Scripts

Companion code for [JMeter vs k6 vs Gatling: Performance Benchmarks](https://qapractices.com/documentation/jmeter-vs-k6-vs-gatling/) on QAPractices.

## What is inside

| Folder | Tool | Version | What it shows |
|--------|------|---------|---------------|
| `k6/load-test.js` | k6 | v1.x | Staged load test (ramp 20 → sustain 50 VUs) with `p(95)<500ms` and error-rate thresholds — exits non-zero on breach. |
| `gatling/ProductBrowsingSimulation.scala` | Gatling | 3.12 | Equivalent scenario in the Scala DSL with percentile assertions. |
| `jmeter/product-browsing.jmx` | JMeter | 5.6.3 | Minimal `.jmx` plan: 20 threads, 30s ramp, status assertion, 1s think time. |

All three hit the same placeholder endpoint (`staging.acme-shop.dev/api/v1/products`, overridable via `BASE_URL`) with the same profile — that is the honest way to compare tools: same load, different engine, measure the generator.

## Run them

```bash
# k6 (requires k6 v1.x)
k6 run --env BASE_URL=https://your-staging.dev k6/load-test.js

# Gatling (inside a gatling-maven project, Gatling 3.12)
mvn gatling:test -Dgatling.simulationClass=ProductBrowsingSimulation -DBASE_URL=https://your-staging.dev

# JMeter (5.6.3, headless)
jmeter -n -t jmeter/product-browsing.jmx -l results.jtl -e -o report/
```

Note: scripts were authored against the documented APIs of each tool version but not executed here — no load-testing binaries in this environment. The k6 script follows the `k6/http` + thresholds contract, the JMX validates against JMeter 5.6.3's schema, and the Scala sim uses Gatling 3.12's `setup/inject/assertions` DSL.

## Related resource

- [JMeter vs k6 vs Gatling: Performance Benchmarks](https://qapractices.com/documentation/jmeter-vs-k6-vs-gatling/) — the full comparison, decision matrix and migration story these scripts support.
