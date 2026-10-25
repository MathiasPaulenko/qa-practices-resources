# Plantilla de Informe de Auditoría de Accesibilidad — Companion

Archivos descargables de la [Plantilla de Informe de Auditoría de Accesibilidad](https://qapractices.com/es/templates/accessibility-audit-report-template/) en QAPractices.

## Contenido

| Archivo | Propósito |
|---|---|
| `accessibility-audit-report.md` | Informe de auditoría en blanco: encabezado, resumen ejecutivo, alcance, metodología, resumen y bloques de hallazgos, plan de remediación, firmas y registro de evidencias. |
| `accessibility-audit-report-sample.md` | El mismo informe completado de punta a punta tras una auditoría ficticia de WCAG 2.2 Nivel AA del portal de cotización de ClearPath Insurance — 1 hallazgo crítico, 2 mayores, 3 menores con un plan P0-P3. |

## Uso

1. Copia `accessibility-audit-report.md` en los docs o la wiki de tu proyecto.
2. Completa las Secciones 1-4 antes y durante la auditoría: alcance y metodología primero, nunca de memoria después.
3. Escribe un bloque de hallazgo por problema en la Sección 6 — agrupa instancias repetidas bajo un solo hallazgo con conteo de ocurrencias.
4. Completa el resumen de hallazgos (Sección 5) al final, para que los conteos coincidan exactamente con la Sección 6.
5. Usa `accessibility-audit-report-sample.md` como referencia de tono, nivel de detalle y decisiones de severidad.

La estructura del informe sigue WCAG-EM. Mapea cada hallazgo a un [criterio de conformidad WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) específico con su nivel.
