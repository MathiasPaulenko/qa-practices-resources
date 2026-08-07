# Ejemplo de tienda con Behave BDD

Proyecto completo y ejecutable de Behave/Gherkin usado en las guías de QAPractices:

- [Gherkin Best Practices for Behave](https://qapractices.com/es/documentation/gherkin-best-practices-behave/)
- [Behave BDD Project Setup Guide](https://qapractices.com/es/documentation/behave-bdd-project-setup-guide/)

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -r requirements-dev.txt
behave
```

## Probar el orden de ejecución

```bash
behave @order-a.txt
behave @order-b.txt
```

Si el suite pasa en un orden y falla en otro, tenés dependencias entre escenarios.

## Estructura del proyecto

```text
shop-bdd/
  shop_domain.py            # modelo de dominio
  features/
    environment.py          # setup de before_scenario
    steps/
      shop_steps.py         # definiciones de pasos
    order_discount.feature
    product_catalog.feature
    inventory_alerts.feature
    loyalty_benefits.feature
```
