"""Validate a JWT token signature, expiration, audience and issuer.

Usage: python validate-jwt.py <token> <public-key.pem>
Requires: pip install PyJWT==2.9.0
"""
import sys
import jwt
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    DecodeError,
)

if len(sys.argv) < 3:
    print("Usage: python validate-jwt.py <token> <public-key.pem>")
    sys.exit(1)

token = sys.argv[1]
with open(sys.argv[2], "r", encoding="utf-8") as f:
    public_key = f.read()

try:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience="https://api.qa.local",
        issuer="https://auth.qa.local",
    )
    print("Token is valid")
    print(f"Claims: {decoded}")
    sys.exit(0)
except InvalidSignatureError:
    print("FAIL: signature validation failed")
    sys.exit(2)
except ExpiredSignatureError:
    print("FAIL: token expired")
    sys.exit(3)
except InvalidAudienceError:
    print("FAIL: audience mismatch")
    sys.exit(4)
except InvalidIssuerError:
    print("FAIL: issuer mismatch")
    sys.exit(5)
except DecodeError as e:
    print(f"FAIL: decode error: {e}")
    sys.exit(6)
