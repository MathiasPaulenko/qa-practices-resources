@password-reset
Feature: Password reset via email
  Registered customers regain account access through a single-use,
  time-limited reset link sent by email.

  Background:
    Given a registered customer account exists for "ana@acme-shop.test"

  @smoke
  Scenario: Request a reset link with a valid email
    When the customer requests a password reset for "ana@acme-shop.test"
    Then a reset email is sent to that address
    And the message contains a signed, single-use reset link

  Scenario: Reset link expires after 24 hours
    Given the customer requested a reset link 25 hours ago
    When the customer opens the link and submits a new password
    Then the link is rejected as expired
    And the previous password still works

  @negative
  Scenario: A used reset link cannot be replayed
    Given the customer already completed a reset with the link
    When the customer opens the same link again
    Then the link is rejected as already used

  @regression
  Scenario Outline: New passwords must satisfy the complexity rules
    Given the customer opened a valid reset link
    When the customer submits "<password>" as the new password
    Then the reset is "<result>"

    Examples:
      | password        | result                       |
      | short1!         | rejected: too short          |
      | alllowercase12! | rejected: missing uppercase  |
      | NoDigitPass!    | rejected: missing digit      |
      | Valid#Pass2026  | accepted                     |

  @negative
  Scenario: The old password stops working after a reset
    Given the customer completed a password reset
    When the customer logs in with the previous password
    Then access is denied
    And a confirmation email was sent after the reset
