Feature: IO steps

  Scenario: Create and verify a directory
    Given I create the directory "reports"
    Then the directory "reports" exists
