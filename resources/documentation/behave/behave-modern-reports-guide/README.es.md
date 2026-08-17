# Payment Reports — Demo de Informes Modernos para Behave

Este es un proyecto mínimo de Behave que muestra cómo generar múltiples formatos de informe desde una misma suite.

## Qué contiene

- `features/payment.feature` — dos escenarios simples de pago.
- `features/steps/payment_steps.py` — step definitions correspondientes.
- `behave.ini` — todos los formateadores de informes modernos pre-registrados.
- `pyproject.toml` — extras opcionales para cada paquete de informes.
- `environment.py` — hooks de entorno.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[ci]"
mkdir -p reports
```

## Correr un informe

```bash
# Markdown
behave -f markdown -o reports/report.md

# JSON
behave -f modern-json -o reports/report.json

# HTML
behave -f modern-html -o reports/report.html

# CSV
behave -f csv -o reports/report.csv

# XLSX
behave -f xlsx -o reports/report.xlsx

# TXT
behave -f modern-txt -o reports/report.txt

# Consola (en Windows configurá PYTHONIOENCODING=utf-8)
behave -f modern-console
```

## Nota para consola en Windows

Si el formateador de consola falla con `UnicodeEncodeError`, configurá `PYTHONIOENCODING=utf-8` antes de correr:

```powershell
$env:PYTHONIOENCODING = "utf-8"
behave -f modern-console
```

## Guía completa

Consultá la [guía de QAPractices](https://qapractices.com/es/documentation/behave-modern-reports-guide) para setup, ejemplos de CI, depuración y tablas de decisión.
