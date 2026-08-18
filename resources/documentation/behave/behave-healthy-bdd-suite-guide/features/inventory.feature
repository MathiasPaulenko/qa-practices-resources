Feature: Inventory

  @regression
  Scenario: Check stock for a title
    Given the catalog contains "Clean Code" priced at "$44.99"
    When the customer checks stock for "Clean Code"
    Then the stock count should be 10
