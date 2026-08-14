Feature: Checkout cart

  Scenario: Calculate cart total
    Given the cart contains "SKU-123" priced at 29.99
    And the cart contains "SKU-456" priced at 15.50
    When I calculate the total
    Then the total should be 45.49
