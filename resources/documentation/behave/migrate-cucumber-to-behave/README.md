# Migrate from Cucumber to Behave Example

This folder contains a runnable **Behave 1.2.6** project that mirrors the migration examples from the QAPractices guide [Migrate from Cucumber to Behave: A Python BDD Guide](https://qapractices.com/documentation/migrate-cucumber-to-behave/).

It shows the same Gherkin scenario implemented after a migration from Cucumber-JVM or cucumber-js, with Python step definitions, `context`-based shared state and `environment.py` hooks.

## Project structure

```text
migrate-cucumber-to-behave/
└── cart_bdd/
    ├── behave.ini
    ├── pyproject.toml
    ├── requirements.txt
    ├── api_server.py
    ├── cart/
    │   ├── __init__.py
    │   └── service.py
    └── features/
        ├── environment.py
        ├── cart.feature
        ├── api.feature
        └── steps/
            ├── cart_steps.py
            ├── api_steps.py
            └── types.py
```

## What it demonstrates

- `cart/service.py` is the domain code under test (product catalog and cart).
- `features/cart.feature` is the migrated Gherkin scenario.
- `features/steps/cart_steps.py` is the Python equivalent of the original Java `@Given`, `@When` and `@Then` methods.
- `features/steps/types.py` shows how to register a custom `Product` parameter type with `parse_type`.
- `features/steps/api_steps.py` shows how to migrate a `cucumber-js` API scenario to `requests` and `behave`.
- `features/environment.py` initializes `context.catalog`, `context.cart`, `context.base_url` and `context.token` per scenario, and starts/stops the mock API server via `before_all` / `after_all`.
- `api_server.py` is a tiny `http.server` mock that returns 200 and 404 so the API example runs offline.
- `behave.ini` keeps paths, formatters and `userdata` out of the step code.

## Run the cart scenario

```bash
cd cart_bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture features/cart.feature
```

Expected output:

```text
Feature: Add products to the shopping cart

  Scenario: Add a single product and check the total
    Given the product catalog contains "Book" priced at 15.00
    When the user adds 1 Book to the cart
    Then the cart total should be 15.00

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped
```

## Run the API scenario

The API scenario uses `requests` against a local mock server started by `environment.py` in `before_all`. It does not require an internet connection.

```bash
behave --tags=@api --no-capture
```

Expected output:

```text
Feature: API health check migrated from cucumber-js

  @api
  Scenario: GET a 200 response
    Given the API is available at "http://127.0.0.1:8765"
    When I GET "/status/200"
    Then the response status should be 200

  @api
  Scenario: GET a 404 response
    Given the API is available at "http://127.0.0.1:8765"
    When I GET "/status/404"
    Then the response status should be 404

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped
```

To point it at your own API, set the `API_BASE_URL` environment variable or edit `behave.ini`:

```ini
[behave.userdata]
api_url = https://your-api.example.com
```

Then update `features/environment.py` to read `config.userdata.get('api_url')`.
