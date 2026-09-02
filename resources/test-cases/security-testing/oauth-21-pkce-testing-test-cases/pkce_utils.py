"""PKCE utilities for OAuth 2.1 test cases."""

import base64
import hashlib
import secrets
from dataclasses import dataclass


@dataclass
class PkcePair:
    """A PKCE verifier/challenge pair using S256."""

    verifier: str
    challenge: str
    method: str = "S256"
    skip_validation: bool = False

    def __post_init__(self):
        if self.skip_validation:
            return
        if not (43 <= len(self.verifier) <= 128):
            raise ValueError(
                f"code_verifier must be 43-128 chars, got {len(self.verifier)}"
            )


def generate_pkce_pair(length: int = 64) -> PkcePair:
    """Generate a PKCE pair with S256 challenge method.

    Args:
        length: Number of bytes for the verifier (before base64url encoding).
                64 bytes produces ~86 chars, well within the 43-128 range.

    Returns:
        PkcePair with verifier and S256 challenge.
    """
    verifier = secrets.token_urlsafe(length)[:128]
    challenge = (
        base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode("ascii")).digest()
        )
        .rstrip(b"=")
        .decode("ascii")
    )
    return PkcePair(verifier=verifier, challenge=challenge)


def generate_plain_challenge(value: str = "hello") -> PkcePair:
    """Generate a PKCE pair with plain method (for negative tests).

    OAuth 2.1 servers should reject this. Use in TC-03 to verify rejection.
    """
    return PkcePair(verifier=value, challenge=value, method="plain", skip_validation=True)
