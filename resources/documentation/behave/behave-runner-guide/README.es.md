# Ejemplo de Behave Runner para BDD de pagos

Esta carpeta contiene un proyecto **behave-runner** ejecutable que refleja el ejemplo de pagos de la guía de QAPractices [Guía CLI de behave-runner](https://qapractices.com/es/documentation/behave-runner-guide/).

Es una pequeña suite BDD de pagos con escenarios smoke, de regresión y críticos, más perfiles en `pyproject.toml` y un workflow de GitHub Actions.

## Estructura del proyecto

```text
payment-bdd/
├── .github/
│   └── workflows/
│       └── behave.yml
├── pyproject.toml
├── behave.ini
├── requirements-dev.txt
├── features/
│   ├── environment.py
│   ├── payment.feature
│   └── steps/
│       └── payment_steps.py
```

## Qué demuestra

- `features/payment.feature` tiene tres escenarios etiquetados con `@smoke`, `@critical` y `@regression`.
- `features/steps/payment_steps.py` implementa los pasos con un estado simple en memoria.
- `pyproject.toml` define un perfil `smoke` (filtro por tag) y un perfil `ci` (paralelismo, reporte JSON, salida `reports/report.json`).
- `behave.ini` muestra las mismas configuraciones usando la notación punto plana que soporta `behave-runner`.
- `.github/workflows/behave.yml` instala el runner, ejecuta el perfil `ci` y sube el reporte JSON como artifact.

## Correr localmente

```bash
cd payment-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
behave-runner run
```

Correr un perfil:

```bash
behave-runner run --profile smoke
```

Listar escenarios sin ejecutarlos:

```bash
behave-runner list --format json
```

Seleccionar solo escenarios smoke:

```bash
behave-runner select --tags '@smoke' --format names
```

Observar archivos durante el desarrollo:

```bash
behave-runner watch
```

Generar un reporte HTML:

```bash
behave-runner report generate --format html
```

## CI

El workflow de GitHub Actions ejecuta `behave-runner run --profile ci` y sube `reports/report.json` como artifact.
