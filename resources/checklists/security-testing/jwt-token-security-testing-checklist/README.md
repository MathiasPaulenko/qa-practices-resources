# JWT Token Security Testing Checklist — Companion Scripts

Companion scripts for the [JWT Token Security Checklist](https://qapractices.com/checklists/jwt-token-security-testing-checklist).

## Files

| File | Purpose |
| --- | --- |
| `scripts/generate-keys.sh` | Generate RSA key pair for testing with openssl. |
| `scripts/test_jwt_validation.py` | Test RS256 signature verification with PyJWT 2.10. |
| `scripts/test_algorithm_confusion.py` | Test that `alg: none` and RS256→HS256 confusion are rejected. |
| `scripts/test_tampered_payload.py` | Test that modified payloads with tampered signatures are rejected. |
| `scripts/test_claims_validation.py` | Test `exp`, `iss`, `aud`, `iat` claim validation. |

## Usage

```bash
# Generate RSA key pair
bash scripts/generate-keys.sh

# Install dependencies
pip install PyJWT==2.10 cryptography==43.0

# Run all tests
pytest scripts/ -v

# Run individual test
pytest scripts/test_algorithm_confusion.py -v
```

## Requirements

- Python 3.10+
- PyJWT 2.10+
- cryptography 43.0+
- openssl (for key generation)
