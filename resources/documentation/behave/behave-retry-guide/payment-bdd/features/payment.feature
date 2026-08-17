Feature: Payment processing

  @flaky
  Scenario: Charge a card with slow gateway
    Given the gateway is slow
    When the card is charged
    Then the payment should be approved

  Scenario: Charge a card normally
    Given the gateway is responsive
    When the card is charged
    Then the payment should be approved

  @flaky @retry:3
  Scenario: Refund a charge with intermittent error
    Given the refund service is intermittent
    When the refund is requested
    Then the balance should be 45.49
