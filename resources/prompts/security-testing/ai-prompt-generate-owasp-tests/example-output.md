# Example output — OWASP Top 10 test cases

| ID | Category | Description | Input/payload | Steps | Expected | Evidence | Risk |
|---|---|---|---|---|---|---|---|
| OWASP-001 | A01 | IDOR on invoice fetch | `GET /api/invoices/1042` with user token for a user who owns invoice 2088 only | Send request, then increment the id | 403 or 404 — never the invoice body | Response contains another tenant's invoice data | High |
| OWASP-002 | A03 | SQLi in search param | `?q=%27%20OR%201%3D1--` on `GET /api/invoices` | Send the encoded value, then the same value URL-double-encoded | 400 with a field error; identical record count both times | 200 with the full invoice table or a DB error trace | High |
| OWASP-003 | A03 | Stored XSS in invoice notes | `<img src=x onerror=alert(1)>` in `notes` field | POST invoice, open it in the accountant role | Payload stored escaped; never executes | Script executes on render | High |
| OWASP-004 | A04 | No rate limit on login | 30 POST /api/login attempts, same account, 60 s | Run from a single test IP | Lockout or 429 well before attempt 30 | All 30 attempts processed | High |
| OWASP-005 | A05 | Missing security headers | `GET /` on the SPA | Inspect response headers | `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security` present | Any of them absent | Medium |
| OWASP-006 | A07 | JWT accepted after logout | Capture token, call `POST /api/logout`, replay token on `/api/users/me` | Replay within the 30-min session window | 401 after logout | 200 with user data | High |
| OWASP-007 | A10 | SSRF via logo URL import | `"logo_url": "http://169.254.169.254/latest/meta-data"` in `POST /api/invoices/branding` | Submit, then probe the fetch | 400 rejected; allowlist only http(s) public hosts | Server fetches the internal address | High |
| OWASP-008 | A02 | Sensitive data in error body | Trigger a 500 on `POST /api/invoices` with malformed JSON | Inspect the error response | Generic error id, no internals | Stack trace, SQL or env values leaked | Medium |

Gap note: A06 and A08 produced no rows — A06 belongs to dependency
scanning (run `npm audit`/Trivy, not payload tests) and A08 needs
CI/CD context the app spec didn't provide. That's a scope note,
not a coverage hole.
