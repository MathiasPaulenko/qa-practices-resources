@smoke @critical
Feature: Checkout

  @regression @payment
  Scenario: Credit card payment
    Given a registered user is logged in
    When the user proceeds to checkout with a valid credit card
    Then the payment should be processed successfully
    And the order confirmation should be displayed

  @skip @flaky
  Scenario: PayPal payment
    Given a registered user is logged in
    When the user proceeds to checkout with PayPal
    Then the payment should be processed successfully
