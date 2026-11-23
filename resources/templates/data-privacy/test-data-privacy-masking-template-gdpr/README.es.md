# Plantilla de Enmascaramiento de Datos de Prueba (GDPR) — Companion

Archivos descargables de la [Plantilla de Enmascaramiento de Datos de Prueba](https://qapractices.com/es/templates/test-data-privacy-masking-template-gdpr/) de QAPractices.

## Contenido

| Archivo | Propósito |
|---|---|
| `test-data-privacy-masking-template.md` | Documento en blanco de 7 secciones: clasificación, técnicas, reglas por campo, pipeline, checklist de cumplimiento, tests de validación y aprobación. |
| `customers-masking-sample.md` | El documento rellenado para Northline Commerce: tabla `customers` (41.208 filas) enmascarada para el refresco de staging, todos los tests pasando. |
| `masking-validation.sql` | Puerta de validación PostgreSQL que cubre TD-001 a TD-007 — cada query debe devolver 0 antes de que la carga continúe. |

## Uso

1. Copia `test-data-privacy-masking-template.md` en los docs o la wiki de tu proyecto y rellena las secciones 1-4 antes de la primera exportación, nunca después.
2. Adapta las reglas por campo a tu esquema; ten en mente la integridad referencial de las claves compartidas entre tablas.
3. Integra `masking-validation.sql` en el pipeline como puerta dura: ejecútalo tras el enmascaramiento y aborta la carga ante cualquier cuenta distinta de cero.
4. Usa `customers-masking-sample.md` como referencia de cómo se documenta una ejecución de enmascaramiento bien hecha.

El SQL apunta a PostgreSQL; adapta los operadores regex (`~`, `!~`) para MySQL o SQL Server.
