# Prompt de IA: Generar un Script de Pruebas de Rendimiento con k6

Archivos companion del prompt de QAPractices
[Generar un Script de Pruebas de Rendimiento con k6](https://qapractices.com/es/prompts/ai-prompt-k6-performance-test-script/)
([English version](https://qapractices.com/prompts/ai-prompt-k6-performance-test-script/)).

## Contenido

| Archivo | Propósito |
|---|---|
| `prompt.md` | El prompt, listo para pegar en ChatGPT, Claude o cualquier LLM. |
| `example-input.txt` | Un bloque de variables rellenado (servicio de checkout) que puedes adaptar. |
| `load-test.js` | Salida de ejemplo: prueba de carga por etapas con `ramping-vus`, `setup()` OAuth2, datos con `SharedArray`, métricas custom y umbrales de SLA. |
| `spike-test.js` | Variante de pico: rampa rápida a VUs máximos, hold corto, bajada y ventana de recuperación. |
| `users.json` | Datos de prueba de ejemplo que leen los scripts vía `SharedArray`. |

## Uso

1. Copia `prompt.md` en tu LLM y reemplaza los placeholders entre corchetes — `example-input.txt` muestra un relleno realista.
2. O corre los scripts generados directamente con k6 1.x:

```bash
export BASE_URL=https://api-staging.example.com
export CLIENT_ID=your-client-id
export CLIENT_SECRET=your-client-secret

k6 run load-test.js
k6 run spike-test.js
```

Los scripts esperan `users.json` en la misma carpeta y autenticación OAuth2 client-credentials; cambia `setup()` por un token estático o API key si tu servicio usa otro método.

## Requisitos

- k6 1.x (`k6 version`)
- Un `BASE_URL` accesible que implemente `POST /oauth/token`, `GET /products`, `POST /cart`, `POST /checkout`
