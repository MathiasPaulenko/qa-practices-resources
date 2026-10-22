# Functional Testing Checklist — Runnable Companion

The executable pieces behind the [Functional Testing Checklist](https://qapractices.com/checklists/functional-testing-checklist/) on QAPractices: the 139 items as machine-readable CSV with risk tags, a login-form HTML fixture to exercise boundary and negative checks, a Playwright spec, and a pytest contract test over a bundled API response sample.

## Contents

| File | What it is |
|---|---|
| `checklist-items.csv` | All 139 checklist items (`id`, `area`, `item`, `risk`) — import into your tracker or pipe into a triage script. |
| `login-form.html` | Zero-dependency fixture with `data-testid` hooks: email, password, age with min-18 validation, and double-purpose login/save buttons. |
| `functional.spec.ts` | Playwright 1.48 spec: age-field boundary check and login happy path with credentials injected via `TEST_USER_EMAIL` / `TEST_USER_PASSWORD`. |
| `fixtures/profile-response.json` | Sample API response used by the contract test. |
| `tests/test_contract.py` | pytest 8.3 checks: response shape, CSV completeness/risk coverage, fixture testids. |

## Run the pytest suite

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output:

```text
tests/test_contract.py::test_profile_response_shape PASSED
tests/test_contract.py::test_checklist_csv_is_complete_and_risk_tagged PASSED
tests/test_contract.py::test_login_form_fixture_has_required_testids PASSED
3 passed
```

## Run the Playwright spec (optional)

```bash
npm i -D @playwright/test
npx playwright install chromium
TEST_USER_EMAIL=qa_ana@test.local TEST_USER_PASSWORD=ChangeMe123! \
  npx playwright test functional.spec.ts
```

The spec loads `login-form.html` relative to this directory — point `baseURL` or `page.goto` at a local server (e.g. `python -m http.server`) when running it.

## Using the CSV

Each row is one checkbox from the article, tagged `High`, `Medium` or `Low`. Filter `risk=High` for a release-blocking sweep, or group by `area` to scope a regression to the sections a change touched — the same triage logic the article describes.

## Cross-references

- Source article: <https://qapractices.com/checklists/functional-testing-checklist/> · [Versión ES](https://qapractices.com/es/checklists/functional-testing-checklist/)
- Deliverable format: the article links the [functional testing bundle template](https://qapractices.com/templates/functional-testing-checklist-bundle/) for hand-off contexts.
