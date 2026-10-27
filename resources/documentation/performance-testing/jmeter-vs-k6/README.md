# JMeter vs k6 — Runnable Payment Flow Scripts

Companion code for the guide [JMeter vs k6: Choosing a Load Testing Tool](https://qapractices.com/documentation/jmeter-vs-k6/) — the runnable artifacts behind the NovaPay decision: 50,000 virtual users, a stepped ramp, and a hybrid JMeter + k6 setup.

## Contents

| Path | What it is |
|---|---|
| `k6/payments.js` | k6 v1.x script: `ramping-vus` to 50k VUs, p95/failed-rate thresholds, payment → refund flow, ~40 s think time. |
| `jmeter/jsr223-payment-sampler.groovy` | JMeter 5.6.3 JSR223 Sampler + PostProcessor: builds the payment JSON and extracts `transactionId`. |
| `ci/jmeter-v1-load-test.yml` | GitHub Actions workflow that runs the `.jmx` suite non-GUI and asserts on the JTL error rate. |
| `ci/k6-v2-load-test.yml` | GitHub Actions workflow using `grafana/k6-action@v0.3.1` with InfluxDB output. |
| `scripts/assert-jtl.sh` | Bash gate that fails the build when the JTL error rate exceeds a given fraction. |

## Usage

```bash
# k6 — requires k6 v1.x and a reachable BASE_URL
NOVA_API_KEY=your-key BASE_URL=https://staging.api.local/v2 \
  k6 run k6/payments.js

# JMeter — non-GUI mode, JTL + HTML report
jmeter -n -t jmeter/v1-payments.jmx -l results.jtl -e -o report/

# Assert on the JTL error rate (< 0.5%)
./scripts/assert-jtl.sh results.jtl 0.005
```

Copy the files under `ci/` into `.github/workflows/` of your own repo to activate them — they live outside `.github/` here on purpose so they never trigger on this repository.

`api.novapay.example.com` and `influxdb.novapay-sandbox` are placeholders; substitute your staging URL and internal InfluxDB endpoint.
