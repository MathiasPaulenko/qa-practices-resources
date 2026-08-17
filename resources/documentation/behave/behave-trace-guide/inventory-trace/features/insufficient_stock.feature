Feature: Over-selling protection

  Scenario: Reject an order that exceeds available stock
    Given the product "SKU-9000" starts with 2 units in stock
    When an order removes 5 units of "SKU-9000"
    Then the stock for "SKU-9000" should be 2 units
