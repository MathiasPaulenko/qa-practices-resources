# Behave Kit Utilities Example

This folder contains a runnable **Behave 1.2.6** project with **behave-kit 1.5.0**. It is the companion project for the QAPractices guide [Behave Kit Utilities for BDD Tests](https://qapractices.com/documentation/behave-kit-guide/).

It demonstrates the most useful `behave-kit` features in a single small shopping-cart suite:

- Soft assertions with `assert_soft` and `assert_soft_equals`.
- `TypedContext` with a schema class.
- Conditional skip with `@skip_if_env`.
- `env()` for typed environment reads.
- `load_data()` for CSV/JSON data files.
- Tag-based fixtures with `@fixture`.
- Class-based steps with `step_impl_base()`.
- `run_steps()` for sub-step execution.
- Per-scenario timeout with `@timeout:N`.

## Project structure

```text
behave-kit-guide/
└── cart_bdd/
    ├── behave.ini
    ├── pyproject.toml
    ├── requirements.txt
    ├── catalog_service.py
    ├── tests/
    │   └── data/
    │       └── users.csv
    └── features/
        ├── environment.py
        ├── cart.feature
        └── steps/
            ├── cart_steps.py
            └── fixtures.py
```

## Run the cart example

```bash
cd cart_bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture
```

Expected output:

```text
4 scenarios passed, 0 failed, 0 skipped
13 steps passed, 0 failed, 0 skipped
```

## Explore individual features

- `features/steps/cart_steps.py` — soft assertions and `TypedContext`.
- `features/steps/fixtures.py` — tag-based fixtures and conditional skips.
- `features/environment.py` — `setup()` and soft-assert activation.
- `catalog_service.py` — small in-memory domain code under test.
- `tests/data/users.csv` — data file used by `load_data`.

## Optional extras

For YAML or Excel data files install the extras:

```bash
pip install "behave-kit[yaml,excel,dotenv]"
```
