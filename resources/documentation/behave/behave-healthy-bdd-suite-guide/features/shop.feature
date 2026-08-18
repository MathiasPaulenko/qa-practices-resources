Feature: Shopping cart

  @smoke
  Scenario: Add a book to the cart
    Given the catalog contains "Clean Code" priced at "$44.99"
    When the customer adds "Clean Code" to the cart
    Then the cart total should be "$44.99"

  @regression
  Scenario: Apply a discount
    Given the catalog contains "Refactoring" priced at "$39.99"
    And the customer adds "Refactoring" to the cart
    When a "10%" discount is applied
    Then the cart total should be "$35.99"
