Feature: Payment processing

  @smoke @critical
  Scenario: Charge a valid card
    Given the cart total is 45.49
    When the card is charged
    Then the payment should be approved

  @regression
  Scenario: Reject a card with insufficient funds
    Given the cart total is 99.99
    And the card balance is 0.00
    When the card is charged
    Then the payment should be declined

  @smoke
  Scenario: Refund a previous charge
    Given a previous charge of 45.49
    When the refund is requested
    Then the balance should be 45.49
