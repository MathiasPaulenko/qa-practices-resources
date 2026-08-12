# Ejemplo de behave-data — BDD de catálogo de productos

Esta carpeta contiene un proyecto **Behave** ejecutable que acompaña a la guía de QAPractices [Gestión de datos para Behave BDD](https://qapractices.com/es/documentation/behave-data-guide/).

Demuestra tablas tipadas, diff de tablas, ejemplos dinámicos cargados desde CSV y JSON, fixtures, builders y secretos enmascarados con `behave-data==1.0.2` y `behave==1.3.3` sobre Python 3.11+.

## Estructura del proyecto

```text
product_bdd/
├── .github/workflows/behave-data.yml
├── behave.ini
├── pyproject.toml
├── requirements.txt
├── product_catalog.py
└── features/
    ├── environment.py
    ├── products.feature
    ├── steps/product_steps.py
    └── data/
        ├── fixtures.py
        ├── products.csv
        ├── users.csv
        ├── prices.json
        └── secrets/
            └── .gitkeep
```

`product_catalog.py` es un catálogo en memoria que la suite BDD ejercita. `features/environment.py` inicializa `behave-data` con `setup_data`, registra el tipo custom `product_code` y conecta todos los hooks. `features/data/fixtures.py` define dos recetas `data_fixture` y un `data_builder`. `features/products.feature` es el Gherkin que ejercita cada funcionalidad del paquete.

## Ejecutar localmente

```bash
cd product_bdd
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
behave --no-capture
```

Output esperado:

```text
Feature: Product catalog data management

  @load_examples:csv:features/data/products.csv
  Scenario Outline: Bulk load products from CSV -- @1.1
    Given the catalog is empty
    When I import a product with name "T-Shirt", price 19.99, active "true" and stock 50
    Then the catalog should contain the product "T-Shirt"

  @load_examples:csv:features/data/products.csv
  Scenario Outline: Bulk load products from CSV -- @1.2
    Given the catalog is empty
    When I import a product with name "Mug", price 9.50, active "false" and stock 0
    Then the catalog should contain the product "Mug"

  @load_examples:csv:features/data/users.csv
  Scenario Outline: Load users from CSV and match fixtures -- @1.1
    Given a registered user "alice" with email "alice@qapractices.com" and role "user"
    Then the loaded user matches the fixture

  @load_examples:json:features/data/prices.json
  Scenario Outline: Load price tiers from JSON -- @1.1
    Given the catalog is empty
    When I import a price tier "basic" with sku "PRD-003" and price 5.99
    Then the catalog should contain the product "PRD-003"

  @needs_data:regular_user:alice
  Scenario: Declarative fixture tag loads a user
    Then the loaded user has username "alice" and role "user"

  @with_fixture:admin_user
  Scenario: Nested admin fixture references a regular user
    Then the admin has username "admin" and reports to user "alice"

  Scenario: Typed table conversion and diff
    When I add the following products
      | name:str | sku:product_code | price:float | active:bool | stock:int | released:date | description:str? |
      | T-Shirt  | PRD-001          | 19.99       | true        | 50        | 2025-03-15    |                  |
      | Mug      | PRD-002          | 9.50        | false       | 0         | 2025-04-01    | None             |
    Then the catalog should contain the following products
      | name:str | sku:product_code | price:float | active:bool | stock:int | released:date | description:str? |
      | T-Shirt  | PRD-001          | 19.99       | true        | 50        | 2025-03-15    |                  |
      | Mug      | PRD-002          | 9.50        | false       | 0         | 2025-04-01    | None             |

  Scenario: Build products with a data builder
    Given the catalog is empty
    When I build 3 "product" items with name prefix "Custom"
    Then the catalog should contain 3 products with name starting with "Custom"

  Scenario: Resolve and mask a secret from env
    When I resolve the API key from env
    Then the resolved value is masked in logs

1 feature passed, 0 failed, 0 skipped
12 scenarios passed, 0 failed, 0 skipped
28 steps passed, 0 failed, 0 skipped
```

## Qué demuestra

- `features/environment.py` muestra cómo llamar a `setup_data`, registrar un tipo custom y conectar `before_feature_hook`, `before_scenario_hook`, `before_step_hook` y `after_scenario_hook`.
- `features/products.feature` usa `@load_examples` desde CSV y JSON, encabezados de tabla tipados, tags `@needs_data` y `@with_fixture`, y un `Scenario Outline` con data builders.
- `features/steps/product_steps.py` usa `typed_wrap`, `diff`, `DataManager.resolve` y `DataManager.build`.
- `features/data/fixtures.py` define fixtures parametrizados y un fixture anidado con `ref:`.
- `behave.ini` configura `behave-data` a través de la sección `[behave.userdata]`.
- `.github/workflows/behave-data.yml` ejecuta la suite sobre Python 3.11, 3.12 y 3.13 y sube los reportes incluso cuando el job falla.

## Notas

- Los bloques `Examples` bajo `@load_examples` necesitan al menos una fila descartable porque Behave los parsea antes de que `before_feature_hook` pueda reemplazarlos con los datos cargados.
- La variable de entorno `CATALOG_API_KEY` se setea en `environment.py` para ejecuciones locales y en el workflow de CI para GitHub Actions.
- Los extras opcionales como `[yaml]`, `[excel]`, `[sql]`, `[http]`, `[vault]` y `[aws]` no son necesarios para este ejemplo.
