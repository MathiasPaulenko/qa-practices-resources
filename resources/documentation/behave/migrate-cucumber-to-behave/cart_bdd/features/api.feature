Feature: API health check migrated from cucumber-js

  @api
  Scenario: GET a 200 response
    Given the API is available at "http://127.0.0.1:8765"
    When I GET "/status/200"
    Then the response status should be 200

  @api
  Scenario: GET a 404 response
    Given the API is available at "http://127.0.0.1:8765"
    When I GET "/status/404"
    Then the response status should be 404
