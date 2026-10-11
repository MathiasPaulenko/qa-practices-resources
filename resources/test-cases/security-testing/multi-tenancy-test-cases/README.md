# Multi-Tenancy Test Cases — Companion

Companion resource for [Multi-Tenancy Test Cases: Tenant Isolation & SaaS](https://qapractices.com/test-cases/multi-tenancy-test-cases/).

## Contents

- `mock_server.py` — stdlib-only multi-tenant API. Two tenants (`acme`, `globex`), fake base64 JWT with a `tenant` claim, `X-Tenant-ID` header resolution, RLS-style object scoping, a suspended-tenant flag, and a shared cache with one intentionally unnamespaced key.
- `tests/conftest.py` — starts the mock on an ephemeral port; `token_a` / `token_b` fixtures.
- `tests/test_tenant_isolation.py` — tenant resolution (claim, header, mismatch, malformed, unknown), IDOR with uniform-403 (no enumeration), the unnamespaced cache key hunt, and concurrent tenant-context swap.
- `requirements.txt` — pytest 8.3 + requests.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
cd resources/test-cases/security-testing/multi-tenancy-test-cases
pytest tests/ -v
```

Run the mock standalone for manual probes:

```bash
python mock_server.py 8571
curl -H "Authorization: Bearer $(python -c 'from mock_server import fake_jwt; print(fake_jwt("acme"))')" http://127.0.0.1:8571/api/me
curl -H "Authorization: Bearer $(python -c 'from mock_server import fake_jwt; print(fake_jwt("globex"))')" http://127.0.0.1:8571/api/orders/A-order-7781   # 403 — IDOR probe
curl http://127.0.0.1:8571/api/me                                                                                                                        # 401 — no tenant context
```

## What this covers

- Tenant resolution via JWT claim and `X-Tenant-ID` header; header/claim mismatch rejected.
- Cross-tenant object access (IDOR) with uniform 403 — IDs are not enumerable.
- Suspended tenants lose access mid-session (lifecycle edge).
- Cache namespace audit — an intentionally unnamespaced key to hunt.
- Concurrent requests alternating tokens — tenant context must not swap.
