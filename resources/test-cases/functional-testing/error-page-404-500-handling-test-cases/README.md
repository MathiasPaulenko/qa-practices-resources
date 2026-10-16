# Error Page (404, 500) Handling Test Cases — Pytest Companion

Companion code for [Error Page (404, 500) Handling Test Cases](https://qapractices.com/test-cases/error-page-404-500-handling-test-cases/) on QAPractices.

## What is inside

| File | What it shows |
|------|---------------|
| `error_server.py` | Stdlib `http.server` mock serving custom 404/403/413/429/500/503 pages with correct status codes and headers: JSON 404 content negotiation, redirect chain ending at 404, a redirect loop, and two deliberately misconfigured routes (`/misconfigured/404` soft 404, `/misconfigured/500-debug` stack-trace + credential leak) for the negative cases. |
| `tests/test_error_pages.py` | 15 pytest cases covering TC002, TC004, TC007, TC010, TC016, TC017, TC023, TC025, TC026, TC029, TC031, TC032, TC033 plus the redirect-chain and server-header edge cases. |
| `tests/conftest.py` | Session-scoped server fixture on a free port and rate-limit reset. |
| `requirements.txt` | `pytest==8.3.4`, `requests==2.32.3`. |

## Run it

```bash
python -m venv .venv && .venv\Scripts\activate   # or source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

Expected: **15 passed**.

The suite talks to `error_server.py` over loopback — no external services needed. The `/misconfigured/*` routes exist to prove the defects exist; the tests that assert the bad behavior are documenting what TC016/TC017 would catch on a real site.

## Related resource

- [Error Page (404, 500) Handling Test Cases](https://qapractices.com/test-cases/error-page-404-500-handling-test-cases/) — the full 33-case suite plus the edge/boundary table this code automates.
