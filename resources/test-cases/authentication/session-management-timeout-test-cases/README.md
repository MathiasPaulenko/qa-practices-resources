# Session Timeout Lab

Runnable companion for [Session Management Test Cases](https://qapractices.com/test-cases/session-management-timeout-test-cases/) — a stdlib-only Python session store that mirrors the TaskFlow rules from the suite: 30-minute idle timeout, 8-hour absolute limit, 15-minute access tokens, refresh token rotation and server-side invalidation on logout, password change and lockout.

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## What it covers

| Test | Suite case |
|---|---|
| `test_idle_timeout_expires_at_30_minutes` | TC-001 idle timeout |
| `test_activity_resets_idle_timer` | TC-002/TC-009 sliding expiration |
| `test_refresh_issues_new_access_token` | TC-003 token refresh |
| `test_remember_me_survives_browser_restart` | TC-004 remember me |
| `test_no_remember_me_dies_on_browser_restart` | TC-005 session cookie |
| `test_concurrent_sessions_same_user` | TC-006 concurrent sessions |
| `test_logout_invalidates_session` | TC-008 logout |
| `test_absolute_timeout_ignores_activity` | TC-010 absolute cap |
| `test_expired_access_token_rejected` | TC-012 expired token |
| `test_revoked_refresh_token_rejected` | TC-013 revoked refresh |
| `test_login_regenerates_session_id` | TC-014 fixation defense |
| `test_password_change_kills_all_sessions` | TC-022 password change |
| `test_single_flight_refresh_under_concurrency` | TC-028 refresh race |
| `test_lockout_kills_active_session` | TC-029 lockout |
| `test_session_cookie_flags` | TC-016/017/018 cookie flags |

## Notes

- `session_store.py` takes an injectable clock (`FakeClock` in the tests) so idle and absolute timeouts run in milliseconds instead of real minutes.
- The refresh path is single-flight: five threads racing one refresh token produce exactly one rotation and four revocations — the TC-028 stampede scenario.
- This is a logic-level lab, not a browser test. For the UI cases (TC-019/TC-020 warnings, TC-021 tabs, TC-030 mobile background) use Playwright 1.48+ against a real TaskFlow build.
