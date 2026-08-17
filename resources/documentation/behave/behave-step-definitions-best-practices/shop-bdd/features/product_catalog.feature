Feature: Product catalog

  @regression
  Scenario: Search returns the right product
    Given the catalog contains the following products:
      | SKU        | Name        | Price   | Stock |
      | TSHIRT-001 | Camp Tee    | $20.00  | 100   |
      | MUG-001    | Glass Mug   | $15.00  | 5     |
    When a customer searches for "Camp Tee"
    Then the search results should contain 1 result
    And the first result should be "TSHIRT-001"
