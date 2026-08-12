Feature: Product catalog data management

  @load_examples:csv:features/data/products.csv
  Scenario Outline: Bulk load products from CSV
    Given the catalog is empty
    When I import a product with name "<name>", price <price>, active "<active>" and stock <stock>
    Then the catalog should contain the product "<name>"

    Examples:
      | name | price | active | stock |
      | temp | 0.00  | false  | 0     |

  @load_examples:csv:features/data/users.csv
  Scenario Outline: Load users from CSV and match fixtures
    Given a registered user "<username>" with email "<email>" and role "<role>"
    Then the loaded user matches the fixture

    Examples:
      | username | email | role |
      | temp     | temp  | temp |

  @load_examples:json:features/data/prices.json
  Scenario Outline: Load price tiers from JSON
    Given the catalog is empty
    When I import a price tier "<tier>" with sku "<sku>" and price <price>
    Then the catalog should contain the product "<sku>"

    Examples:
      | sku | price | tier |
      | temp| 0.00  | temp |

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
