"""Minimal TOTP service for the 2FA test cases companion.

Implements RFC 6238 TOTP (HMAC-SHA-1, 30-second steps, 6 digits) plus
single-use enforcement, attempt limiting and backup codes — enough surface
to exercise the test cases from the QAPractices resource without external
services.
"""

import base64
import hashlib
import hmac
import secrets
import struct
import time


class TOTPService:
    STEP = 30
    DIGITS = 6
    MAX_ATTEMPTS = 5

    def __init__(self, drift=0):
        # `drift` is the server-side acceptance window in steps (RFC 6238 §6).
        self.drift = drift
        self._consumed = set()
        self._attempts = {}
        self._backup_codes = {}

    def generate_secret(self, account, issuer="QAPractices"):
        raw = secrets.token_bytes(20)
        return base64.b32encode(raw).decode().rstrip("=")

    def _hotp(self, secret, counter):
        padding = "=" * (-len(secret) % 8)
        key = base64.b32decode(secret + padding)
        msg = struct.pack(">Q", counter)
        digest = hmac.new(key, msg, hashlib.sha1).digest()
        offset = digest[-1] & 0x0F
        binary = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
        return str(binary % (10 ** self.DIGITS)).zfill(self.DIGITS)

    def current_code(self, secret, at=None):
        t = time.time() if at is None else at
        return self._hotp(secret, int(t // self.STEP))

    def verify(self, secret, code, account="user", at=None):
        """Verify `code` for `account`, enforcing single-use and the
        attempt limit. Returns True on success, False otherwise."""
        if self.is_locked(account):
            return False
        t = time.time() if at is None else at
        counter = int(t // self.STEP)
        ok = any(
            self._hotp(secret, counter - d) == code
            for d in range(-self.drift, self.drift + 1)
        )
        if ok and code in self._consumed:
            ok = False
        if ok:
            self._consumed.add(code)
            self._attempts.pop(account, None)
        else:
            self._attempts[account] = self._attempts.get(account, 0) + 1
        return ok

    def issue_backup_codes(self, account, count=10):
        codes = [secrets.token_hex(4) for _ in range(count)]
        self._backup_codes[account] = set(codes)
        return codes

    def verify_backup_code(self, account, code):
        codes = self._backup_codes.get(account)
        if codes and code in codes:
            codes.remove(code)
            return True
        return False

    def remaining_backup_codes(self, account):
        return len(self._backup_codes.get(account, ()))

    def is_locked(self, account):
        return self._attempts.get(account, 0) >= self.MAX_ATTEMPTS

    def reset_attempts(self, account):
        self._attempts.pop(account, None)
