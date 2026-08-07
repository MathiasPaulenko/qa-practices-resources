Feature: Book catalog search

  @smoke
  Scenario: Find a book by title
    Given the catalog contains "Clean Code"
    When I search for "Clean Code"
    Then I should find 1 result

  @regression
  Scenario Outline: Search returns the expected availability
    Given the catalog contains "<title>" marked as <availability>
    When I search for "<title>"
    Then I should find 1 result
    And the result should be <expected>

    Examples:
      | title       | availability | expected     |
      | Refactoring | unavailable  | unavailable  |
      | Clean Code  | available    | available    |

  @regression
  Scenario Outline: Search by title returns the expected count
    Given the catalog contains "<first>"
    And the catalog contains "<second>"
    When I search for "<title>"
    Then I should find <count> <label>

    Examples:
      | first      | second      | title       | count | label   |
      | Clean Code | Refactoring | Clean Code  | 1     | result  |
      | Clean Code | Refactoring | Refactoring | 1     | result  |
      | Clean Code | Refactoring | DDD         | 0     | results |

  @regression
  Scenario: Load books from a data table
    Given the catalog contains the following books:
      | Title                    | Available |
      | Clean Code               | true      |
      | Refactoring              | false     |
      | The Pragmatic Programmer | true      |
    When I search for "Refactoring"
    Then the result should be unavailable
