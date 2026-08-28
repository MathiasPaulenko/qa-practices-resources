# Proyecto Ejemplo Completo de Pytest

Proyecto complementario para la [Guía Completa de Pytest](https://qapractices.com/es/documentation/pytest-complete-guide/) en QAPractices.

## Qué incluye este proyecto

- `src/calculator.py` — clase de dominio simple para tests unitarios.
- `src/user_service.py` — cliente de API para usar con ejemplos de `pytest-mock`.
- `tests/conftest.py` — fixtures compartidas, fixture factory y fixture de sesión.
- `tests/unit/` — tests unitarios que cubren fixtures, parametrización, markers y mocking.
- `tests/integration/` — tests de integración marcados con `@pytest.mark.integration`.
- `.github/workflows/pytest.yml` — CI con matriz de Python y cobertura.
- `pytest.ini` — markers y opciones por defecto.
- `pyproject.toml` — metadatos del proyecto y configuración de cobertura.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
pytest
pytest -m smoke
pytest -m "not slow"
pytest -n auto
pytest --cov=src --cov-report=term-missing
```

## Estructura del proyecto

```text
pytest-complete/
├── src/
│   ├── calculator.py
│   └── user_service.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_calculator.py
│   │   ├── test_parametrize.py
│   │   ├── test_mocking.py
│   │   └── test_fixtures.py
│   └── integration/
│       └── test_user_service.py
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── .github/workflows/pytest.yml
```
