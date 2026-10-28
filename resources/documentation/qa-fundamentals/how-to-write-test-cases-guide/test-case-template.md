# Test Case Template

Reusable template from the guide — same fields as TC-EC-02-001.

```text
Test Case ID:
Title:
Scenario ID:
Requirement:
Priority: High / Medium / Low
Tags:

Preconditions:
- Account/environment (exact user, data state)
- Feature flags / configuration
- Starting state the tester can set up

Test Steps:
1. Ordered action, exact UI element and value
2. ...

Expected Result:
- Observable outcome the user can verify
- Backend state when it matters (field = value)

Actual Result: (fill during execution)
Status: (Pass / Fail / Blocked)
```

Rules of thumb:

- One test case, one intent — boundary and negative paths get their own IDs.
- Preconditions must be actionable: a named account and a points balance, not "database is clean".
- Every case links to a requirement ID so coverage reports are real.
