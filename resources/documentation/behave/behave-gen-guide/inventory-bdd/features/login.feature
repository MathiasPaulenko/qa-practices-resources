Feature: User session management
  A small example that shows how behave-gen scaffolds a feature and a step library.

  Scenario: Anonymous user is not authenticated
    Given I am not authenticated
    Then I should not be authenticated

  Scenario: User with a valid token is authenticated
    Given I am not authenticated
    And I have a session token "abc-123"
    Then I should be authenticated

  Scenario: Clearing the session removes authentication
    Given I have a session token "abc-123"
    When I clear the session
    Then I should not be authenticated
