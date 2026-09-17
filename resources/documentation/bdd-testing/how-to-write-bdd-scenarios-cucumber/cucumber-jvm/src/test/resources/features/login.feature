Feature: User Login
  As a registered user
  I want to log in with my credentials
  So that I can reach my dashboard

  Background:
    Given I am on the login page

  @smoke
  Scenario: Successful login with valid credentials
    When I enter "jane@qapractices.com" in the email field
    And I enter "SecurePass123!" in the password field
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And I should see "Welcome"

  @regression @auth
  Scenario Outline: Login with various credentials
    When I enter "<email>" in the email field
    And I enter "<password>" in the password field
    And I click the "Login" button
    Then I should see "<message>"

    Examples:
      | email                 | password       | message             |
      | jane@qapractices.com  | SecurePass123! | Welcome             |
      | jane@qapractices.com  | wrong          | Invalid credentials |
      | ghost@qapractices.com | anypass        | User not found      |

  @regression
  Scenario: Login requires an email
    When I enter "SecurePass123!" in the password field
    And I click the "Login" button
    Then I should see "Email is required"

  @wip
  Scenario: Login with SSO
    When I log in with SSO
    Then I should see the dashboard
