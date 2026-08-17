Feature: Inventory alerts

  @regression
  Scenario: Low stock triggers an alert
    Given the product "MUG-001" has a stock of 5
    When the stock alert threshold is 10
    Then an alert should be sent for "MUG-001"
