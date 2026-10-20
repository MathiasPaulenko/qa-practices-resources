# CORS Preflight Request Test Cases — Companion Lab

Companion for [CORS Preflight Request Test Cases: Headers, Methods](https://qapractices.com/test-cases/cors-preflight-request-test-cases/) on QAPractices.

A pure-stdlib Python module that models the checks a browser runs before a
cross-origin request: whether a request is "simple", exact origin matching
(scheme + host + port), method/header allow-lists, the credentials-vs-wildcard
spec violation, `null` origin rejection and `Max-Age` caching.

## Layout

```text
cors_preflight.py           — CorsConfig + evaluate_preflight + helpers
tests/test_cors_preflight.py — pytest cases mapped to TC-xxx on the site
requirements.txt            — pytest 8.3.4
pytest.ini                  — testpaths/pythonpath
```

## Run

```bash
pip install -r requirements.txt
pytest -q
```

## Coverage

Each test maps to a test case on the site (TC001–TC030): simple requests,
JSON/custom-header preflights, origin tuple matching (subdomain, scheme, port),
wildcard+credentials violation, `Origin: null`, Authorization allow-headers and
Max-Age caching.

The evaluator is deterministic and offline — it answers "would the browser let
this through?" given a `CorsConfig` and a request, so it doubles as a lint for
CORS policy changes.
