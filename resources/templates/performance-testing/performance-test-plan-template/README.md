# Performance Test Plan Template — Companion Scripts

Companion scripts for the [Performance Test Plan Template](https://qapractices.com/templates/performance-test-plan-template).

## Files

| File | Purpose |
| --- | --- |
| `scripts/checkout-load-test.js` | k6 0.54 normal load test: 200 VUs for 30 minutes. |
| `scripts/checkout-stress-test.js` | k6 0.54 stress test: incremental load from 500 to 2000 VUs. |
| `scripts/checkout-soak-test.js` | k6 0.54 soak test: 200 VUs for 12 hours. |
| `scripts/checkout-spike-test.js` | k6 0.54 spike test: 100 to 1000 VUs in 1 minute. |
| `scripts/jmeter-checkout-load-test.jmx` | JMeter 5.6 non-GUI load test plan for checkout API. |

## Usage

```bash
# Install k6 0.54
# macOS: brew install k6
# Linux: sudo gpg -k && sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E6019A && echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list && sudo apt update && sudo apt install k6

# Run normal load test
k6 run --vus 200 --duration 30m --out json=results.json scripts/checkout-load-test.js

# Run stress test
k6 run scripts/checkout-stress-test.js

# Run soak test
k6 run scripts/checkout-soak-test.js

# Run spike test
k6 run scripts/checkout-spike-test.js

# Run JMeter test (non-GUI)
jmeter -n -t scripts/jmeter-checkout-load-test.jmx -l results.jtl -e -o dashboard/
```

## Requirements

- k6 0.54+
- JMeter 5.6+
- Node.js 20+ (for k6 ES modules)
