# Prompt de IA: Estrategia de Generación de Datos — Companion

Archivos companion del recurso [Prompt de IA: Estrategia de Generación de Datos](https://qapractices.com/es/prompts/ai-prompt-test-data-generation-strategy).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt de estrategia completo, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: un backend de e-commerce sobre PostgreSQL 16 con 2M de ítems. |
| `example-output.md` | Fragmento del plan de entidades generado para esa entrada (cinco entidades con volúmenes y restricciones). |

## Uso

1. Copiá `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplazá cada placeholder entre corchetes — almacenes, volúmenes, dominio, relaciones, formatos — con tus valores reales.
3. Corrélo y compará la forma de la salida con `example-output.md`; si un área de requisitos vuelve floja, pedile de nuevo ese ítem numerado.
4. Pegá tu schema real y el mapa de relaciones junto al prompt para que las entidades nombren tablas reales.
5. Mantené un random seed fijo en los entregables para que los datasets sean reproducibles.

## Requisitos

- Cualquier LLM que acepte un prompt de ~1.2k tokens (modelos clase GPT-4, Claude, Copilot Chat).
- Para ejecutar los scripts generados: Python con Faker (o JavaFaker / faker-js) y la base de datos destino.

## Notas

- La página del recurso también trae una variante táctica que entrega datasets listos para cargar en vez de una estrategia — usala cuando necesitás datos ya, no un plan.
- Nunca pegues datos de clientes reales ni connection strings de producción en el prompt.
