# Companion de Casos de Prueba de Validación de Formularios

Ejemplos ejecutables para el recurso [Casos de Prueba de Validación de Formularios](https://qapractices.com/es/test-cases/form-validation-test-cases/) en QAPractices. Corresponde a la sección Ejemplos de Automatización: un formulario HTML5 demo, un esquema Zod compartido entre cliente y servidor, y una suite Playwright que cubre validación en cliente, paridad con el servidor y spoofing de extensión en subidas.

## Contenido

| Archivo | Propósito |
|---|---|
| `demo-form.html` | Formulario de registro autocontenido con restricciones HTML5, wiring `aria-*` y verificación de magic bytes del PDF |
| `schema.js` | Esquema de registro en Zod 3.23 compartido por la validación de cliente y servidor |
| `form-validation.spec.ts` | Suite Playwright 1.49: campos requeridos, solo-espacios, limpieza de errores, paridad de esquema, rechazo de `.exe` renombrado |
| `fixtures/payload.exe` | Fixture ejecutable (cabecera `MZ` real) para el caso de extensión falseada TC-FV-080 |

## Ejecutar

```bash
npm install
npx playwright install chromium
npx serve . -l 4173   # servidor estático para demo-form.html
npm test
```

Las comprobaciones del esquema corren dentro de la suite de Playwright — no hace falta un runner aparte.

## Notas

- El formulario demo usa `novalidate` y comprobaciones en JS para poder rejugar las mismas reglas en servidor; en producción, alimenta ambas desde el esquema compartido.
- `fixtures/payload.exe` solo contiene la firma `MZ` seguida de relleno — es inerte, pero trátalo como entrada hostil por diseño.
