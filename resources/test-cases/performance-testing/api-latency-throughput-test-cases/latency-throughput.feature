Feature: API latency and throughput validation
  Companion scenarios for the API Latency & Throughput Test Cases at
  https://qapractices.com/test-cases/api-latency-throughput-test-cases/

  Scenario: API meets the latency SLA under normal load
    Given the latency baseline is recorded
    When 100 concurrent users send requests for 30 seconds
    Then p95 latency stays below the SLA threshold

  Scenario: Throughput degrades gracefully past the saturation point
    Given the saturation point is known
    When traffic exceeds it by 50 percent
    Then the error rate stays below 1 percent
    And the API recovers when the load drops

  Scenario: Rate limiting rejects excess requests
    Given a rate limit of 100 requests per minute is configured
    When the client sends 110 requests within one minute
    Then the first 100 requests succeed
    And the remaining requests are rejected with HTTP 429
    And the response includes a Retry-After header
