# Automated Testing — LedgerFlow Decision Playbook Examples

> Companion resource for [Automated Testing Guide: A Real QA Team Decision](https://qapractices.com/documentation/automated-testing) on QAPractices.com.

Runnable versions of the code snippets from the guide: a Jest 29 unit test for the LedgerFlow tax calculation, a Playwright 1.44 API contract test, a Playwright E2E invoice flow, and the three-job GitHub Actions workflow (unit / integration / e2e).

## Requirements

- Node.js 20
- Jest 29
- Playwright 1.44
- Postgres 15 and Redis 7 (for the integration job in CI, via Docker Compose or GitHub Actions services)

## Setup

```bash
# Install dependencies
npm ci

# Run the unit tests
npm run test:unit

# Install Playwright browsers and run API / E2E suites
# (require a running app; set BASE_URL to point at it)
npx playwright install --with-deps chromium
npm run test:api
npm run test:e2e
```

The unit test runs out of the box against `src/tax/calculateTax.js`. The API and E2E specs target the fictional LedgerFlow app described in the guide — they are meant as drop-in templates for your own routes and `data-testid` attributes.

## Project Structure

```text
src/
  tax/calculateTax.js        # unit under test
tests/
  unit/calculateTax.test.js  # Jest 29 unit test
  api/invoices.spec.js       # Playwright 1.44 API test
  e2e/send-invoice.spec.js   # Playwright 1.44 E2E test
.github/workflows/test.yml   # unit / integration / e2e pipeline
```

## License

MIT — see the repository root LICENSE file.
