Feature: User API tests with Karate 2.x

  Background:
    * url baseUrl
    * header Accept = 'application/json'

  Scenario: Get user by id
    Given path 'users', '1'
    When method get
    Then status 200
    And match response.id == 1
    And match response.username == 'Bret'
    And match response.email == '#string'
    And match response.email == '#regex .+@.+'

  Scenario: Unknown user returns 404
    Given path 'users', '999999'
    When method get
    Then status 404
