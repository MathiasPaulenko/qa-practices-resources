# Website Pre-Launch Testing Checklist — Runnable Companion

Companion to [Website Pre-Launch Testing Checklist: Go-Live QA](https://qapractices.com/checklists/website-pre-launch-testing-checklist/) ([ES](https://qapractices.com/es/checklists/website-pre-launch-testing-checklist/)).

A zero-dependency Node 20+ checker that runs the checklist's SEO, security, and go-live items against a live URL.

## Contents

| File | Purpose |
|---|---|
| `pre-launch-check.mjs` | Fetches a URL and reports PASS/FAIL for: HTTP status, 5 security headers, `noindex` leaks (HTTP header + meta robots), title length, meta description length, self-referencing canonical, OG tags, and `robots.txt` blanket blocks |
| `tests/pre-launch-check.test.mjs` | `node:test` suite — 8 tests covering header checks, noindex leaks, canonical validation, and robots.txt rules |

## Run it

```bash
node pre-launch-check.mjs https://staging.example.com
```

Output is one line per check with a risk tag:

```text
PASS  [High] strict-transport-security — max-age=63072000; includeSubDomains
FAIL  [High] content-security-policy — missing
PASS  [High] meta robots noindex leak — index (ok)
...
staging.example.com: HIGH-RISK FAILURES — do not launch
```

Exit code is `0` only when every High-risk check passes — wire it into a release pipeline as a go/no-go gate. Medium and Low failures still print for the record.

## Run the tests

```bash
node --test tests/*.test.mjs
```

All 8 tests should pass. The checker functions (`checkHeaders`, `checkHtml`, `checkRobotsTxt`) are pure — no network in tests.

## Notes

- The `noindex` checks cover both vectors people forget: the `X-Robots-Tag` HTTP header and `<meta name="robots">` in the HTML.
- Missing data is never a pass — absent headers and tags fail explicitly, matching the checklist's rule.
