# Behave vs pytest-bdd Cart Example

This folder contains the same shopping-cart Gherkin scenario implemented with both **Behave 1.2.6** and **pytest-bdd 7.x**.

It is the companion project for:

- [Behave vs pytest-bdd: Choosing the Right Python BDD Tool](https://qapractices.com/documentation/behave-vs-pytest-bdd/)

## Project structure

```text
behave-vs-pytest-bdd/
├── behave-cart/
│   ├── features/
│   │   ├── cart.feature
│   │   ├── environment.py
│   │   └── steps/
│   │       └── cart_steps.py
│   ├── pyproject.toml
│   └── requirements.txt
└── pytest-bdd-cart/
    ├── features/
    │   └── cart.feature
    ├── conftest.py
    ├── test_cart.py
    ├── pyproject.toml
    └── requirements.txt
```

## Run the Behave project

```bash
cd behave-cart
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
behave
```

## Run the pytest-bdd project

```bash
cd pytest-bdd-cart
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest -v
```

## What to compare

- `cart.feature` is identical in both projects.
- `behave-cart/features/environment.py` sets up the shared `context` object.
- `pytest-bdd-cart/conftest.py` defines the `state` fixture.
- Both suites produce three parameterized tests from the `Examples` table.
