Feature: Behave smoke wiring checks

  @smoke
  Scenario: before_all flag is available in steps
    Given the smoke context is initialized

  @smoke
  Scenario: Data table is parsed and passed into a step
    Given the following users exist
      | name  | role   |
      | Alice | admin  |
      | Bob   | reader |

  @smoke
  Scenario Outline: Login with multiple users
    Given I log in as "<username>" with role "<role>"

    Examples:
      | username | role  |
      | admin    | valid |
      | editor   | valid |
      | reader   | valid |

  @regression
  Scenario: Full login flow (skipped by smoke runs)
    Given a full login flow placeholder
