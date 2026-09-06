# Guía de Testing OAuth — Scripts Companion

Scripts companion para la [Guía de Testing OAuth](https://qapractices.com/es/documentation/oauth-testing) en QAPractices.com.

## Scripts

| Script | Lenguaje | Qué hace |
| --- | --- | --- |
| `scripts/generate-pkce-pair.py` | Python 3.10+ | Genera un `code_verifier` y `code_challenge` PKCE (S256). Sin dependencias. |
| `scripts/token-exchange.sh` | Bash + curl | Intercambia un authorization code por tokens en el endpoint `/token`. |
| `scripts/validate-jwt.py` | Python 3.10+ | Valida firma, expiración, audience e issuer de un JWT con PyJWT 2.9.0. |
| `scripts/token-replay-test.py` | Python 3.10+ | Verifica que un access token revocado sea rechazado después de logout. Usa requests 2.31+. |

## Requisitos

- Python 3.10+
- `pip install PyJWT==2.9.0 requests==2.31.0`
- `curl` (cualquier versión)

## Uso

```bash
# 1. Generar par PKCE
python scripts/generate-pkce-pair.py

# 2. Intercambiar authorization code por tokens
./scripts/token-exchange.sh AUTH_CODE VERIFIER

# 3. Validar un JWT
python scripts/validate-jwt.py <token> <public-key.pem>

# 4. Testear replay de token después de logout
python scripts/token-replay-test.py https://api.qa.local <access-token>
```

## Referencias

- [OAuth 2.0 (RFC 6749)](https://datatracker.ietf.org/doc/html/rfc6749)
- [Proof Key for Code Exchange (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
