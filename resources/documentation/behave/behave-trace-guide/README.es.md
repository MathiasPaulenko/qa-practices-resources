# Ejemplo de inventario con Behave Trace

Esta carpeta contiene un proyecto ejecutable de **behave-trace** que refleja el ejemplo de inventario de la guía de QAPractices [Guía de Behave Trace](https://qapractices.com/es/documentation/behave-trace-guide/).

Es una suite mínima de Behave BDD que muestra cómo `behave-trace 1.3.1` captura resultados de steps, logs, adjuntos de texto y un escenario fallido.

## Estructura del proyecto

```text
inventory-trace/
├── pyproject.toml
├── behave.ini
├── requirements-dev.txt
├── inventory_service.py
└── features/
    ├── environment.py
    ├── inventory.feature
    ├── insufficient_stock.feature
    └── steps/
        └── inventory_steps.py
```

## Qué demuestra

- `features/inventory.feature` tiene dos escenarios que pasan (envío y pedido).
- `features/insufficient_stock.feature` tiene un escenario que falla intencionalmente con un `ValueError`, para que puedas inspeccionar la traza.
- `features/environment.py` adjunta una nota `step.txt` y registra logs después de cada step.
- `behave.ini` selecciona el formatter `behave-trace` y escribe `trace.json`.
- `pyproject.toml` fija `behave==1.3.3` y `behave-trace==1.3.1`.
- `.github/workflows/behave-trace.yml` genera la traza en CI y la sube como artefacto cuando un escenario falla.

## Correr localmente

```bash
cd inventory-trace
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
behave
```

Abrí la traza en el viewer:

```bash
behave-trace show trace.json
```

Corré con `behave-trace run` para recarga en vivo:

```bash
behave-trace run . --watch
```

## CI

El workflow de GitHub Actions corre `behave --format behave-trace -o trace.json` y sube `trace.json` como artefacto solo cuando la suite falla.

## Nota

El `insufficient_stock.feature` falla intencionalmente. Está ahí para mostrar cómo `behave-trace` registra el error, el step `Then` saltado y los logs adjuntos.
