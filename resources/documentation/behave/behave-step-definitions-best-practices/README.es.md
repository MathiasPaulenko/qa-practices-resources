# Ejemplo de tienda para las mejores prácticas de step definitions en Behave

Esta carpeta contiene un proyecto ejecutable de **Behave BDD** que refleja el ejemplo de tienda de la guía de QAPractices [Mejores prácticas de Step Definitions para Behave](https://qapractices.com/es/documentation/behave-step-definitions-best-practices/).

Demuestra tipos `parse` personalizados, módulos de steps separados, tablas de datos, alertas de inventario y matching de steps con regex.

## Estructura del proyecto

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

## Qué demuestra

- `features/steps/shared.py` registra los tipos `Money`, `Percentage` y `Availability` una sola vez.
- `features/steps/cart_steps.py` usa `Money` y `Percentage` para steps de carrito y descuentos.
- `features/steps/catalog_steps.py` carga productos desde tablas de datos y busca en el catálogo.
- `features/steps/inventory_steps.py` verifica alertas de stock bajo.
- `features/steps/order_steps.py` usa un patrón parse personalizado `OrderRef`.
- `features/environment.py` resetea el estado por escenario (`catalog`, `cart`, `discount_engine`, `inventory`, `alert_service`).

## Correr localmente

```bash
cd shop-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
behave
```

Correr solo los escenarios smoke:

```bash
behave --tags=smoke
```

Listar el catálogo de steps sin ejecutar:

```bash
behave --dry-run --format=steps.catalog
```
