# Casos de Prueba de Login — Companion

Archivos companion del recurso [Casos de Prueba de Login: Ejemplos Paso a Paso](https://qapractices.com/es/test-cases/login-test-cases).

## Archivos

| Archivo | Contenido |
|---|---|
| `login-test-cases.csv` | Los 20 casos de prueba como matriz importable (ID, sección, escenario, datos, resultado esperado, herramienta, prioridad) |
| `test-data.json` | Usuarios y payloads reutilizables: usuarios válido/bloqueado/inválido, entradas edge, payloads SQLi + XSS |

## Uso

- Importa `login-test-cases.csv` en TestRail, Xray o una planilla para seguir la suite; filtra por `section` para corridas focalizadas.
- Carga `test-data.json` desde Playwright, Postman o JMeter — los mismos datos alimentan tests de UI, API y carga.
- Mantén el pool de datos por entorno: los usuarios de staging no deben existir en producción.

Recurso en el sitio: [qapractices.com/es/test-cases/login-test-cases](https://qapractices.com/es/test-cases/login-test-cases)
