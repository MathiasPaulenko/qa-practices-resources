# JMeter Elements Cheat Sheet — Companion

Runnable companion for the [JMeter Elements Cheat Sheet](https://qapractices.com/documentation/jmeter-elements-cheat-sheet/) on QAPractices.

Implements the three patterns from the cheat sheet in a single plan (JMeter 5.6.3):

1. **Login once, reuse the token** — `Once Only Controller` + `JSON Extractor` → `${authToken}` injected by `HTTP Header Manager`.
2. **CSV-driven users** — `CSV Data Set Config` feeds `${username}`/`${password}` from `users.csv`.
3. **Realistic think time** — `Uniform Random Timer` between requests.

## Files

- `login-token-pattern.jmx` — the plan (10 threads, 30s ramp-up, 5 loops; placeholder host `staging.example.com` — set your staging URL in `HTTP Request Defaults`).
- `users.csv` — sample credentials; the plan reads `${username}`/`${password}` from it.
- `run-load-test.sh` — headless runner: `jmeter -n -t login-token-pattern.jmx -l results.jtl -e -o report/`.

## Run

```bash
./run-load-test.sh          # or: jmeter -n -t login-token-pattern.jmx -l results.jtl -e -o report/
```

Requires JMeter 5.6.3+ on PATH. Open `report/index.html` for the dashboard.
