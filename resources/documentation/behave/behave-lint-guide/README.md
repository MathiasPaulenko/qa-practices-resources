# behave-lint Example

Companion project for the [Behave Lint Guide](https://qapractices.com/documentation/behave-lint-guide/).

This folder contains a deliberately messy `auth.feature` so you can run `behave-lint` 2.4.1 and see real diagnostics: duplicate scenario names, mixed tag casing, hardcoded dates, trailing punctuation, and a hardcoded secret.

## Quick start

```bash
cd lint-example
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
behave-lint features/
```

The first run should report 20 diagnostics (1 error, 8 warnings, 11 info). Then try `behave-lint --fix --unsafe-fixes features/` to see which issues are auto-fixable.

## Files

- `features/auth.feature` — intentionally broken Gherkin file used in the guide.
- `pyproject.toml` — `behave-lint` configuration with rule selection and overrides.
- `requirements.txt` — pins `behave-lint==2.4.1`.
