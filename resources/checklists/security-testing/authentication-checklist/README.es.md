# Checklist de Testing de Autenticación — Companion

Este companion provee archivos ejecutables para el checklist [Checklist de Pruebas de Autenticación](https://qapractices.com/es/checklists/authentication-checklist).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `src/brute-force-lockout-test.ts` | Test de Playwright para bloqueo de cuenta tras intentos fallidos |
| `src/security-header-validation.py` | Script en Python para validar headers de seguridad en el endpoint de login |
| `src/jwt-expiration-test.py` | Script en Python para testear expiración y validación de tokens JWT |

## Inicio Rápido

```bash
# Instalar Playwright
npm init -y && npm install @playwright/test

# Correr el test de bloqueo por fuerza bruta
npx playwright test src/brute-force-lockout-test.ts

# Correr la validación de headers de seguridad
pip install requests
python src/security-header-validation.py

# Correr el test de expiración de JWT
pip install pyjwt
python src/jwt-expiration-test.py
```