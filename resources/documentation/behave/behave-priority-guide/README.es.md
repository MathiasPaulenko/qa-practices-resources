# Ejemplo de Behave Priority para BDD de pagos

Esta carpeta contiene un proyecto ejecutable de **behave-priority** que refleja el ejemplo de pagos de la guía de QAPractices [Guía de Prioridad y Fail-Fast de Behave](https://qapractices.com/es/documentation/behave-priority-guide/).

Muestra cómo `@priority(N)`, `@critical` y `setup_priority()` ordenan escenarios y paran la suite temprano ante un fallo.

## Estructura del proyecto

```text
payment-bdd/
├── pyproject.toml
├── requirements.txt
├── behave.ini
└── features/
    ├── environment.py
    ├── auth.feature
    ├── payment.feature
    ├── reporting.feature
    └── steps/
        └── payment_steps.py
```

## Qué demuestra

- `features/auth.feature` tiene dos escenarios de login con `@priority(1)` y `@priority(2)`.
- `features/payment.feature` tiene escenarios de pago y reembolso en `@priority(3)` y `@priority(5)`.
- `features/reporting.feature` tiene un escenario sin tag de prioridad, así que usa el default `999`.
- `features/environment.py` conecta `setup_priority(..., order=True, stop_after_failures=1, stop_on_critical=True, report=True)`.
- Un escenario levanta `AssertionError` a propósito para mostrar el fail-fast deteniendo la ejecución.

## Correr localmente

```bash
cd payment-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave
```

La suite corre en orden de prioridad y se detiene después del primer escenario crítico fallido.
