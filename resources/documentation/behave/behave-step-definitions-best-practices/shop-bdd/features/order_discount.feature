Feature: Order discount rules

  @smoke
  Scenario: A bulk discount applies to a single SKU
    Given the product "TSHIRT-001" costs $20.00
    And the catalog has a bulk discount of 10% for at least 3 of "TSHIRT-001"
    When a customer adds 3 of "TSHIRT-001" to the cart
    Then the cart total should be $54.00
