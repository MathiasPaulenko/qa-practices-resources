# Test Pyramid Explained Companion

Companion resource for the [Test Pyramid Explained](https://qapractices.com/documentation/test-pyramid-explained) guide. Contains runnable examples for each layer of the test pyramid: unit, integration, API and end-to-end.

## Files

| File | Layer | Purpose |
| ---- | ----- | ------- |
| `src/calculateTotal.test.js` | Unit | Jest unit test for cart discount logic |
| `src/test_order_api.py` | Integration | pytest integration test for order persistence |
| `src/test_checkout_api.py` | API / Service | pytest API test for payment validation |
| `src/checkout.spec.js` | End-to-End | Playwright e2e test for guest checkout |
| `.github/workflows/tests.yml` | CI | GitHub Actions workflow running all layers |

## Quick Start

```bash
# Unit tests (Node.js + Jest)
npm install jest
npx jest src/calculateTotal.test.js

# Integration and API tests (Python + pytest)
pip install requests pytest
pytest src/test_order_api.py src/test_checkout_api.py

# End-to-end tests (Playwright)
npx playwright install
npx playwright test src/checkout.spec.js
```

## Requirements

- Node.js 18+ and npm
- Python 3.11+
- A local API server at `http://localhost:8000` (for integration/API tests)
- Playwright browsers installed
