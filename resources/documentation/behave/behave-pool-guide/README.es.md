# Ejemplo de Checkout con Behave Pool

Esta carpeta contiene un proyecto ejecutable de **behave-pool** que refleja el ejemplo de ejecución en paralelo de la guía de QAPractices [Ejecución Paralela de Behave BDD con behave-pool](https://qapractices.com/es/documentation/behave-pool-guide/).

Es un pequeño `checkout-service` con escenarios de inventario, carrito y pago que demuestra paralelismo a nivel de feature, la etiqueta `@serial`, balanceo LPT y sharding entre runners en GitHub Actions.

## Estructura del proyecto

```text
checkout-service/
├── .github/
│   └── workflows/
│       └── behave-pool.yml
├── behave.ini
├── pyproject.toml
├── requirements.txt
├── checkout_service.py
├── features/
│   ├── environment.py
│   ├── inventory.feature
│   ├── checkout.feature
│   ├── payment.feature
│   └── steps/
│       └── checkout_steps.py
```

## Qué demuestra

- `checkout_service.py` es un pequeño servicio en memoria de inventario, carrito y pasarela de pago usado por el suite BDD.
- `features/inventory.feature` y `features/checkout.feature` corren en paralelo porque están aislados por feature.
- `features/payment.feature` contiene un escenario `@serial` que no puede solaparse con otros (mock de pasarela con rate limit).
- `behave.ini` selecciona el runner paralelo, pone `jobs = 4`, y configura balanceo LPT y el reporte JSON unificado.
- `.github/workflows/behave-pool.yml` corre un job local en paralelo y una matriz sharded.

## Correr localmente

```bash
cd checkout-service
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave
```

Salida esperada en Linux/macOS:

```text
Feature: Inventory reservation
  Scenario: Reserve in-stock item ... passed
  Scenario: Reserve another in-stock item ... passed

Feature: Checkout cart
  Scenario: Calculate cart total ... passed

Feature: Payment processing
  @serial
  Scenario: Charge a card through the rate-limited gateway ... passed

3 features passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
```

Después de la corrida, la raíz del proyecto contiene:

- `.behave-pool-timing.json` — duraciones históricas usadas por el scheduling LPT.
- `behave-pool-report.json` — artefacto unificado en formato `behave-modern-json-report`.

## Correr secuencialmente para depurar

```bash
behave --jobs 1
```

## Sharding en CI

El workflow de GitHub Actions escribe un `behave.ini` por shard, corre `behave features/` y sube cada `behave-pool-report.json` como un artefacto separado. El mismo patrón se puede adaptar a GitLab CI con `CI_NODE_INDEX` y `CI_NODE_TOTAL`.
