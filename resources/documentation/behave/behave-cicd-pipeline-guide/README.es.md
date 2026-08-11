# Ejemplo de pipeline CI/CD con Behave

Esta carpeta contiene un proyecto ejecutable con **Behave** que refleja el ejemplo de pipeline CI/CD de la guía de QAPractices [Behave CI/CD Pipeline Guide](https://qapractices.com/es/documentation/behave-cicd-pipeline-guide/).

Es un pequeño servicio de catálogo de libros con un workflow de GitHub Actions que ejecuta la suite en Python 3.11, 3.12 y 3.13, produce reportes JUnit XML y JSON, y sube artefactos aunque el job falle.

## Estructura del proyecto

```text
book-catalog/
├── .github/
│   └── workflows/
│       └── behave.yml
├── behave.ini
├── pyproject.toml
├── requirements-dev.txt
├── catalog_service.py
├── discover_features.py
├── features/
│   ├── environment.py
│   ├── catalog.feature
│   └── steps/
│       └── catalog_steps.py
└── reports/
    └── .gitkeep
```

## Qué demuestra

- `catalog_service.py` es un catálogo en memoria usado por la suite BDD.
- `features/catalog.feature` contiene un escenario `@smoke`.
- `features/steps/catalog_steps.py` mapea los pasos Gherkin a Python.
- `features/environment.py` inicializa `context.catalog` antes de cada escenario y lee `base_url` desde `userdata` de `behave.ini`.
- `behave.ini` desactiva el color, escribe `reports/behave-report.json` y `reports/junit/*.xml`, y excluye las etiquetas `@skip` y `@manual`.
- `.github/workflows/behave.yml` es el workflow de GitHub Actions con matriz y `if: always()` en la subida de artefactos.
- `discover_features.py` es el script de descubrimiento de shards usado en el ejemplo de ejecución paralela.
- `pyproject.toml` y `requirements-dev.txt` fijan las mismas dependencias.

## Ejecutar localmente

```bash
cd book-catalog
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
mkdir -p reports
behave
```

Salida esperada:

```text
Feature: Catalog search

  @smoke
  Scenario: Find a book by title
    Given the catalog contains "Clean Code"
    When I search for "Clean Code"
    Then I should find 1 book

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped
```

Después de la corrida, `reports/` contiene:

- `behave-report.json` — reporte JSON legible.
- `junit/TESTS-catalog.xml` — JUnit XML para dashboards de CI.

## Ejecutar con behavex

```bash
behavex --parallel-processes=4 --parallel-scheme=feature
```

## Descubrir shards de features

```bash
python discover_features.py
```
