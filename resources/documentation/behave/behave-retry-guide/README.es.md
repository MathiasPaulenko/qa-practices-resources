# Ejemplo de Behave Retry para BDD de pagos

Esta carpeta contiene un proyecto ejecutable de **behave-retry** que refleja el ejemplo de pagos de la guía de QAPractices [Guía de Behave Retry](https://qapractices.com/es/documentation/behave-retry-guide/).

Muestra cómo los tags `@flaky` y `@retry:N` hacen que Behave vuelva a ejecutar escenarios fallidos que coinciden con excepciones específicas.

## Estructura del proyecto

```text
payment-bdd/
├── pyproject.toml
├── requirements.txt
├── behave.ini
└── features/
    ├── environment.py
    ├── payment.feature
    └── steps/
        └── payment_steps.py
```

## Qué demuestra

- `features/payment.feature` tiene tres escenarios.
- El escenario `@flaky` de cargo falla una vez con `TimeoutError` y luego pasa en el reintento.
- El escenario `@flaky @retry:3` de reembolso sobreescribe `max_retries` y pasa en el tercer intento.
- El escenario normal de cargo no se reintenta.
- `features/environment.py` conecta `setup_retry()` con `max_retries=2`, filtrado por tags y backoff exponencial.

## Correr localmente

```bash
cd payment-bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave
```

El reporte de reintentos al final muestra cuántos escenarios se reintentaron y cuántos pasaron en el reintento.
