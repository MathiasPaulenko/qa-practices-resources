"""TOTP helpers for MFA tests (pyotp 2.12.1).

Test users in staging get a known base32 seed provisioned at setup time;
these helpers generate the same codes an authenticator app would.
"""

import time

import pyotp

# Test seed provisioned in staging, never a real user secret.
TEST_TOTP_SEED = "JBSWY3DPEHPK3PXP"


def current_totp(seed: str = TEST_TOTP_SEED) -> str:
    """Code valid for the current 30-second time step."""
    return pyotp.TOTP(seed).now()


def previous_totp(seed: str = TEST_TOTP_SEED) -> str:
    """Code from one time step back, for drift-window tests."""
    return pyotp.TOTP(seed).at(int(time.time()) - 30)


def next_totp(seed: str = TEST_TOTP_SEED) -> str:
    """Code for the upcoming time step, for boundary tests."""
    return pyotp.TOTP(seed).at(int(time.time()) + 30)


if __name__ == "__main__":
    print("current :", current_totp())
    print("previous:", previous_totp())
    print("next    :", next_totp())
