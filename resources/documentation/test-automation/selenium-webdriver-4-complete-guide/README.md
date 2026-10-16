# Selenium WebDriver 4 — Runnable Test Suite

Companion code for the [Selenium WebDriver 4: New Features](https://qapractices.com/documentation/selenium-webdriver-4-complete-guide/) guide.

A self-contained suite that exercises the guide's core techniques — Page Object Model, explicit waits, relative locators, window handles and alerts — against a local HTML fixture (`app/login.html`). No external site needed.

## Requirements

- Python 3.10+ and Chrome installed (Selenium Manager downloads ChromeDriver automatically)
- `pip install -r requirements.txt`

## Run

```bash
python -m pytest tests/ -v
```

Headless mode is on by default. To watch the browser run:

```bash
SELENIUM_HEADLESS=false python -m pytest tests/ -v
```

## What it covers

| File | Technique |
|---|---|
| `tests/test_login_pom.py` | Page Object Model: fluent login page, success and failure paths |
| `tests/test_selenium4_features.py` | Relative locator (`above`), explicit wait for a delayed element, spinner invisibility, new-tab window handle, confirm-alert accept |
