"""Executable subset of the multi-tenancy test cases.

Maps to the tenant-identification, isolation and edge-table cases from
qapractices.com/test-cases/multi-tenancy-test-cases/.
"""

import requests

from mock_server import fake_jwt


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


class TestTenantResolution:
    def test_jwt_claim_resolves_tenant(self, api_base, token_a):
        body = requests.get(f"{api_base}/api/me", headers=auth(token_a)).json()
        assert body["tenant"] == "acme"

    def test_missing_tenant_context_401(self, api_base):
        r = requests.get(f"{api_base}/api/me")
        assert r.status_code == 401

    def test_malformed_token_rejected(self, api_base):
        r = requests.get(f"{api_base}/api/me", headers={"Authorization": "Bearer not-a-jwt"})
        assert r.status_code == 401

    def test_header_claim_mismatch_rejected(self, api_base, token_a):
        r = requests.get(f"{api_base}/api/me", headers={**auth(token_a), "X-Tenant-ID": "globex"})
        assert r.status_code == 403

    def test_unknown_tenant_rejected(self, api_base):
        r = requests.get(f"{api_base}/api/me", headers=auth(fake_jwt("nosuchco")))
        assert r.status_code == 403

    def test_suspended_tenant_denied_mid_session(self, api_base):
        # lifecycle edge: a valid token for a suspended tenant must not work
        r = requests.get(f"{api_base}/api/me", headers=auth(fake_jwt("oldco", "u-9")))
        assert r.status_code == 403


class TestObjectIsolation:
    def test_own_order_visible(self, api_base, token_a):
        r = requests.get(f"{api_base}/api/orders/A-order-7781", headers=auth(token_a))
        assert r.status_code == 200
        assert r.json()["id"] == "A-order-7781"

    def test_idor_cross_tenant_uniform_403(self, api_base, token_b):
        # Tenant B requests Tenant A's order — must not 404-reveal existence
        r = requests.get(f"{api_base}/api/orders/A-order-7781", headers=auth(token_b))
        assert r.status_code == 403
        assert r.json() == {"error": "forbidden"}  # uniform body, no metadata

    def test_idor_unknown_id_same_response(self, api_base, token_b):
        # existence cannot be probed: unknown ID looks identical to foreign ID
        r = requests.get(f"{api_base}/api/orders/nope-0000", headers=auth(token_b))
        assert r.status_code == 403


class TestCacheNamespace:
    def test_unnamespaced_cache_key_is_exposed(self, api_base, token_a):
        # this test DOCUMENTS the intentional leak — it fails once fixed
        keys = requests.get(f"{api_base}/api/cache/keys", headers=auth(token_a)).json()["keys"]
        leaks = [k for k in keys if not k.startswith("acme:") and not k.startswith("globex:")]
        assert "user:42" in leaks  # unnamespaced — the bug the suite hunts


class TestConcurrency:
    def test_concurrent_requests_keep_tenant(self, api_base, token_a, token_b):
        import concurrent.futures
        tokens = [token_a, token_b] * 25
        with concurrent.futures.ThreadPoolExecutor(10) as ex:
            bodies = list(ex.map(
                lambda t: requests.get(f"{api_base}/api/me", headers=auth(t)).json(),
                tokens,
            ))
        assert all(b["tenant"] == ("acme" if i % 2 == 0 else "globex")
                   for i, b in enumerate(bodies))
