# JMeter API Load Test Companion

Runnable companion for the QAPractices guide [JMeter Tutorial: Load Testing APIs and Web Applications](https://qapractices.com/documentation/jmeter-tutorial/).

## What's inside

- **`api-load-test.jmx`** — JMeter 5.6.3 test plan with a 10-user, 10-second ramp-up GET request against a placeholder API host.
- **`test-data.csv`** — Sample CSV with user IDs to feed a `CSV Data Set Config` if you want to parameterize the path.

## Stack versions

| Tool | Version |
| --- | --- |
| JMeter | 5.6.3 |
| Java | 8 or later |

## Before you run

1. Update the `apiHost` User Defined Variable from `api-staging.example.com` to your own staging host.
2. (Optional) Add a `CSV Data Set Config` that reads `test-data.csv` and use `${userId}` in the HTTP Request path (e.g., `/users/${userId}`).
3. Disable `View Results Tree` if you plan to run more than a few hundred threads.

## Run the test

```bash
jmeter -n -t api-load-test.jmx -l results.jtl -e -o report-folder
```

Open `report-folder/index.html` when it finishes.

## What the plan does

- Hits `${apiHost}/users` with 10 threads, ramping up over 10 seconds, for up to 120 seconds.
- Asserts HTTP 200 and a response time under 500ms.
- Writes a raw `results.jtl` log and an HTML dashboard.

## License

MIT — see the main repo for details.
