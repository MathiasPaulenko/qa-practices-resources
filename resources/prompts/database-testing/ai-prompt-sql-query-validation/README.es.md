# Prompt de IA: Validación de Consultas SQL — Companion

Archivos companion del recurso [Prompt de IA: Validación de Consultas SQL](https://qapractices.com/es/prompts/ai-prompt-sql-query-validation).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de validación de queries, listo para copiar y pegar en cualquier LLM. |
| `example-input.sql` | Input de ejemplo: DDL de PostgreSQL 16.4 para `users`/`orders` más una query de reportes con defectos plantados (error de dialecto, binding inseguro, join implícito, trampa de NULL, predicados no sargables). |
| `expected-findings.md` | La tabla de hallazgos de referencia (F-01..F-08) y la query corregida — sirve para comprobar si el modelo ignoró el contexto. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los marcadores con la versión de tu motor, el DDL, los volúmenes de filas y el SLA.
3. Valida una query por ejecución — un script con varias sentencias recibe una revisión superficial de todas.
4. Compara la salida con `expected-findings.md`: una buena corrida detecta F-01 y F-02 primero.
5. Ejecuta la query corregida en una base de datos desechable antes de mergear nada.

## Requisitos

- Cualquier LLM con espacio para el prompt más tu DDL.
- Opcional: una base de datos desechable (Postgres en Docker, por ejemplo) para verificar el SQL corregido y correr `EXPLAIN (ANALYZE, BUFFERS)`.
