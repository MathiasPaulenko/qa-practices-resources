# Postman API Testing Tutorial — Companion Resources

Companion resources for the [Postman API Testing Tutorial](https://qapractices.com/documentation/postman-api-testing-tutorial/) on QAPractices.com.

## Contents

| File | Description |
| --- | --- |
| `collections/user-api-tests.postman_collection.json` | Postman collection with GET, POST, login and chained requests. Includes test scripts with assertions. |
| `environments/staging.postman_environment.json` | Staging environment with `baseUrl`, `apiToken`, `userId` and auth variables. |
| `data/test-data.json` | Data-driven test data for parameterized runs with Newman `-d` flag. |

## Requirements

- Postman v11 (GUI) or Newman 6.x (CLI)
- Node.js 20 LTS

## Quick Start

Import the collection and environment into Postman:

1. Open Postman v11
2. Click **Import** and select `collections/user-api-tests.postman_collection.json`
3. Click **Import** again and select `environments/staging.postman_environment.json`
4. Select the **Staging** environment from the dropdown
5. Run individual requests or the entire collection

## Run with Newman (CLI)

```bash
# Install Newman 6.x
npm install -g newman
npm install -g newman-reporter-htmlextra

# Run the collection with the staging environment
newman run collections/user-api-tests.postman_collection.json \
  -e environments/staging.postman_environment.json \
  --reporters cli,htmlextra

# Run with data-driven test data
newman run collections/user-api-tests.postman_collection.json \
  -e environments/staging.postman_environment.json \
  -d data/test-data.json \
  --reporters cli,htmlextra
```

## CI/CD Integration (GitHub Actions)

```yaml
name: API Tests
on: [push, pull_request]
jobs:
  postman-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install Newman
        run: |
          npm install -g newman
          npm install -g newman-reporter-htmlextra
      - name: Run Postman Collection
        run: |
          newman run collections/user-api-tests.postman_collection.json \
            -e environments/staging.postman_environment.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export reports/report.html
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: postman-report
          path: reports/
```

## Related Resources

- [Postman API Testing Tutorial](https://qapractices.com/documentation/postman-api-testing-tutorial/)
- [REST Assured API Testing Guide](https://qapractices.com/documentation/rest-assured-api-testing-guide/)
- [API Testing Guide](https://qapractices.com/documentation/api-testing-guide/)
