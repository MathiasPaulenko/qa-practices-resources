# Casos de Prueba de Smoke para Behave BDD — Proyecto ejecutable

> Companion de [Casos de Prueba de Smoke para Behave BDD](https://qapractices.com/es/test-cases/behave-bdd-smoke-test-cases) en QAPractices.

Un proyecto Behave mínimo que implementa los chequeos de wiring del recurso: hooks de `environment.py`, filtrado por el tag `@smoke`, tablas de datos, scenario outlines, modo dry-run y códigos de salida.

## Requisitos

- Python 3.11, 3.12 o 3.13
- `behave==1.3.3`, `behave-steplib==1.5.1` (fijados en `requirements.txt`)

## Ejecutar

```bash
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt

behave --tags=smoke          # gate de smoke — 4 escenarios
behave --dry-run             # solo parseo + emparejamiento de steps, sin hooks
behave                       # suite completa, incluido @regression
behave --tags="smoke,~slow"  # ejemplo de expresión de tag negativa
```

Esperado: los escenarios `@smoke` pasan, el escenario `@regression` se salta con `--tags=smoke`, y un escenario fallido hace que el proceso salga con código 1.

## Archivos

- `behave.ini` — configuración de formatter y captura de salida.
- `features/environment.py` — hook `before_all` que define `context.global_flag` (TC-004).
- `features/smoke.feature` — escenarios `@smoke`, una tabla de datos, un scenario outline y un escenario `@regression` para el filtrado por tags (TC-003, TC-006, TC-007, TC-012).
- `features/steps/smoke_steps.py` — step definitions de los escenarios de smoke (TC-005).
