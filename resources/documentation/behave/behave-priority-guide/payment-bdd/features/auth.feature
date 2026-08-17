Feature: Authentication

  @priority(1) @critical
  Scenario: Login with valid credentials
    Given a registered user
    When the user logs in
    Then the user should be authenticated

  @priority(2)
  Scenario: Login with invalid password
    Given a registered user
    When the user logs in with wrong password
    Then the login should fail
