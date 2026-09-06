# JWT Token Security Testing Checklist — Scripts Companion

Scripts companion para el [Checklist de Seguridad de Tokens JWT](https://qapractices.com/es/checklists/jwt-token-security-testing-checklist).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `scripts/generate-keys.sh` | Generar par de claves RSA para testing con openssl. |
| `scripts/test_jwt_validation.py` | Testear verificación de firma RS256 con PyJWT 2.10. |
| `scripts/test_algorithm_confusion.py` | Testear que `alg: none` y confusión RS256→HS256 sean rechazados. |
| `scripts/test_tampered_payload.py` | Testear que payloads modificados con firmas alteradas sean rechazados. |
| `scripts/test_claims_validation.py` | Testear validación de claims `exp`, `iss`, `aud`, `iat`. |

## Uso

```bash
# Generar par de claves RSA
bash scripts/generate-keys.sh

# Instalar dependencias
pip install PyJWT==2.10 cryptography==43.0

# Correr todos los tests
pytest scripts/ -v

# Correr un test individual
pytest scripts/test_algorithm_confusion.py -v
```

## Requisitos

- Python 3.10+
- PyJWT 2.10+
- cryptography 43.0+
- openssl (para generación de claves)
