# Behave BDD Shop Example

A complete, runnable Behave/Gherkin project used in the QAPractices guide:

- [Gherkin Best Practices for Behave](https://qapractices.com/documentation/gherkin-best-practices-behave/)

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
behave
```

## Test feature order

```bash
behave @order-a.txt
behave @order-b.txt
```

If the suite passes in one order and fails in another, you have scenario-order dependencies.

## Project structure

```text
shop-bdd/
  shop_domain.py            # domain model
  features/
    environment.py          # before_scenario setup
    steps/
      shop_steps.py         # step definitions
    order_discount.feature
    product_catalog.feature
    inventory_alerts.feature
    loyalty_benefits.feature
```
