# Casos de Prueba de Registro — Companion

Subconjunto ejecutable de los [Casos de Prueba de Registro](https://qapractices.com/es/test-cases/registration-test-cases/) — los que vale la pena automatizar primero.

## Archivos

| Archivo | Qué hace |
|---|---|
| `registration.spec.ts` | Spec de Playwright cubriendo TC-008 (signup válido), TC-013 (email duplicado), TC-014 (formato inválido), TC-010 (contraseña débil) y TC-012 (términos sin marcar). |
| `registration-data.json` | Fixture de datos de prueba: emails válido/duplicado/inválido más los payloads SQLi, XSS, unicode y tempmail usados en los bloques de seguridad y borde. |

## Ejecutar

```bash
BASE_URL=http://localhost:3000 npx playwright test registration.spec.ts
```

Apunta `BASE_URL` a staging — nunca producción. Ajusta los selectores al markup de tu formulario.

## Qué demuestra

- **La columna de herramienta es deliberada** — estos cinco son los casos que Playwright realmente cubre; las sondas de seguridad son de ZAP/Burp y los bordes de pytest parametrize.
- **Los errores deben ser genéricos** — la assertion de TC-013 es el mismo mensaje que vería un atacante durante enumeración (TC-022).
