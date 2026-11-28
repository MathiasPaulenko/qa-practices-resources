# Prompt de IA: Escenarios de Test de Rate Limiting — Companion

Archivos companion del recurso [Prompt de IA: Escenarios de Test de Rate Limiting](https://qapractices.com/es/prompts/ai-prompt-rate-limiting-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de diseño de tests de rate limiting, listo para copiar en un LLM. |
| `example-input.txt` | Un contexto rellenado: PaymentAPI, token bucket, contador compartido en Redis, 3 tiers, conteo por API key. |
| `example-output.md` | Un fragmento de salida realista: escenarios de borde de burst y contador compartido, aritmética del borde para el límite dado, y un test de failover fail-closed. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Rellena el contexto del limiter — nombra tu algoritmo, tu clave de conteo y dónde vive el enforcement; omite lo que no aplique.
3. Decide fail-open o fail-closed *antes* de ejecutarlo — el prompt pide la expectativa, no un "depende".
4. Compara la respuesta con `example-output.md`; los escenarios de bypass deben corresponder a tu clave de conteo y la aritmética debe usar tus números reales.
5. Re-ejecuta tras upgrades de Redis, migraciones de gateway o cambios de reglas en el CDN.
