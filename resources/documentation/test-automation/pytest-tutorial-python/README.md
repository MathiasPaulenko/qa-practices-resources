# Pytest Starter Companion

Runnable Python 3.11 + pytest 8.3 starter project that mirrors the
[QAPractices Pytest Tutorial for Python](https://qapractices.com/documentation/pytest-tutorial-python/).
It packages every snippet from the tutorial into a suite you can clone and run: Calculator and
checkout tests, fixtures via `conftest.py`, parametrization, markers, `pytest.ini`, coverage and an
HTML report, plus a GitHub Actions workflow that runs the same commands in CI.

## Structure

```text
pytest-starter/
├── requirements.txt      # pytest 8.3, pytest-cov, pytest-html, pytest-xdist
├── pytest.ini            # testpaths, addopts, registered markers
├── src/
│   ├── calculator.py     # add / subtract / divide (raises ValueError)
│   ├── checkout.py       # calculate_total with discount validation
│   └── csv_export.py     # export_csv used by the tmp_path example
└── tests/
    ├── conftest.py       # calculator and sample_orders fixtures + src on sys.path
    ├── test_calculator.py
    ├── test_checkout.py
    └── test_csv_export.py
```

## Quick start

```bash
cd pytest-starter
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest                                  # run the suite
pytest -m smoke                         # run only smoke tests
pytest --cov=src --cov-report=html      # coverage report in htmlcov/
pytest --html=report.html --self-contained-html
pytest -n auto                          # parallel run with pytest-xdist
```

Expected result: **16 tests, all passing** on pytest 8.3.

## Source

- EN: https://qapractices.com/documentation/pytest-tutorial-python/
- ES: https://qapractices.com/es/documentation/pytest-tutorial-python/
