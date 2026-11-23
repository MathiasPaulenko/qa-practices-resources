# Casos de Prueba de Programa de Afiliados y Referidos — companion Playwright

Companion de [Casos de Prueba de Programa de Afiliados y Referidos](https://qapractices.com/es/test-cases/affiliate-referral-program-test-cases/).

- `fixture-referral.html` — simulación auto-contenida del flujo de referidos de TaskFlow: `?code=LUIS25` instala la cookie de tracking, el registro guarda `referred_by` y el paso de compra ejecuta la atribución más el control de fraude por autorreferencia. Carga vía `file://`, sin servidor.
- `referral-flow.spec.ts` — spec de Playwright 1.48 que cubre TC003/TC005/TC006 (atribución + recompensa acreditada), TC009 (autorreferencia bloqueada vía `luis.herrera+alias`) y el camino orgánico sin cookie.
- `referrals-api.http` — las dos llamadas curl del recurso (generar código, registrar conversión) más el caso 400 de un código por encima del límite de 32 caracteres. Necesita una API real de staging para ejecutarse.

## Ejecutar

```bash
npm install
npx playwright install chromium   # primera vez
npm test
```

Para ver el control de fraude fallar a propósito, quita el guard `selfReferral` del fixture — el segundo test demuestra que TC009 está detectando un bug real.
