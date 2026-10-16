# Alineación de Testing ISO 9001 — Archivos Complementarios

Artefactos complementarios de la guía [Guía de Alineación ISO 9001: Calidad y Testing](https://qapractices.com/es/documentation/iso-9001-quality-management-testing-alignment/).

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `traceability-matrix-template.csv` | Matriz requisitos → casos de test → defectos con filas de ejemplo, incluida una fila "gap" sin completar que muestra cómo se ve un hallazgo de auditoría |
| `iso-9001-clause-mapping.csv` | Hoja de trabajo cláusula por cláusula (cláusulas 4-10) mapeando requisitos ISO a artefactos y evidencias de QA |
| `audit-evidence-checklist.md` / `.es.md` | Checklist de evidencia pre-auditoría — cada ítem debería poder producirse en menos de 15 minutos |

## Cómo usarlo

1. Copia `iso-9001-clause-mapping.csv` y rellena la columna `owner` — una persona nombrada por cláusula, no "el equipo".
2. Usa `traceability-matrix-template.csv` como forma para tu RTM real; la columna `linked_defects` es lo primero que revisan los auditores.
3. Corre `audit-evidence-checklist.md` 4-6 semanas antes de la auditoría, no la semana anterior — las brechas tardan en cerrarse.

Son plantillas, no cumplimiento llave en mano. Adapta nombres de artefactos e IDs a tu tracker (Jira, Azure DevOps, TestRail, lo que uses).
