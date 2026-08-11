Feature: Shopping cart voucher

  Background:
    Given the catalog price for "book" is 20.00

  @smoke
  Scenario Outline: Apply a voucher discount
    Given the cart contains <quantity> "book"
    When I apply a <discount>% voucher
    Then the cart total should be <total>

    Examples:
      | quantity | discount | total |
      | 1        | 0        | 20.00 |
      | 2        | 10       | 36.00 |
      | 3        | 15       | 51.00 |
