# Example output fragment — POST /api/users negative cases

```text
| ID | Category | Description | Input | Expected behavior | Status | Risk | Reason |
|----|----------|-------------|-------|-------------------|--------|------|--------|
| NT-001 | Invalid | email empty string | email:"" , pw:"Passw0rd!" | error code EMAIL_REQUIRED | 400 | High | contract field |
| NT-002 | Boundary | password min-1 | pw:"Ab1!xyz" (7 chars) | error PASSWORD_TOO_SHORT | 400 | High | policy boundary |
| NT-003 | Invalid | SQL-shaped email | email:"'; DROP TABLE users;--" | rejected as invalid email; no query executed | 400 | High | injection probe |
| NT-004 | Invalid | XSS-shaped name | name:"<script>alert(1)</script>" | stored escaped or rejected | 400/201 | High | stored-XSS probe |
| NT-005 | Boundary | email max+1 | 255-char email | error EMAIL_TOO_LONG | 400 | Medium | declared max 254 |
| NT-006 | Malformed | non-JSON body | body:"not json", CT: app/json | error INVALID_BODY | 400 | Medium | parser contract |
| NT-007 | Malformed | duplicated field | {"email":"a","email":"b"} | last-wins or reject — spec silent | 400 | Medium | ambiguous contract |
| NT-008 | Auth | no token when admin-only | no Authorization header | unauthorized | 401 | High | spec ambiguous: JWT optional — flag |
| NT-009 | Auth | rate limit | 101st POST in the window | throttled | 429 | Medium | declared limit |
| NT-010 | Concurrency | duplicate email | two POSTs, same email, parallel | one 201, one 409 | 201/409 | High | unique-constraint race |
| NT-011 | Concurrency | register during user delete | POST while DELETE pending | deterministic outcome | 4xx | Medium | state race |
| NT-012 | Boundary | name at limit+emoji | 100 chars + "🧪" | counted as 101 units or accepted | 400/201 | Low | encoding ambiguity |
```
