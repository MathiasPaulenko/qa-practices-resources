Feature: User access report

  @smoke
  Scenario: Active engineering users
    Given the system has the following users
      | user    | role        | department | active |
      | alice   | engineer    | eng        | true   |
      | bob     | designer    | design     | true   |
      | carol   | engineer    | eng        | false  |
      | dave    | engineer    | eng        | true   |
    When I list the active users in the "eng" department
    Then I should see the following report
      | user  | role     | department | active |
      | alice | engineer | eng        | true   |
      | dave  | engineer | eng        | true   |

  @regression
  Scenario: Export the report as CSV
    Given the system has the following users
      | user    | role        | department | active |
      | alice   | engineer    | eng        | true   |
      | bob     | designer    | design     | true   |
    When I export the report as CSV
    Then the CSV output should contain 2 active users
