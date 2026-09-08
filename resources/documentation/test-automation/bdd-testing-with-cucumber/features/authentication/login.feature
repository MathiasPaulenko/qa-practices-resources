Feature: User authentication
  As a registered user
  I want to sign in with my email and password
  So that I can access my account securely

  Background:
    Given a registered user with email "alice@qa.local" and password "ValidPass1"

  @smoke
  Scenario: Successful login with valid credentials
    When the user enters their credentials and clicks "Sign In"
    Then the user should be redirected to "/dashboard"
    And the welcome message should display "Welcome back, Alice"

  @regression
  Scenario: Failed login with invalid password
    When the user enters email "alice@qa.local" and password "wrongpassword"
    And clicks "Sign In"
    Then the login error message should display "Invalid email or password"
    And the user should remain on "/login"
