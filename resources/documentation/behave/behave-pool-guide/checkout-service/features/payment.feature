Feature: Payment processing

  @serial
  Scenario: Charge a card through the rate-limited gateway
    Given the cart total is 45.49
    When I charge the card
    Then the payment should be approved
