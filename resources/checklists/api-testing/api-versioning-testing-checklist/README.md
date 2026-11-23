# API Versioning Testing Checklist — Companion

Runnable scripts for the [API Versioning Testing Checklist](https://qapractices.com/checklists/api-versioning-testing-checklist/) on QAPractices.

## Scripts

### `scripts/verify-deprecation-headers.sh`

Hits a deprecated endpoint and asserts the three protocol-level signals actually reach the response: `Deprecation` (RFC 9745), `Sunset` with a valid HTTP-date (RFC 8594), and a `Link` header with `rel="successor-version"`. A body returning `200 OK` proves nothing — the retirement signal lives in the headers. Exits `0` if the endpoint already returns `410 Gone` (retirement is done, headers no longer expected).

```bash
./scripts/verify-deprecation-headers.sh https://api.acme.dev/v1/users/42
```

### `scripts/check-version-negotiation.sh`

Probes the negotiation surface: a valid version path, a request with no version, a non-existent version, a non-numeric version header, and conflicting URL-vs-header indicators. Any `500` fails immediately — invalid input must never crash the version router. Missing-version and conflict probes are reported, not enforced, because the right status depends on the documented default and precedence rule.

```bash
./scripts/check-version-negotiation.sh https://api.acme.dev v1 v99
```

## Requirements

- `bash`, `curl`

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Checks pass |
| 1 | Usage error or endpoint unreachable |
| 2 | Verification failed — missing/malformed headers or undocumented status |
