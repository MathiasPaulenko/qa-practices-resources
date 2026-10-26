"""Minimal 2FA login gateway for the test cases companion.

Models the API surface exercised by TC-015 (server-side bypass attempts)
and TC-016 (2FA enforcement for privileged roles): a password login that
never yields a full session while 2FA is pending, pre-auth tokens scoped
to the verification step only, codes bound to the account that requested
them, and authorization-level enforcement for admin roles. Pure stdlib;
responses mimic the HTTP status codes the resource expects.
"""

import secrets

from totp_service import TOTPService


class LoginGateway:
    def __init__(self, totp=None):
        self.totp = totp or TOTPService()
        self._users = {}
        self._pre_auth = {}
        self._sessions = {}

    def add_user(self, username, password, role="user", totp_secret=None):
        self._users[username] = {
            "password": password,
            "role": role,
            "totp_secret": totp_secret,
        }

    def login(self, username, password, **client_flags):
        """Password step. Client-supplied flags like `2fa_verified` or
        `skip_2fa` are accepted and ignored — the server never honors them."""
        user = self._users.get(username)
        if user is None or user["password"] != password:
            return {"status": 401, "error": "invalid_credentials"}
        if user["totp_secret"]:
            token = "pre_" + secrets.token_hex(8)
            self._pre_auth[token] = username
            return {"status": 200, "2fa_required": True, "pre_auth_token": token}
        token = self._issue_session(username)
        flags = set()
        if user["role"] == "admin":
            flags.add("2fa_enrollment_required")
        self._sessions[token]["flags"] = flags
        return {
            "status": 200,
            "2fa_required": False,
            "session_token": token,
            "flags": sorted(flags),
        }

    def verify_2fa(self, pre_auth_token, code):
        """Exchanges a pre-auth token plus a code for a full session. The
        code is checked against the token owner's secret — a code issued
        to a different account never validates."""
        username = self._pre_auth.get(pre_auth_token)
        if username is None:
            return {"status": 401, "error": "invalid_pre_auth_token"}
        secret = self._users[username]["totp_secret"]
        if not self.totp.verify(secret, code, account=username):
            return {"status": 401, "error": "invalid_code"}
        del self._pre_auth[pre_auth_token]
        token = self._issue_session(username)
        return {"status": 200, "session_token": token, "flags": []}

    def get_account(self, token):
        """Authenticated surface — pre-auth tokens are rejected."""
        session = self._sessions.get(token)
        if session is None:
            return {"status": 401, "error": "authentication_required"}
        return {"status": 200, "user": session["user"]}

    def admin_access(self, token):
        """Privileged surface — blocked while `2fa_enrollment_required`
        is flagged, and always blocked for non-admin roles."""
        session = self._sessions.get(token)
        if session is None:
            return {"status": 401, "error": "authentication_required"}
        if "2fa_enrollment_required" in session["flags"]:
            return {
                "status": 403,
                "error": "2fa_enrollment_required",
                "redirect": "/settings/security/2fa/enroll",
            }
        if session["role"] != "admin":
            return {"status": 403, "error": "forbidden"}
        return {"status": 200}

    def _issue_session(self, username):
        token = "sess_" + secrets.token_hex(8)
        self._sessions[token] = {
            "user": username,
            "role": self._users[username]["role"],
            "flags": set(),
        }
        return token
