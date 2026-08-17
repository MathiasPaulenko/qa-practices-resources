Feature: Inventory stock adjustments

  Scenario: Increase stock when a shipment arrives
    Given the product "SKU-1234" starts with 10 units in stock
    When a shipment adds 5 units of "SKU-1234"
    Then the stock for "SKU-1234" should be 15 units

  Scenario: Decrease stock when an order is placed
    Given the product "SKU-5678" starts with 8 units in stock
    When an order removes 3 units of "SKU-5678"
    Then the stock for "SKU-5678" should be 5 units
