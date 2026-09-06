# OAuth Testing Guide — Companion Scripts

Companion scripts for the [OAuth Testing Guide](https://qapractices.com/documentation/oauth-testing) on QAPractices.com.

## Scripts

| Script | Language | What it does |
| --- | --- | --- |
| `scripts/generate-pkce-pair.py` | Python 3.10+ | Generate a PKCE `code_verifier` and `code_challenge` (S256). No dependencies. |
| `scripts/token-exchange.sh` | Bash + curl | Exchange an authorization code for tokens at the `/token` endpoint. |
| `scripts/validate-jwt.py` | Python 3.10+ | Validate a JWT signature, expiration, audience and issuer using PyJWT 2.9.0. |
| `scripts/token-replay-test.py` | Python 3.10+ | Test that a revoked access token is rejected after logout. Uses requests 2.31+. |

## Requirements

- Python 3.10+
- `pip install PyJWT==2.9.0 requests==2.31.0`
- `curl` (any version)

## Usage

```bash
# 1. Generate PKCE pair
python scripts/generate-pkce-pair.py

# 2. Exchange authorization code for tokens
./scripts/token-exchange.sh AUTH_CODE VERIFIER

# 3. Validate a JWT
python scripts/validate-jwt.py <token> <public-key.pem>

# 4. Test token replay after logout
python scripts/token-replay-test.py https://api.qa.local <access-token>
```

## References

- [OAuth 2.0 (RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749)
- [Proof Key for Code Exchange (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
