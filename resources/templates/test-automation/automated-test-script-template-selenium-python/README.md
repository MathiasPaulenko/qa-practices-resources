# Automated Test Script Template (Selenium + Python) — Companion

Runnable companion for the [Automated Test Script Template (Selenium + Python)](https://qapractices.com/templates/automated-test-script-template-selenium-python/) on QAPractices.

A complete Selenium 4 + pytest suite scaffold: page object model, `conftest.py` fixtures with failure screenshots, JSON/YAML test data, parallel execution via pytest-xdist, and a GitHub Actions workflow. The login tests run against [the-internet.herokuapp.com](https://the-internet.herokuapp.com), a public Selenium practice site, so the smoke suite passes out of the box.

## Layout

- `pages/` — `BasePage` (explicit waits, common actions) plus `LoginPage`, `DashboardPage`, `CheckoutPage`
- `tests/` — `test_login.py` (smoke + regression) and `test_checkout.py` (regression)
- `utils/` — `TestDataLoader` (JSON/YAML) and `ScreenshotUtils`
- `data/` — `test_data.json` (users, products, URLs) and `credentials.yaml` (passwords; swap for CI secrets)
- `config/` — `browsers.yaml` with per-environment URLs and timeouts
- `conftest.py` — `driver` fixture (browser + headless via CLI flags) and failure-screenshot hook
- `requirements.txt` — pinned versions: selenium 4.27.0, pytest 8.4.2, pytest-xdist 3.8.1, allure-pytest 2.15.0

## Usage

```bash
pip install -r requirements.txt

# smoke suite against the-internet.herokuapp.com (headless Chrome by default)
pytest -m smoke

# watch the browser instead of headless
pytest -m smoke --headless=no

# Firefox
pytest -m smoke --browser=firefox

# full regression across 4 workers
pytest -m regression -n 4
```

Selenium Manager downloads the matching driver automatically — no `webdriver-manager` needed. Reports land in `reports/html/`, failure screenshots in `reports/screenshots/`.

## Adapting it

Point `base_url` in `data/test_data.json` at your app, replace the `LoginPage` locators with yours, and keep passwords in `credentials.yaml` (gitignore it in real projects) or in CI secrets.
