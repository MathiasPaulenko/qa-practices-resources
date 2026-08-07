Feature: Book catalog search with SQLite

  @db @smoke
  Scenario: Find an available book in the SQLite catalog
    Given the catalog contains "Clean Code" marked as available
    When I search for "Clean Code"
    Then I should find 1 result
    And the result should be available

  @db @regression
  Scenario: Find an unavailable book in the SQLite catalog
    Given the catalog contains "Refactoring" marked as unavailable
    When I search for "Refactoring"
    Then I should find 1 result
    And the result should be unavailable
