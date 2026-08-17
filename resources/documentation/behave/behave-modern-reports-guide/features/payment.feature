Feature: Payment processing

  Scenario: Successful payment
    Given the checkout total is "$54.99"
    When the customer pays with a valid card
    Then the payment is authorized

  Scenario: Declined payment
    Given the checkout total is "$54.99"
    When the customer pays with a declined card
    Then the payment is declined
