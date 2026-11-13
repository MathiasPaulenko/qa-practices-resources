Feature: Rewarded video grant
  Scenario: Reward granted after a complete view
    Given the rewarded ad is cached and the balance is 1000 coins
    When the player watches to completion and closes the end card
    Then the reward callback fires once and the balance is 1500 coins

  Scenario: Early close grants nothing
    Given the rewarded ad is cached
    When the player closes the video before completion
    Then no reward is granted and a new ad can be requested
