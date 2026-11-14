# Companion del Tutorial de Pytest

Proyecto ejecutable de Python 3.11 + pytest 8.3 que replica el
[Tutorial de Pytest para Python de QAPractices](https://qapractices.com/es/documentation/pytest-tutorial-python/).
Empaqueta cada snippet del tutorial en una suite que puedes clonar y correr: tests de Calculator y
checkout, fixtures vía `conftest.py`, parametrización, markers, `pytest.ini`, cobertura y reporte
HTML, más un workflow de GitHub Actions que corre los mismos comandos en CI.

## Estructura

```text
pytest-starter/
├── requirements.txt      # pytest 8.3, pytest-cov, pytest-html, pytest-xdist
├── pytest.ini            # testpaths, addopts, markers registrados
├── src/
│   ├── calculator.py     # add / subtract / divide (lanza ValueError)
│   ├── checkout.py       # calculate_total con validación de descuento
│   └── csv_export.py     # export_csv usado por el ejemplo de tmp_path
└── tests/
    ├── conftest.py       # fixtures calculator y sample_orders + src en sys.path
    ├── test_calculator.py
    ├── test_checkout.py
    └── test_csv_export.py
```

## Inicio rápido

```bash
cd pytest-starter
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate en Windows
pip install -r requirements.txt
pytest                                  # correr la suite
pytest -m smoke                         # solo tests smoke
pytest --cov=src --cov-report=html      # reporte de cobertura en htmlcov/
pytest --html=report.html --self-contained-html
pytest -n auto                          # corrida paralela con pytest-xdist
```

Resultado esperado: **16 tests, todos en verde** con pytest 8.3.

## Fuente

- EN: https://qapractices.com/documentation/pytest-tutorial-python/
- ES: https://qapractices.com/es/documentation/pytest-tutorial-python/
