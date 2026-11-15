# Ejemplos de Testing de Seguridad de Contraseñas

Snippets ejecutables usados en la guía de QAPractices:

- [Guía de Pruebas de Seguridad de Contraseñas](https://qapractices.com/es/documentation/password-security/)

Tres piezas, cada una correspondiente a una sección de la guía:

| Archivo | Qué prueba |
|---|---|
| `breach_check.py` | Consulta k-anonymity de Have I Been Pwned — rechaza contraseñas presentes en brechas sin enviar la contraseña a ningún lado |
| `password_policy.js` | Política estilo NIST 800-63B: longitud mínima 12 + blocklist, sin reglas de composición |
| `login_rate_limit.spec.ts` | Spec de Playwright: bloqueo tras 5 intentos fallidos + error genérico que no revela si la cuenta existe |

## Ejecutar

```bash
# Python 3.11+ — chequeo de brechas (llama a la API real de HIBP)
pip install -r requirements.txt
python breach_check.py "Correct-Horse-Battery-Staple!"

# Node 20+ — self-check de la política, sin dependencias
node password_policy.js

# Playwright — spec de rate limiting contra tu entorno de staging
npm install
npx playwright install chromium
BASE_URL=https://staging.example.dev npx playwright test
```

La spec de Playwright necesita una página de login real — apuntá `BASE_URL` a
staging y ajustá los selectores y el texto de bloqueo esperado a tu app.
