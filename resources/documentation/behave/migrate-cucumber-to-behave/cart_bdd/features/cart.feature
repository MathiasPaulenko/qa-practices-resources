Feature: Add products to the shopping cart

  @smoke
  Scenario: Add a single product and check the total
    Given the product catalog contains "Book" priced at 15.00
    When the user adds 1 Book to the cart
    Then the cart total should be 15.00
