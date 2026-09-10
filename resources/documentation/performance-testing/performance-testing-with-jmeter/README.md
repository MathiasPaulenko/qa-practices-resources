# Performance Testing with JMeter Companion

Companion resource for the [Performance Testing with JMeter](https://qapractices.com/documentation/performance-testing-with-jmeter) guide. Contains a ready-to-run JMeter test plan, CSV test data, an SLA assertion script and a GitHub Actions workflow.

## Files

| File | Purpose |
| ---- | ------- |
| `test-plans/checkout-load.jmx` | JMeter test plan for checkout load testing (100 threads, 60s ramp-up) |
| `test-data/checkout-users.csv` | CSV data set with realistic checkout users |
| `scripts/assert-sla.py` | Python script to assert p95 and error rate from JTL results |
| `.github/workflows/perf-tests.yml` | GitHub Actions workflow running JMeter nightly |

## Quick Start

```bash
# Download JMeter 5.6.3
wget https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz

# Run the load test in CLI mode
./apache-jmeter-5.6.3/bin/jmeter \
  -n -t test-plans/checkout-load.jmx \
  -l results/checkout.jtl \
  -e -o report/ \
  -JdataDir=./test-data

# Assert SLA from results
python scripts/assert-sla.py \
  --jtl results/checkout.jtl \
  --max-p95 1000 \
  --max-error-rate 0.5
```

## Requirements

- Apache JMeter 5.6.3
- Python 3.11+
- A target API server (default: `api.staging.local:8080`)
