# Prompt IA: Plan de Pruebas JMeter — Companion

Archivos companion del recurso [Prompt IA: Plan de Pruebas JMeter](https://qapractices.com/es/prompts/ai-prompt-generate-jmeter-plan).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo para generar el test plan JMeter, listo para copiar en un LLM. |
| `example-input.txt` | Contexto realista de una API de checkout con modelo de carga, SLA y ajustes de JMeter. |
| `example-output.md` | Fragmento de salida realista: thread group, samplers, timers, assertions, listeners y la línea de ejecución non-GUI. |
| `users.csv` | Dataset CSV de ejemplo para el CSV Data Set Config (solo usuarios de prueba, sin credenciales reales). |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Reemplaza los placeholders entre corchetes con tu API real, modelo de carga, SLA y versión de JMeter.
3. Compara la respuesta con `example-output.md`; una buena salida nombra thread groups, correlación por sampler, assertions, estrategia de datos y la línea `jmeter -n -t`.
4. Construye el plan en el GUI de JMeter o un editor `.jmx` y corre un smoke de 10 usuarios y 2 minutos antes de la carga completa.
5. Ejecuta pruebas de carga solo contra staging o un entorno de performance dedicado. Nunca uses credenciales, tokens ni datos de clientes de producción.

## Requisitos

- Apache JMeter 5.6.3 (o la versión indicada en la salida del prompt).
- Un entorno de staging que tolere la carga planificada.
- Un dataset CSV dimensionado al número de hilos (ver `users.csv` para el formato).
