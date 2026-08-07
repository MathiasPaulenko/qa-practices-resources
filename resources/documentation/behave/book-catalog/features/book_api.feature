Feature: Book lookup API

  Background:
    Given the API catalog contains the following books:
      | Title       | Available |
      | Clean Code  | true      |
      | Refactoring | false     |

  @api
  Scenario: Request a book that is in the catalog
    When I request the book "Clean Code"
    Then the API returns 200
    And the response shows it is available

  @api
  Scenario: Request a missing book
    When I request the book "DDD"
    Then the API returns 404
