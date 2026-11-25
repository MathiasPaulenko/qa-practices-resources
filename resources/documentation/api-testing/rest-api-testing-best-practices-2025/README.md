# REST API Testing Best Practices 2025 — Companion

Runnable `.http` collection covering the risk areas from the guide: authentication boundaries, pagination limits, rate-limit headers, idempotent retries, and schema validation.

## Usage

1. Copy `.env.example` values into a `.env` file (or your HTTP client's environment):

```
API_BASE_URL=https://staging.your-app.com/api
API_TOKEN=your-staging-token
```

2. Open `http/api-checks.http` with the VS Code REST Client extension, the JetBrains HTTP Client, or run it headless with `httpyac`.

3. Each request documents the expected status/assertion in its comment.

## Checks included

- Health check (200, response time)
- Unauthenticated request (401)
- Paginated request (200 + pagination fields)
- Oversized page rejection (400 / clamped)
- Role-based forbidden (403)
- Rate-limit headers and 429 + Retry-After
- Idempotent POST with `Idempotency-Key` (no duplicates on retry)
- Malformed body rejection (400)
- Structured error body (no HTML error pages)

Full guide: https://qapractices.com/documentation/rest-api-testing-best-practices-2025
