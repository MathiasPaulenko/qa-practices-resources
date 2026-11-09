# Postman Collection Testing Template — Companion

Runnable files that implement the [Postman Collection Testing: Newman template](https://qapractices.com/templates/postman-collection-testing-template/) from QAPractices: an exported collection with `pm.test` assertion scripts, a staging environment, a CSV data file for data-driven runs and a GitHub Actions workflow.

## Files

| File | What it is |
|---|---|
| `api-test-collection.postman_collection.json` | Postman Collection v2.1 export: auth folder, users folder, negative tests, `pm.test` scripts |
| `staging.postman_environment.json` | Staging environment variables — replace the placeholder credentials before running |
| `login_test_data.csv` | Data file for the data-driven login test (7 rows: valid, invalid and boundary cases) |
| `newman-ci.yml` | GitHub Actions workflow that installs Newman 6.x and runs the collection with an htmlextra report |

## Run it

```bash
npm install -g newman@6 newman-reporter-htmlextra@1

newman run api-test-collection.postman_collection.json \
  -e staging.postman_environment.json \
  -d login_test_data.csv \
  -r cli,htmlextra \
  --reporter-htmlextra-export reports/api-test-report.html
```

The collection points `{{base_url}}` at your staging API. Override it without editing files:

```bash
newman run api-test-collection.postman_collection.json \
  -e staging.postman_environment.json \
  --env-var "base_url=https://api.staging.your-domain.com"
```

## Notes

- The `Login_Valid` request writes `auth_token` and `refresh_token` to the environment via its test script; downstream requests consume `{{auth_token}}`.
- `newman-ci.yml` expects the collection under `collections/` and the environment under `environments/` — adjust paths to your repo layout.
- Newman exits non-zero on any failed assertion, so the workflow fails the job automatically.

Source: [qapractices.com/templates/postman-collection-testing-template](https://qapractices.com/templates/postman-collection-testing-template/)
