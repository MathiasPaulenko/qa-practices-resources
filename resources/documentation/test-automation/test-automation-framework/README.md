# Test Automation Framework — Minimal Playwright Scaffold

> Companion resource for [How to Build a Test Automation Framework from Scratch](https://qapractices.com/documentation/test-automation-framework) on QAPractices.com.

A minimal Python/Playwright 1.48 framework scaffold showing layered architecture: config, page objects, and base tests. Designed as a starting point for teams building their first custom automation layer.

## Requirements

- Python 3.12+
- pytest 8.3
- pytest-playwright 0.5
- playwright 1.48

## Setup

```bash
# Clone and install
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install pytest==8.3 pytest-playwright==0.5
playwright install chromium

# Run tests
pytest --numprocesses 4
```

## Project Structure

```text
tests/
  core/
    config.py          # Environment configuration
  ui/
    pages/
      login_page.py    # Page object for login
    specs/
      test_login.py    # Login test specs
pyproject.toml         # pytest configuration
```

## Files

| File | Purpose |
| ------ | --------- |
| `tests/core/config.py` | Base URL, browser, headless mode from env vars |
| `tests/ui/pages/login_page.py` | Page object with `open`, `login`, `error_message` methods |
| `tests/ui/specs/test_login.py` | Valid and invalid login test cases |
| `pyproject.toml` | pytest config with `--numprocesses 4` for parallel execution |

## Architecture

The scaffold follows a three-layer design:

1. **Test layer** (`tests/ui/specs/`) — reads like a specification, no browser drivers imported directly.
2. **Business layer** (`tests/ui/pages/`) — page objects that encapsulate UI interactions.
3. **Core layer** (`tests/core/`) — shared infrastructure: config, logging, test data.

## License

MIT — free to use, modify, and distribute.
