# Prompt de IA: Casos de Prueba de Base de Datos SQL — Companion

Archivos companion del recurso [Prompt de IA: Casos de Prueba de Base de Datos SQL](https://qapractices.com/es/prompts/ai-prompt-database-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de esquema-a-suite, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: una tabla `public.users` de PostgreSQL 16 con restricciones unique, índices B-tree y una estimación de 100 000 filas. |
| `example-output.csv` | Los casos de prueba generados como CSV importable: id, título, categoría, prioridad, SQL, resultado esperado y resultado SQL esperado. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los placeholders entre corchetes con tu versión del motor, DDL, índices y estimación de filas.
3. Ejecútalo sobre una tabla a la vez — pegar un esquema entero devuelve cobertura superficial.
4. Compara la salida con `example-output.csv` para validar el formato esperado.
5. Ejecuta cada consulta generada en una base desechable antes de sumar los casos a una suite.

## Requisitos

- Cualquier LLM con espacio para el prompt más el DDL de tu tabla.
- Opcional: una base de datos desechable (Postgres en Docker, por ejemplo) para verificar el SQL generado.
