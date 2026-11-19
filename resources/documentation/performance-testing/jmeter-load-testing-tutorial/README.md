# JMeter Load Testing Tutorial Companion

Runnable companion for the QAPractices guide [JMeter Load Testing Tutorial: Plans, Threads, Listeners](https://qapractices.com/documentation/jmeter-load-testing-tutorial/).

## What's inside

- **`first-load-test.jmx`** — JMeter 5.6.3 test plan with a 10-user, 10-second ramp-up Thread Group, HTTP Request Defaults, CSV Data Set Config, two assertions, and the two listeners used in the tutorial.
- **`users.csv`** — Sample CSV consumed by the CSV Data Set Config; the sampler path reads it as `/users/${userId}`.

## Stack versions

| Tool | Version |
| --- | --- |
| JMeter | 5.6.3 |
| Java | 8 or later (17+ recommended) |

## Before you run

1. Update the `apiHost` User Defined Variable from `api-staging.example.com` to your own staging host.
2. Keep `users.csv` in the same folder as the `.jmx`, or point the CSV Data Set Config filename at its absolute path.
3. For a zero-risk first run you can set `apiHost` to `jsonplaceholder.typicode.com` and change the sampler path to `/posts` (then adjust the Response Assertion pattern to something the body actually contains, e.g. `userId` still works).

## Run the test

```bash
jmeter -n -t first-load-test.jmx -l results.jtl -e -o report-folder
```

Open `report-folder/index.html` when it finishes.

## What the plan does

- Fires `GET /users/${userId}` with 10 threads ramping up over 10 seconds, one iteration each.
- Asserts the response body contains `userId` and completes under 500 ms.
- Includes a `View Results Tree` listener for GUI debugging — disable it before real load runs; it buffers every response body in memory.
- Writes a raw `results.jtl` log and an HTML dashboard.

## License

MIT — see the main repo for details.
