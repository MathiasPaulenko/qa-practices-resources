# Login Test Cases — Companion

Companion files for the [Login Test Cases Examples](https://qapractices.com/test-cases/login-test-cases) resource.

## Files

| File | Contents |
|---|---|
| `login-test-cases.csv` | All 20 test cases as an importable matrix (ID, section, scenario, test data, expected result, automation tool, priority) |
| `test-data.json` | Reusable test users and payloads: valid/locked/invalid users, edge-case inputs, SQLi + XSS payloads |

## Usage

- Import `login-test-cases.csv` into TestRail, Xray or a spreadsheet to track the suite; filter by `section` for focused runs.
- Load `test-data.json` from Playwright, Postman or JMeter — same data drives UI, API and load tests.
- Keep the test-data pool per environment: staging users must never exist in production.

Site resource: [qapractices.com/test-cases/login-test-cases](https://qapractices.com/test-cases/login-test-cases)
