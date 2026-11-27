# Prompt IA: Generar Consultas GraphQL de Prueba — Companion

Archivos companion del recurso [Prompt IA: Generar Consultas GraphQL de Prueba](https://qapractices.com/es/prompts/ai-prompt-generate-graphql-queries).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | Prompt completo de generación de consultas GraphQL de prueba, listo para copiar en un LLM. |
| `example-input.txt` | Fragmento SDL de gestión de pedidos con contexto de endpoint, autorización, paginación y fixtures. |
| `example-output.md` | Fragmento realista de salida: fragment reutilizable, query y mutation con nombre, matriz de cobertura y notas. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Sustituye los placeholders entre corchetes por tu SDL real, endpoint, modelo de autorización, reglas de ejecución y restricciones de fixtures.
3. Compara la forma de la respuesta con `example-output.md`; si falta una cobertura, vuelve a pedir esa sección numerada.
4. Valida cada operación generada contra tu schema real antes de ejecutarla. Trata el GraphQL generado como código no confiable.
5. Ejecuta mutaciones solo contra fixtures controlados de staging y revisa antes los pasos de limpieza o rollback.

## Requisitos

- Un cliente GraphQL, IDE o paso de validación en CI que entienda el schema.
- Fixtures de staging para cualquier mutación o prueba de campos sensibles.
- Nada de datos reales de clientes, pagos o producción en prompts ni variables.
