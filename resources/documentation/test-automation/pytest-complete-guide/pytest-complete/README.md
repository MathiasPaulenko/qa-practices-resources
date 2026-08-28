# Pytest Complete Example Project

Companion project for [Pytest Complete Guide](https://qapractices.com/documentation/pytest-complete-guide/) on QAPractices.

## What this project includes

- `src/calculator.py` — simple domain class for unit tests.
- `src/user_service.py` — API client to use with `pytest-mock` examples.
- `tests/conftest.py` — shared fixtures, fixture factory and session-scoped fixture.
- `tests/unit/` — unit tests covering fixtures, parametrization, markers and mocking.
- `tests/integration/` — integration tests marked with `@pytest.mark.integration`.
- `.github/workflows/pytest.yml` — GitHub Actions matrix CI with coverage.
- `pytest.ini` — markers and default options.
- `pyproject.toml` — project metadata and coverage configuration.

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
pytest
pytest -m smoke
pytest -m "not slow"
pytest -n auto
pytest --cov=src --cov-report=term-missing
```

## Project structure

```text
pytest-complete/
├── src/
│   ├── calculator.py
│   └── user_service.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_calculator.py
│   │   ├── test_parametrize.py
│   │   ├── test_mocking.py
│   │   └── test_fixtures.py
│   └── integration/
│       └── test_user_service.py
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── .github/workflows/pytest.yml
```
