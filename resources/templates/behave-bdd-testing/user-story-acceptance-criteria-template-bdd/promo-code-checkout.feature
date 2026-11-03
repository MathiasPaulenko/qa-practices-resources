Feature: Promo codes at checkout
  As a returning customer
  I want to apply a promo code at checkout
  So that I pay the discounted price advertised in the campaign

  Background:
    Given the customer has $120.00 of items in the cart
    And they are on the checkout page

  Scenario: Valid percentage code applies the discount
    When the customer enters the code "WELCOME10"
    And they click "Apply"
    Then the order summary shows a discount of $12.00
    And the order total updates to $108.00

  Scenario: Expired code is rejected with a clear message
    Given the code "SUMMER25" expired on 2025-09-01
    When the customer enters the code "SUMMER25"
    And they click "Apply"
    Then they see the message "This promo code has expired"
    And the order total stays at $120.00

  Scenario: Code below the minimum spend is rejected
    Given the code "SAVE15" requires a minimum spend of $150.00
    When the customer enters the code "SAVE15"
    And they click "Apply"
    Then they see the message "Add $30.00 more to use this code"
    And no discount is applied

  Scenario Outline: Code entry is validated before lookup
    When the customer enters "<input>" in the promo code field
    And they click "Apply"
    Then they see the message "<message>"

    Examples:
      | input      | message                            |
      |            | Enter a promo code                 |
      | wel come10 | Promo codes can't contain spaces   |
      | FAKE-999   | We don't recognize that promo code |
      | WELCOME10  | Promo code applied                 |

  Scenario: Removing an item drops the order below the minimum spend
    Given the code "SAVE15" is applied with a $100.00 minimum spend
    When the customer removes an item and the subtotal falls to $95.00
    Then the discount is removed automatically
    And they see "Promo code removed: minimum spend not met"
