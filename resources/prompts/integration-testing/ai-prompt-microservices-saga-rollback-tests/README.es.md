# Prompt de IA: Tests de Rollback de Saga en Microservicios — Companion

Archivos companion del recurso [Prompt de IA: Tests de Rollback de Saga en Microservicios](https://qapractices.com/es/prompts/ai-prompt-microservices-saga-rollback-tests).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de rollback de sagas, listo para copiar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: una saga de pedidos e-commerce de cuatro servicios con coreografía sobre Kafka, estado en Postgres e idempotency keys. |
| `example-output.csv` | Los casos generados como CSV importable: id, nombre, tipo de saga, servicios, escenario de fallo, precondiciones, resultado esperado, criterio pass/fail, severidad y tipo de test. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes estilo Copilot).
2. Reemplaza los placeholders entre corchetes con la topología de tu saga: tipo de saga, servicios, broker, framework de orquestación, persistencia de estado, idempotencia, timeouts, reintentos, DLQ, monitorización y contexto de negocio.
3. Ejecútalo por saga, no por sistema — una arquitectura completa devuelve cobertura genérica.
4. Compara la salida con `example-output.csv` para verificar el formato esperado.
5. Verifica cada caso generado contra comportamiento de broker real (reenvíos, particiones, caídas de consumidores) antes de añadirlo a una suite.

## Requisitos

- Cualquier LLM con espacio para el prompt más la descripción de tu saga.
- Opcional: un entorno de staging con Testcontainers o Toxiproxy para convertir los casos generados en tests ejecutables.
