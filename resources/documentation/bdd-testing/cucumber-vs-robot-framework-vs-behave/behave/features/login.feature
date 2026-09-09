Feature: Login via API

  @smoke
  Scenario: Valid user logs in and reaches the dashboard
    Given a user account exists with "qa@qapractices.com" and "ValidPass!2026"
    When "qa@qapractices.com" logs in through the API with "ValidPass!2026"
    Then the API should respond with 200 and a token
    When the user requests the dashboard with the token
    Then the dashboard should respond with 200 and "Welcome to QA Practices"
