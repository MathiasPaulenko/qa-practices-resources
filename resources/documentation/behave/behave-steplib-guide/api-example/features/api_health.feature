Feature: API health check with behave-steplib

  Scenario: GET a user returns 200 and JSON
    Given the API base url is "https://jsonplaceholder.typicode.com"
    When I send a GET request to "/users/1"
    Then the response status is 200
    And the response body is valid JSON
    And the JSON path "$.id" equals "1"
