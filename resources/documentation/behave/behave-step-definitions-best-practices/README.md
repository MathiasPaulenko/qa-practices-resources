# Behave Step Definitions Best Practices Shop Example

This folder contains a runnable **Behave BDD** project that mirrors the shop example from the QAPractices guide [Behave Step Definitions Best Practices](https://qapractices.com/documentation/behave-step-definitions-best-practices/).

It demonstrates custom `parse` types, split step modules, data tables, inventory alerts and regex-based step matching.

## Project structure

```text
shop-bdd/
├── pyproject.toml
├── requirements-dev.txt
├── behave.ini
├── shop_domain.py
└── features/
    ├── environment.py
    ├── order_discount.feature
    ├── product_catalog.feature
    ├── inventory_alerts.feature
    ├── order.feature
    └── steps/
        ├── shared.py
        ├── cart_steps.py
        ├── catalog_steps.py
        ├── inventory_steps.py
        └── order_steps.py
```

## What it demonstrates

- `features/steps/shared.py` registers `Money`, `Percentage` and `Availability` types once.
- `features/steps/cart_steps.py` uses `Money` and `Percentage` for cart and discount steps.
- `features/steps/catalog_steps.py` loads products from data tables and searches the catalog.
- `features/steps/inventory_steps.py` checks low-stock alerts.
- `features/steps/order_steps.py` uses a custom `OrderRef` parse pattern.
- `features/environment.py` resets per-scenario state (`catalog`, `cart`, `discount_engine`, `inventory`, `alert_service`).

## Run locally

```bash
cd shop-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
behave
```

Run only smoke scenarios:

```bash
behave --tags=smoke
```

List the step catalog without running:

```bash
behave --dry-run --format=steps.catalog
```
