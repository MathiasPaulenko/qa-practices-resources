# Ejemplo de utilidades de Behave Kit

Esta carpeta contiene un proyecto ejecutable con **Behave 1.2.6** y **behave-kit 1.5.0**. Es el proyecto complementario de la guía de QAPractices [Utilidades de Behave Kit para tests BDD](https://qapractices.com/es/documentation/behave-kit-guide/).

Demuestra las características más útiles de `behave-kit` en una pequeña suite de carrito de compras:

- Soft assertions con `assert_soft` y `assert_soft_equals`.
- `TypedContext` con una clase esquema.
- Skip condicional con `@skip_if_env`.
- `env()` para lecturas tipadas de variables de entorno.
- `load_data()` para archivos CSV/JSON.
- Fixtures basados en tags con `@fixture`.
- Steps basados en clases con `step_impl_base()`.
- `run_steps()` para ejecución de sub-steps.
- Timeout por escenario con `@timeout:N`.

## Estructura del proyecto

```text
behave-kit-guide/
└── cart_bdd/
    ├── behave.ini
    ├── pyproject.toml
    ├── requirements.txt
    ├── catalog_service.py
    ├── tests/
    │   └── data/
    │       └── users.csv
    └── features/
        ├── environment.py
        ├── cart.feature
        └── steps/
            ├── cart_steps.py
            └── fixtures.py
```

## Ejecutar el ejemplo del carrito

```bash
cd cart_bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture
```

Salida esperada:

```text
4 scenarios passed, 0 failed, 0 skipped
13 steps passed, 0 failed, 0 skipped
```

## Explorar características individuales

- `features/steps/cart_steps.py` — soft assertions y `TypedContext`.
- `features/steps/fixtures.py` — fixtures por tags y skips condicionales.
- `features/environment.py` — `setup()` y activación de soft asserts.
- `catalog_service.py` — pequeño código de dominio bajo prueba.
- `tests/data/users.csv` — archivo de datos usado por `load_data`.

## Extras opcionales

Para archivos de datos YAML o Excel instalá los extras:

```bash
pip install "behave-kit[yaml,excel,dotenv]"
```
