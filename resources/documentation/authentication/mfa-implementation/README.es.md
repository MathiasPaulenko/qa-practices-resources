# Guía de Pruebas de Implementación de MFA — Scripts complementarios

Scripts complementarios de la [Guía de Pruebas de Implementación de MFA](https://qapractices.com/es/documentation/mfa-implementation/) de QAPractices.com.

## Scripts

| Script | Lenguaje | Qué hace |
| --- | --- | --- |
| `scripts/totp-helpers.py` | Python 3.10+ | Genera códigos TOTP del paso actual, anterior y siguiente a partir de una semilla aprovisionada, con pyotp 2.12.1. |
| `scripts/lockout-probe.py` | Python 3.10+ | Bombardea el endpoint de verificación con códigos incorrectos y comprueba que el verificador limita o bloquea la cuenta. Usa requests 2.32.3. |
| `scripts/totp-login.spec.ts` | TypeScript | Spec de Playwright que completa el desafío OTP con un código generado por otplib 13.6, más la prueba de replay. |
| `scripts/webauthn-virtual-authenticator.spec.ts` | TypeScript | Spec de Playwright que registra un autenticador WebAuthn virtual vía Chrome DevTools Protocol y ejecuta una ceremonia de aserción. |

## Requisitos

- Python 3.10+
- `pip install pyotp==2.12.1 requests==2.32.3`
- Node 20+, `@playwright/test` 1.65.1, `otplib` 13.6.0

## Uso

```bash
# 1. Generar códigos TOTP para los fixtures
python scripts/totp-helpers.py

# 2. Probar el verificador contra bloqueo / límite de intentos
python scripts/lockout-probe.py

# 3. Ejecutar los specs de Playwright (solo staging, usuarios de prueba)
export TEST_TOTP_SEED=JBSWY3DPEHPK3PXP
export TEST_USER_PASSWORD=<contraseña-de-prueba>
npx playwright test scripts/totp-login.spec.ts
npx playwright test scripts/webauthn-virtual-authenticator.spec.ts
```

## Notas

- Todas las URLs apuntan a `staging.qapractices.com` como placeholder — reemplázalas por tu propio entorno de pruebas.
- Nunca ejecutes `lockout-probe.py` contra producción ni entornos compartidos; bloquea la cuenta de prueba a propósito.
- El spec de WebAuthn requiere Chromium (CDP `WebAuthn.addVirtualAuthenticator`); no funciona en Firefox ni Safari.
