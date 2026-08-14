Feature: Data steps

  Scenario: Set and assert a variable
    Given I set the variable "user_id" to "42"
    Then the variable "user_id" equals "42"
