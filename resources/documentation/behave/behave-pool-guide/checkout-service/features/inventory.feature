Feature: Inventory reservation

  Scenario: Reserve in-stock item
    Given the inventory contains "SKU-123" with quantity 10
    When I reserve 2 units of "SKU-123"
    Then the available quantity of "SKU-123" should be 8

  Scenario: Reserve another in-stock item
    Given the inventory contains "SKU-456" with quantity 5
    When I reserve 1 units of "SKU-456"
    Then the available quantity of "SKU-456" should be 4
