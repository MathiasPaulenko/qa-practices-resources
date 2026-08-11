# Ejemplo de carrito con Behave vs pytest-bdd

Esta carpeta contiene el mismo escenario Gherkin de carrito de compras implementado con **Behave 1.2.6** y **pytest-bdd 7.x**.

Es el proyecto complementario de:

- [Behave vs pytest-bdd: elige la herramienta BDD de Python](https://qapractices.com/es/documentation/behave-vs-pytest-bdd/)

## Estructura del proyecto

```text
behave-vs-pytest-bdd/
├── behave-cart/
│   ├── features/
│   │   ├── cart.feature
│   │   ├── environment.py
│   │   └── steps/
│   │       └── cart_steps.py
│   ├── pyproject.toml
│   └── requirements.txt
└── pytest-bdd-cart/
    ├── features/
    │   └── cart.feature
    ├── conftest.py
    ├── test_cart.py
    ├── pyproject.toml
    └── requirements.txt
```

## Ejecutar el proyecto de Behave

```bash
cd behave-cart
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -r requirements.txt
behave
```

## Ejecutar el proyecto de pytest-bdd

```bash
cd pytest-bdd-cart
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate en Windows
pip install -r requirements.txt
pytest -v
```

## Qué comparar

- `cart.feature` es idéntico en ambos proyectos.
- `behave-cart/features/environment.py` inicializa el objeto `context` compartido.
- `pytest-bdd-cart/conftest.py` define la fixture `state`.
- Ambos suites producen tres tests parametrizados a partir de la tabla `Examples`.
