Feature: Stock reservation and reordering
  Companion scenarios for https://qapractices.com/test-cases/inventory-stock-management-testing/
  covering the highest-risk inventory behaviors: overselling prevention,
  reservation expiry and reorder alerts.

  Scenario: Concurrent buyers cannot oversell the last unit
    Given the product "SKU123" has 1 unit available
    When 10 buyers reserve 1 unit of "SKU123" simultaneously
    Then exactly 1 reservation succeeds
    And the remaining reservations receive an out-of-stock response

  Scenario: An abandoned checkout releases its reservation
    Given the product "SKU123" has 10 units available
    When a buyer reserves 3 units at checkout
    And the reservation TTL expires without payment
    Then 10 units are available again
    And the abandoned cart can no longer complete

  Scenario: Crossing the reorder threshold fires an alert
    Given the reorder threshold for "SKU123" is 20 units
    And the current stock is 22 units
    When an order for 5 units is placed
    Then the stock drops to 17
    And a reorder alert is fired for "SKU123"

  Scenario: FEFO allocation skips an expired batch
    Given batch "X" of "SKU123" expires in 10 days with 5 units
    And batch "Y" of "SKU123" expires in 90 days with 10 units
    When an order for 5 units is placed
    Then the units are allocated from batch "X" first
