Feature: Reporting

  Scenario: Generate daily summary
    Given there are completed payments
    When the summary is generated
    Then the report should contain payments
