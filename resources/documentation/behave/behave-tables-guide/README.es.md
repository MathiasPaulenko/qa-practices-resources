# Ejemplo de behave-tables — Reporte de Accesos de Usuarios

Esta carpeta contiene un proyecto ejecutable de **Behave** que acompaña la guía de QAPractices [Tablas de Behave Facilitadas](https://qapractices.com/es/documentation/behave-tables-guide/).

Demuestra cómo envolver tablas de datos de Behave con `behave-tables`, convertir filas a dicts, comparar tablas y exportar a CSV con `behave-tables==1.3.1` y `behave==1.3.3` en Python 3.11+.

## Estructura del proyecto

```text
user_access_report/
├── .github/workflows/behave-tables.yml
├── behave.ini
├── pyproject.toml
├── requirements.txt
├── access_service.py
└── features/
    ├── environment.py
    ├── access_report.feature
    └── steps/
        └── access_steps.py
```

`access_service.py` es un servicio en memoria usado por la suite BDD. `features/steps/access_steps.py` usa `behave-tables` para convertir, filtrar, comparar y exportar datos de tablas.

## Correr localmente

```bash
cd user_access_report
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture
```

Salida esperada:

```text
Feature: User access report

  @smoke
  Scenario: Active engineering users
    Given the system has the following users
    When I list the active users in the "eng" department
    Then I should see the following report

  @regression
  Scenario: Export the report as CSV
    Given the system has the following users
    When I export the report as CSV
    Then the CSV output should contain 2 active users

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
7 steps passed, 0 failed, 0 skipped
```
