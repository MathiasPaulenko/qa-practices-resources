# Prompt IA: Pruebas de Interrupción Móvil — Companion

Archivos complementarios del recurso [Prompt IA: Pruebas de Interrupción Móvil](https://qapractices.com/es/prompts/ai-prompt-generate-interruption-tests).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | Prompt completo para generar pruebas de interrupción móvil, listo para copiar en un LLM. |
| `example-input.txt` | Contexto realista de checkout con versiones Android/iOS, autenticación, eventos interruptores, recuperación backend y restricciones de staging. |
| `example-output.md` | Fragmento de salida realista: matriz de interrupciones y casos detallados para llamadas, pérdida de red, muerte del proceso, bloqueo y notificaciones. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Reemplaza los placeholders entre corchetes con el contexto real de tu app, restricciones de ciclo de vida, contrato backend de recuperación y dispositivos disponibles.
3. Compara la respuesta con `example-output.md`; cada caso de alto riesgo debe incluir aserciones de recuperación, comprobaciones backend o de estado, limpieza y viabilidad de automatización.
4. Revisa manualmente los supuestos de plataforma antes de ejecutar. Android e iOS tienen comportamientos relacionados, no idénticos.
5. Ejecuta casos transaccionales solo en staging con fixtures controlados. Nunca uses números reales, tarjetas reales, cuentas de clientes ni tokens de producción.

## Requisitos

- Dispositivos físicos Android e iOS para los casos de interrupción de mayor riesgo.
- Backend de staging o servicio simulado seguro para comprobaciones transaccionales.
- Acceso a logs de ciclo de vida, logs de red, crash reporting e IDs de correlación backend cuando sea posible.
