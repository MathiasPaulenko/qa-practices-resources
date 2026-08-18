# Shop BDD — Demo de Suite Behave Saludable

Este es un proyecto mínimo de Behave BDD que demuestra una estructura de suite saludable e incluye un script `health_check.py` para auditarla.

## Qué contiene

- `shop.py` — pequeño dominio de catálogo y carrito.
- `features/shop.feature` — escenarios de carrito.
- `features/inventory.feature` — escenario de inventario.
- `features/steps/catalog_steps.py` — step compartido del catálogo con tipo `Price`.
- `features/steps/shop_steps.py` — step definitions del carrito.
- `features/steps/inventory_steps.py` — step definitions de inventario.
- `features/environment.py` — setup del contexto por escenario.
- `scripts/health_check.py` — detecta patterns de steps duplicados y tags riesgosos.
- `behave.ini` y `pyproject.toml` — configuración mínima del proyecto.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Correr la suite

```bash
behave --dry-run
behave
```

## Correr el health check

```bash
python scripts/health_check.py
```

## Guía completa

Consultá la [guía de QAPractices](https://qapractices.com/es/documentation/behave-healthy-bdd-suite-guide) para métricas, setup de CI, depuración y patrones de escalamiento.
