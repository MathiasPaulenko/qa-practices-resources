Feature: Auth

  @Login @Web
  Scenario: login works
    Given the user is on the login page
    When the user enters "admin" and "password123" into the login form
    And the user calls the API with "Authorization: Bearer sk-abc123secret"
    Then the user should be redirected to the dashboard

  @Login @web
  Scenario: login works
    Given the user is on the login page
    When the user enters "Admin" and "Secret99!" into the login form
    Then the user should be redirected to the dashboard

  Scenario: forgot password flow
    Given the user is on the forgot password page
    When the user submits "qa@qapractices.com" and "2024-03-15".
    Then a reset email should be sent.
