Feature: Book catalog web UI

  @ui
  Scenario: Search for an available book
    Given the catalog contains "Clean Code" marked as available
    When I search for "Clean Code" in the web catalog
    Then the web result should show "Clean Code"

  @ui
  Scenario: Search for a missing book
    When I search for "DDD" in the web catalog
    Then the web result should show "Book not found"
