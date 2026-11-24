Feature: User login
  Scenario: Valid user can log in
    Given a user exists with email "alice@test.com"
    And the user has password "Secret123!"
    When the user attempts to log in with "alice@test.com" and "Secret123!"
    Then the user should be authenticated
    And a session token should be returned

  Scenario: Invalid password is rejected
    Given a user exists with email "alice@test.com"
    When the user attempts to log in with "alice@test.com" and "wrong"
    Then the login should fail
    And an error message "Invalid credentials" should be returned
