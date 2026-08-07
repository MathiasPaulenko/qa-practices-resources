# features/loyalty_benefits.feature
Feature: Loyalty tier benefits

  @regression
  Scenario Outline: A customer receives the correct tier discount
    Given the customer has spent <lifetime_spend> in the last year
    When the customer checks their tier discount
    Then the discount should be <discount>
    And the tier name should be <tier>

    Examples:
      | lifetime_spend | discount | tier   |
      | $0.00          | 0%       | bronze |
      | $50.00         | 0%       | bronze |
      | $5,000.00      | 5%       | silver |
      | $15,000.00     | 10%      | gold   |
