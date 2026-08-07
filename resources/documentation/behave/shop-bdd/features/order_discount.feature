# features/order_discount.feature
Feature: Order discount rules

  @smoke
  Scenario: A bulk discount applies to a single SKU
    Given the product "TSHIRT-001" costs $20.00
    And the catalog has a bulk discount of 10% for at least 3 of "TSHIRT-001"
    When a customer adds 3 of "TSHIRT-001" to the cart
    Then the cart total should be $54.00

  @regression
  Scenario Outline: Bulk discounts are calculated per SKU
    Given the product "<sku>" costs <price>
    And the catalog has a bulk discount of <discount> for at least <min_qty> of "<sku>"
    When a customer adds <qty> of "<sku>" to the cart
    Then the cart total should be <total>

    Examples:
      | sku        | price   | min_qty | discount | qty | total   |
      | MUG-001    | $15.00  | 2       | 10%      | 2   | $27.00  |
      | TSHIRT-001 | $20.00  | 3       | 10%      | 3   | $54.00  |
      | TSHIRT-001 | $20.00  | 3       | 10%      | 1   | $20.00  |
