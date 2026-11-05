# JMeter Load Testing Script Template — Companion

Executable companion for https://qapractices.com/templates/load-testing-script-template-jmeter/

## Files

- `loadtest.jmx` — JMeter test plan (thread group, HTTP samplers, assertions, CSV data set, listeners)
- `users.csv` — synthetic test data for `CSVDataSet` (place under `testdata/users.csv`)
- `jmeter-load-test.yml` — GitHub Actions workflow that downloads JMeter 5.6.3 and runs the plan headless

## Run

```bash
jmeter -n -t loadtest.jmx -JbaseUrl=https://your-staging-url -JapiKey=YOUR_KEY -l results.jtl -e -o report/
```

Override `baseUrl`/`apiKey` with `-J` flags; never hardcode environment values in the plan.
