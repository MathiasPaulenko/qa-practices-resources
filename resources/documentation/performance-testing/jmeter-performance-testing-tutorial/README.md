# JMeter Performance Testing Tutorial — Companion

Runnable assets for the [JMeter Performance Testing Tutorial](https://qapractices.com/documentation/jmeter-performance-testing-tutorial/).

## Files

| File | What it does |
|---|---|
| `users.csv` | The CSV Data Set fixture from Step 5 — 3 rows covering valid and invalid login cases. |
| `run-load-test.sh` | Non-GUI runner with the tutorial's exact flags (`-n -t -l -e -o`), timestamped results, and a post-run checklist printed to the console. |
| `results-checklist.md` | Post-run analysis table: where each metric lives in the report, what's healthy, what to do when it isn't. |

## Run

```bash
chmod +x run-load-test.sh
JMETER_HOME=/path/to/apache-jmeter-5.6.3 ./run-load-test.sh test-plans/load-test.jmx
```

Point `testdata/` at `users.csv` in your CSV Data Set Config (Step 5 of the tutorial).

## What it demonstrates

- **Non-GUI is the real mode** — the script bakes in the flags so nobody runs load tests from the GUI by accident.
- **The run isn't the deliverable, the analysis is** — the printed checklist keeps you from collecting a report nobody reads.
