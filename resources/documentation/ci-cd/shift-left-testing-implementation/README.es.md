# Companion de Implementación de Shift-Left Testing

Recurso complementario de la [Guía de Implementación de Shift-Left Testing](https://qapractices.com/es/documentation/shift-left-testing-implementation). Artefactos listos para copiar de los dos gates más baratos de la guía: el commit gate y el build gate.

## Archivos

| Archivo | Qué hace | Stack |
|---------|----------|-------|
| `build-gate.yml` | Workflow de GitHub Actions que bloquea merges si fallan tests o la cobertura | GitHub Actions, pytest, ruff |
| `.pre-commit-config.yaml` | Commit gate: lint/format con ruff + unit tests rápidos en cada commit | framework pre-commit |
| `check_coverage.py` | Parsea un reporte Cobertura XML y sale con error bajo un piso | Python 3.9+ stdlib |

## Quick Start

```bash
# Commit gate — instalar una vez por clon
pre-commit install

# Build gate — copiar el workflow a tu repo
mkdir -p .github/workflows scripts
cp build-gate.yml .github/workflows/build-gate.yml
cp check_coverage.py scripts/check_coverage.py

# Chequear un reporte de cobertura en local
pytest --cov=src --cov-report=xml
python scripts/check_coverage.py coverage.xml --floor 70
```

## Requisitos

- Python 3.9+ (check_coverage.py corre solo con la standard library)
- Paquete `pre-commit` para el commit gate
- El workflow asume `requirements.txt` y layout `src/` — ajustá los paths a tu proyecto

## Notas

- Poné `--floor` en tu número *actual* de cobertura y subilo mes a mes. Un piso muy por encima de la realidad se esquiva dentro de un sprint.
- Marcá los tests lentos con `@pytest.mark.slow` para que el commit gate quede bajo los dos minutos.
