# features/inventory_alerts.feature
Feature: Inventory stock alerts

  Background:
    Given the warehouse has the following stock levels:
      | SKU        | Quantity |
      | MUG-001    | 5        |
      | TSHIRT-001 | 100      |

  @smoke
  Scenario: A low stock alert is sent for a product below threshold
    When the system checks stock for "MUG-001" with threshold 10
    Then a low stock alert should be sent for "MUG-001"

  @regression
  Scenario: No alert is sent when stock is above threshold
    When the system checks stock for "TSHIRT-001" with threshold 10
    Then no low stock alert should be sent
