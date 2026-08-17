Feature: Payment processing

  @priority(3)
  Scenario: Charge a card
    Given the cart total is 45.49
    When the card is charged
    Then the payment should be approved

  @priority(5)
  Scenario: Refund a charge
    Given a previous charge of 45.49
    When the refund is requested
    Then the balance should be 45.49
