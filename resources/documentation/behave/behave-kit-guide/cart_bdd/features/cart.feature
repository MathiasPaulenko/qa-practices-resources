Feature: Shopping cart with behave-kit

  @smoke
  Scenario: Add a single product and check the total
    Given the product catalog contains "Book" priced at 15.00
    When the user adds 1 Book to the cart
    Then the cart total should be 15.00

  @smoke
  Scenario Outline: Apply a voucher discount
    Given the product catalog contains "<product>" priced at <price>
    When the user adds <quantity> <product> to the cart
    And a <discount>% voucher is applied
    Then the cart total should be <total>

    Examples:
      | product | price | quantity | discount | total |
      | Book    | 15.00 | 1        | 0        | 15.00 |
      | Book    | 15.00 | 2        | 10       | 27.00 |

  @api
  Scenario: Load test users from CSV
    Given the test users are loaded from CSV
    Then there should be 2 users
