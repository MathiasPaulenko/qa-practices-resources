# behave-data Example — Product Catalog BDD

This folder contains a runnable **Behave** project that accompanies the QAPractices guide [Data Management for Behave BDD](https://qapractices.com/documentation/behave-data-guide/).

It demonstrates typed tables, table diffing, dynamic examples loaded from CSV and JSON, fixtures, builders, and masked secrets with `behave-data==1.0.2` and `behave==1.3.3` on Python 3.11+.

## Project structure

```text
product_bdd/
├── .github/workflows/behave-data.yml
├── behave.ini
├── pyproject.toml
├── requirements.txt
├── product_catalog.py
└── features/
    ├── environment.py
    ├── products.feature
    ├── steps/product_steps.py
    └── data/
        ├── fixtures.py
        ├── products.csv
        ├── users.csv
        ├── prices.json
        └── secrets/
            └── .gitkeep
```

`product_catalog.py` is a tiny in-memory catalog used by the BDD suite. `features/environment.py` initializes `behave-data` with `setup_data`, registers the custom `product_code` type, and wires all hooks. `features/data/fixtures.py` defines two `data_fixture` recipes and one `data_builder`. `features/products.feature` is the Gherkin that exercises every feature of the package.

## Run locally

```bash
cd product_bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture
```

Expected output:

```text
Feature: Product catalog data management

  @load_examples:csv:features/data/products.csv
  Scenario Outline: Bulk load products from CSV -- @1.1
    Given the catalog is empty
    When I import a product with name "T-Shirt", price 19.99, active "true" and stock 50
    Then the catalog should contain the product "T-Shirt"

  @load_examples:csv:features/data/products.csv
  Scenario Outline: Bulk load products from CSV -- @1.2
    Given the catalog is empty
    When I import a product with name "Mug", price 9.50, active "false" and stock 0
    Then the catalog should contain the product "Mug"

  @load_examples:csv:features/data/users.csv
  Scenario Outline: Load users from CSV and match fixtures -- @1.1
    Given a registered user "alice" with email "alice@qapractices.com" and role "user"
    Then the loaded user matches the fixture

  @load_examples:json:features/data/prices.json
  Scenario Outline: Load price tiers from JSON -- @1.1
    Given the catalog is empty
    When I import a price tier "basic" with sku "PRD-003" and price 5.99
    Then the catalog should contain the product "PRD-003"

  @needs_data:regular_user:alice
  Scenario: Declarative fixture tag loads a user
    Then the loaded user has username "alice" and role "user"

  @with_fixture:admin_user
  Scenario: Nested admin fixture references a regular user
    Then the admin has username "admin" and reports to user "alice"

  Scenario: Typed table conversion and diff
    When I add the following products
      | name:str | sku:product_code | price:float | active:bool | stock:int | released:date | description:str? |
      | T-Shirt  | PRD-001          | 19.99       | true        | 50        | 2025-03-15    |                  |
      | Mug      | PRD-002          | 9.50        | false       | 0         | 2025-04-01    | None             |
    Then the catalog should contain the following products
      | name:str | sku:product_code | price:float | active:bool | stock:int | released:date | description:str? |
      | T-Shirt  | PRD-001          | 19.99       | true        | 50        | 2025-03-15    |                  |
      | Mug      | PRD-002          | 9.50        | false       | 0         | 2025-04-01    | None             |

  Scenario: Build products with a data builder
    Given the catalog is empty
    When I build 3 "product" items with name prefix "Custom"
    Then the catalog should contain 3 products with name starting with "Custom"

  Scenario: Resolve and mask a secret from env
    When I resolve the API key from env
    Then the resolved value is masked in logs

1 feature passed, 0 failed, 0 skipped
12 scenarios passed, 0 failed, 0 skipped
28 steps passed, 0 failed, 0 skipped
```

## What it demonstrates

- `features/environment.py` shows how to call `setup_data`, register a custom type, and wire `before_feature_hook`, `before_scenario_hook`, `before_step_hook`, and `after_scenario_hook`.
- `features/products.feature` uses `@load_examples` from CSV and JSON, typed table headers, `@needs_data` and `@with_fixture` tags, and a `Scenario Outline` with data builders.
- `features/steps/product_steps.py` uses `typed_wrap`, `diff`, `DataManager.resolve`, and `DataManager.build`.
- `features/data/fixtures.py` defines parametrized fixtures and a nested `ref:` fixture.
- `behave.ini` configures `behave-data` through the `[behave.userdata]` section.
- `.github/workflows/behave-data.yml` runs the suite on Python 3.11, 3.12, and 3.13 and uploads reports even when the job fails.

## Notes

- The `Examples` blocks under `@load_examples` need at least one throw-away row because Behave parses them before `before_feature_hook` can replace them with the loaded data.
- The `CATALOG_API_KEY` environment variable is set in `environment.py` for local runs and in the CI workflow for GitHub Actions.
- Optional extras such as `[yaml]`, `[excel]`, `[sql]`, `[http]`, `[vault]`, and `[aws]` are not required for this example.
