Feature: REST API contract validation
  The users resource honours its HTTP contract — status codes, headers and
  body shape — across CRUD, error handling, security and boundary cases.

  Scenario: Created resources are addressable
    Given a valid POST /api/v1/users request
    When the API returns 201
    Then the Location header points to a retrievable resource

  Scenario: Updates are idempotent
    Given an existing user 42
    When the same PUT /api/v1/users/42 is sent twice
    Then both responses are equivalent
    And the resource state is unchanged between them

  Scenario: Missing resources return a clean 404
    Given no user exists with id 999999
    When GET /api/v1/users/999999 is requested
    Then the API returns 404
    And the error body contains an error or message field
    And no internal stack trace is exposed

  Scenario: Malformed JSON is rejected at the parse layer
    Given a POST body with truncated JSON
    When it is sent to /api/v1/users
    Then the API returns 400
    And no resource is created

  Scenario: Unauthenticated requests get a challenge
    Given a request without a Bearer token
    When it hits a protected endpoint
    Then the API returns 401
    And a WWW-Authenticate header is present

  Scenario: Users cannot touch other users' resources
    Given a valid token for user A
    And resource 42 belongs to user B
    When user A requests GET /api/v1/users/42
    Then the API returns 403 or 404
    And user B's data is not returned

  Scenario: Excess load is rejected politely
    Given the rate limit is exhausted
    When the client keeps sending requests
    Then the API returns 429 with Retry-After
    And clients can resume after the window resets
