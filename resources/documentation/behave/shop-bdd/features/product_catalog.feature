# features/product_catalog.feature
Feature: Product catalog search

  @smoke
  Scenario: Find a product by exact name
    Given the catalog contains the following products:
      | SKU        | Name       | Price  | Stock |
      | MUG-001    | Camp Mug   | $15.00 | 100   |
      | TSHIRT-001 | Camp Tee   | $20.00 | 50    |
    When a customer searches for "Camp Tee"
    Then the search results should contain 1 product
    And the first result should be "TSHIRT-001"
