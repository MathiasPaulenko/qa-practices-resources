
That taught me that third-party APIs are dependencies I don't control. Testing them means covering their failure modes as carefully as their happy paths.

![Third-party API integration test flow: auth, rate limit, request, provider response, schema validation, fallback, webhook signature validation](/assets/images/diagrams/third-party-api-integration-flow.svg)

**What are these test cases?** I wrote them as a reusable, step-by-step suite I run before shipping any feature that depends on an external API. They cover authentication, rate limits, timeouts, retries, fallbacks, webhooks and schema changes. For related guidance, see [REST API Testing Best Practices](/documentation/rest-api-testing-best-practices) and [API Mocking with WireMock](/documentation/api-mocking-with-wiremock).

## When to Use

I run these cases whenever the app hands off control to a service I can't fix myself. Common triggers:

- **New third-party integration:** before shipping any feature that depends on an external API.
- **Provider contract updates:** after any changelog entry that could change payloads or status codes.
- **Rate limit changes:** when the provider introduces new tiers or throttling rules.
- **Disaster recovery drills:** simulate provider downtime and verify fallback behavior.
- **Migration between providers:** validate parity between old and new integrations.

## Test Cases

### Edge Cases and Boundary Values

These are the boundaries that separate a working integration from a broken one. I keep them as a separate checklist because the provider's docs rarely mention them explicitly.

| Scenario | Input | Boundary / Edge Type | Expected Result | Automation Note | Priority |
|---|---|---|---|---|---|
| Request with expired OAuth token | `Authorization: Bearer expired-token` | Token expiry boundary | HTTP 401 or 403 with a clear token expired message | pytest + requests | High |
| Request at exact rate limit threshold | 999th request of a 1,000 req/min limit | Rate limit boundary | Request succeeds; next request returns 429 with `Retry-After` | k6 / Locust | High |
| Provider returns 503 with no fallback configured | Forced 503 from mock provider | Provider outage boundary | Circuit opens or user sees a graceful error within the SLA | WireMock + toxiproxy | High |
| Webhook with invalid signature | `X-Signature` header doesn't match payload | Webhook integrity boundary | Webhook is rejected with HTTP 400; no action is processed | Flask test client | High |
| Payload one byte over provider limit | Body of `max_size + 1` bytes | Size boundary | HTTP 413 Payload Too Large or equivalent provider error | pytest + requests | Medium |

### TC-001: Authenticate with Valid Credentials

Before testing failure modes, prove the happy path works against the provider's sandbox.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-001 | Authenticate with valid API key or OAuth token | Valid credentials configured for the sandbox environment | Sandbox API key and OAuth token | 1. Send an authenticated request to the third-party sandbox.<br>2. Verify the response status and payload structure. | Request succeeds (2xx). Response matches the documented schema for the endpoint. | pytest + requests | High |

### TC-002: Reject Invalid or Expired Credentials

Bad credentials are the first line of defense. This case verifies the app rejects them without leaking secrets.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-002 | Reject invalid, expired and revoked credentials | Test environment can use revoked tokens and invalid keys | Invalid API key, expired token, revoked OAuth token | 1. Send a request with an invalid API key.<br>2. Send a request with an expired token.<br>3. Send a request with a revoked OAuth token. | All requests return 401 or 403. Error bodies don't expose internal keys, tokens or stack traces. | pytest + requests | High |

### TC-003: Rate Limit Threshold Behavior

Most providers enforce a request limit. This case proves the app reads the headers and backs off instead of hammering the endpoint.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-003 | Verify rate limit threshold and headers | Rate limit is documented (e.g., 1,000 req/min) | Request volume that crosses the threshold | 1. Send requests up to the documented limit.<br>2. Send one additional request beyond the limit.<br>3. Inspect `Retry-After` and `X-RateLimit-Remaining` headers. | Requests within the limit succeed. The request over the limit returns 429. Headers are present and accurate. | k6 / Locust | High |

### TC-004: Timeout and Retry Logic

Slow responses are not errors, but they become errors if the app waits forever. This case checks timeout and retry behavior.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-004 | Handle slow responses and network timeouts | Mock server or proxy configured to delay responses | Timeout threshold (e.g., 5 seconds); retry policy (e.g., 3 retries with exponential backoff) | 1. Configure the mock to delay the response beyond the timeout.<br>2. Send the request.<br>3. Observe retry attempts and final application behavior. | Request times out after the configured threshold. Retries follow the backoff policy. The user sees a graceful error. | WireMock / toxiproxy + pytest | High |

### TC-005: Error Response Parsing

Providers return 5xx and malformed bodies. This case ensures the app parses them without crashing or exposing internal details.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-005 | Parse and propagate third-party error responses | Mock server or sandbox returns documented error codes | 400, 500, 503 and non-JSON responses | 1. Send requests that trigger each error code.<br>2. Verify that the application logs and surfaces the error correctly. | Application parses the provider error, doesn't crash, logs context and surfaces a user-friendly message. | pytest + requests | High |

### TC-006: Fallback on Service Unavailability

When the provider is down, the app must still work for the user. This case forces a 503 and validates fallback logic.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-006 | Activate fallback when the third-party service is down | Fallback logic is implemented for the feature | Blocked endpoint or WireMock returning 503 | 1. Block all traffic to the provider endpoint or force a 503.<br>2. Trigger a request that depends on the service.<br>3. Observe fallback behavior. | Fallback activates. Core functionality remains available. Non-critical features degrade gracefully. | WireMock + application logs | High |

### TC-007: Response Schema Validation

Provider responses change without warning. This case validates every field the app actually uses and ignores the rest safely.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-007 | Validate third-party response schema | JSON Schema or TypeScript types defined for the integration | Responses covering documented and undocumented variations | 1. Send requests covering all documented response shapes.<br>2. Validate each response against the schema.<br>3. Test handling of unknown fields. | All documented fields are present and correctly typed. Unknown fields are ignored or logged, not crash the parser. | jsonschema / Pydantic | High |

### TC-008: Webhook Delivery and Signature Validation

Webhooks are push, not pull. This case verifies delivery and rejects any payload with a bad signature.

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-008 | Verify webhook delivery and signature from provider | Webhook endpoint is registered with the provider sandbox | Valid and invalid webhook payloads and signatures | 1. Trigger an event in the provider sandbox.<br>2. Verify the webhook reaches the endpoint.<br>3. Validate the signature and payload structure. | Webhook is delivered within the documented SLA. Payload matches the schema. Invalid signatures are rejected. | Flask test client / ngrok for sandbox | High |

## Best Practices

1. Never test against production third-party APIs in CI. I always use mocks, sandboxes or recorded fixtures. Production endpoints can rate-limit the build and mutate real data.
2. Implement and test circuit breakers so repeated failures stop the cascade before they take down the app.
3. Log the full provider response body and headers when an error occurs. Without the raw response, debugging a provider issue is guesswork.
4. Pin to a specific provider API version and test upgrades in a dedicated environment. Silent version bumps are a common source of breaking changes.
5. Monitor response times and uptime against the provider's documented SLA. A 99.99% SLA still means minutes of downtime every month.
6. Validate the response schema on every integration test run to catch provider changes early.
7. Store API keys and tokens in environment variables, never in test code or repositories.

## Common Mistakes

1. Assuming the provider is always available. Even 99.99% uptime means downtime every month.
2. Testing only the happy path and ignoring 5xx, timeouts and malformed responses.
3. Hardcoding provider URLs instead of using configuration for sandbox vs production. I have seen staging accidentally point to production because of this.
4. Ignoring rate limit headers and triggering 429 errors or account suspension.
5. Skipping schema validation, which lets breaking provider changes reach production.
6. Running CI against live endpoints and hitting production rate limits or mutating data.

## Related Resources

- [REST API Testing Best Practices](/documentation/rest-api-testing-best-practices)
- [API Mocking with WireMock](/documentation/api-mocking-with-wiremock)
- [API Rate Limit Test Cases](/test-cases/api-rate-limit-test-cases)
- [API Error Handling Test Cases](/test-cases/api-error-handling-test-cases)
- [API Testing Checklist](/checklists/api-testing-checklist)

## Frequently Asked Questions

### Should I test against the real third-party API in CI?

No. Use the provider's sandbox, mocks with WireMock or recorded fixtures. Production endpoints can rate-limit your CI and mutate real data.

### How do I simulate provider downtime?

Use a mock server returning 503, a proxy like toxiproxy to drop or delay traffic, or firewall rules to block the endpoint in staging.

### What is the most common third-party API testing mistake?

Testing only the happy path. Providers fail with 5xx, slow responses and schema changes that your code must handle.

### How do I detect breaking changes in a provider schema?

Run contract or schema validation on every CI build. Compare the provider's OpenAPI spec or changelog with your integration schema and alert on diffs.
