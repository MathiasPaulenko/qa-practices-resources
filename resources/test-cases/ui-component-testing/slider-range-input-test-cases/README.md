# Slider Range Input Test Cases — Companion

Companion resource for [Slider Range Input Test Cases: Drag, Keyboard, Steps](https://qapractices.com/test-cases/slider-range-input-test-cases/).

## Contents

- `mock_server.py` — stdlib-only mock of the fictional `api.rangesliderpro.io` API used in the article. Implements `GET /v1/products` (`minPrice`, `maxPrice`, `step`, `page`, `pageSize`, Bearer auth), `POST /v1/sliders/validate` (min/max/step/value → validity + `nearestValidValue`), `POST /v1/sliders/validate-range` (crossed handles + `minGap` enforcement) and `POST /v1/users/{id}/preferences` (Bearer auth).
- `slider.html` — static fixture for manual verification of the UI cases: a native `<input type="range">` (min=0, max=1000, step=5) with live tooltip, bidirectional linked numeric input, and a dual-handle emulation enforcing `minGap=10`. Open it in any browser.
- `tests/conftest.py` — spins the mock up on an ephemeral port per test.
- `tests/test_sliders_api.py` — executable subset of the article's cases: price-range filtering, pagination, auth rejection, step-multiple validation, min/max clamping, non-numeric rejection, min-gap boundary (`490/500` allowed, `495/500` rejected) and preference persistence.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/ui-component-testing/slider-range-input-test-cases
pytest tests/ -v
```

Run the mock standalone for manual checks:

```bash
python mock_server.py

curl "http://127.0.0.1:8080/v1/products?minPrice=50&maxPrice=500&step=5&pageSize=5" \
  -H "Authorization: Bearer any-token"
```

## What this covers

- `GET /v1/products` — price-range + step filtering, pagination metadata and Bearer auth.
- `POST /v1/sliders/validate` — step-multiple validation, min/max clamping with `nearestValidValue`, non-numeric rejection.
- `POST /v1/sliders/validate-range` — crossed-handle rejection and the `minGap` boundary (exactly at the gap passes, inside the gap fails).
- `POST /v1/users/{id}/preferences` — preference persistence with auth and required-field validation.
- `slider.html` — manual fixture for TC-001 (drag), TC-005 (snap), TC-010–TC-013 (linked input + invalid input) and TC-008 (min gap) without a real app.
