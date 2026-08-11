# Ejemplo de migración de Cucumber a Behave

Esta carpeta contiene un proyecto ejecutable con **Behave 1.2.6** que refleja los ejemplos de migración de la guía de QAPractices [Migrar de Cucumber a Behave: guía práctica BDD Python](https://qapractices.com/es/documentation/migrate-cucumber-to-behave/).

Muestra el mismo escenario Gherkin implementado después de migrar desde Cucumber-JVM o cucumber-js, con step definitions en Python, estado compartido basado en `context` y hooks en `environment.py`.

## Estructura del proyecto

```text
migrate-cucumber-to-behave/
└── cart_bdd/
    ├── behave.ini
    ├── pyproject.toml
    ├── requirements.txt
    ├── api_server.py
    ├── cart/
    │   ├── __init__.py
    │   └── service.py
    └── features/
        ├── environment.py
        ├── cart.feature
        ├── api.feature
        └── steps/
            ├── cart_steps.py
            ├── api_steps.py
            └── types.py
```

## Qué demuestra

- `cart/service.py` es el código de dominio bajo prueba (catálogo de productos y carrito).
- `features/cart.feature` es el escenario Gherkin migrado.
- `features/steps/cart_steps.py` es el equivalente en Python de los métodos originales Java `@Given`, `@When` y `@Then`.
- `features/steps/types.py` muestra cómo registrar un tipo de parámetro `Product` personalizado con `parse_type`.
- `features/steps/api_steps.py` muestra cómo migrar un escenario de API de `cucumber-js` a `requests` y `behave`.
- `features/environment.py` inicializa `context.catalog`, `context.cart`, `context.base_url` y `context.token` por escenario, e inicia/para el servidor mock de API mediante `before_all` / `after_all`.
- `api_server.py` es un mock mínimo de `http.server` que devuelve 200 y 404 para que el ejemplo de API corra sin conexión.
- `behave.ini` mantiene rutas, formateadores y `userdata` fuera del código de los steps.

## Ejecutar el escenario del carrito

```bash
cd cart_bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture features/cart.feature
```

Salida esperada:

```text
Feature: Add products to the shopping cart

  Scenario: Add a single product and check the total
    Given the product catalog contains "Book" priced at 15.00
    When the user adds 1 Book to the cart
    Then the cart total should be 15.00

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped
```

## Ejecutar el escenario de API

El escenario de API usa `requests` contra un servidor mock local que `environment.py` inicia en `before_all`. No requiere conexión a internet.

```bash
behave --tags=@api --no-capture
```

Salida esperada:

```text
Feature: API health check migrated from cucumber-js

  @api
  Scenario: GET a 200 response
    Given the API is available at "http://127.0.0.1:8765"
    When I GET "/status/200"
    Then the response status should be 200

  @api
  Scenario: GET a 404 response
    Given the API is available at "http://127.0.0.1:8765"
    When I GET "/status/404"
    Then the response status should be 404

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped
```

Para apuntarlo a tu propia API, configurá la variable de entorno `API_BASE_URL` o editá `behave.ini`:

```ini
[behave.userdata]
api_url = https://your-api.example.com
```

Luego actualizá `features/environment.py` para leer `config.userdata.get('api_url')`.
