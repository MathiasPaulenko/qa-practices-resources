# Casos de Prueba de Verificación de Firmas Digitales — Companion

Materiales ejecutables para el recurso [Casos de Prueba de Verificación de Firmas Digitales](https://qapractices.com/es/test-cases/digital-signature-verification-test-cases/) de QAPractices.

## Contenido

| Archivo | Qué es |
|---|---|
| `openssl-verify.sh` | Comandos OpenSSL 3.x para la suite: generación de claves (RSA-2048, ECDSA P-256, Ed25519), firmar+verificar, el caso del byte manipulado, el caso de clave incorrecta, y recetas comentadas para validación de cadena, OCSP, firmas CMS detached y timestamps RFC 3161. |
| `tamper-detection-test.py` | Suite pytest (pytest ≥8.3 + `cryptography` ≥43) que cubre TC-011 detección de manipulación, TC-012 clave incorrecta, TC-015 firma corrupta, TC-016 documento vacío, TC-003 determinismo Ed25519 y TC-025 mismatch de curva. |

## Inicio rápido

```bash
# Flujo OpenSSL (requiere OpenSSL 3.x)
bash openssl-verify.sh

# Suite Python
pip install pytest "cryptography>=43"
pytest tamper-detection-test.py -v
```

## Notas

- Los ejemplos de API del recurso usan la plataforma ficticia SignVerify (`api.signverify.io/v1`) — trata las llamadas curl como contratos request/response para tu propio servicio, no como un endpoint real.
- TC-006, TC-013, TC-014 y TC-007 en el archivo shell están comentados porque necesitan una cadena de fixtures (root CA → intermedia → end-entity, CRL, token TSA). Generalos con `openssl req`/`openssl ca` o reusa los fixtures de tu laboratorio PKI.
