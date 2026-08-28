"""TC-011: Brute force protection on reset requests."""
import pytest
import time


class TestRateLimiting:
    """Tests for rate limiting on the reset request endpoint."""

    def test_tc011_rapid_requests_trigger_rate_limit(self, api_session, base_url, test_email):
        """TC-011: 6 rapid reset requests within 10 seconds return 429 on the 6th."""
        responses = []
        for i in range(6):
            response = api_session.post(
                f"{base_url}/auth/reset-request",
                json={"email": test_email},
            )
            responses.append(response)
            if i < 5:
                time.sleep(0.5)

        # The 6th request should be rate-limited
        assert responses[-1].status_code == 429, (
            f"Expected 429 on 6th request, got {responses[-1].status_code}. "
            f"Status codes: {[r.status_code for r in responses]}"
        )
