Feature: Catalog search

  @smoke
  Scenario: Find a book by title
    Given the catalog contains "Clean Code"
    When I search for "Clean Code"
    Then I should find 1 book
