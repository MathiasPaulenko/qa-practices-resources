# Seguimiento del Ciclo de Vida de Defectos — Archivos de workflow

Versiones machine-readable de la [Plantilla de Seguimiento del Ciclo de Vida de Defectos](https://qapractices.com/es/templates/defect-lifecycle-tracking-template/) de QAPractices. Úsalas para configurar tu tracker de issues en lugar de copiar tablas a mano.

## Archivos

| Archivo | Qué contiene |
|---|---|
| `jira-workflow.json` | Estados, categorías, transiciones, campos obligatorios por transición y las reglas de automatización (bloquear si falta el número de build, auto-cierre a las 48 h, aviso de SLA al 80%). Mapea los 12 estados de la plantilla a un workflow estilo JIRA. |
| `sla-targets.json` | SLA de resolución por severidad, acciones de escalación ante incumplimientos y umbrales de indicadores de calidad (tasa de reapertura, cumplimiento de SLA, tasa de escape...). |

## Cómo usar

1. Importa o reproduce `jira-workflow.json` en tu tracker: JIRA (Configuración → Issues → Workflows), Linear, Azure DevOps o YouTrack.
2. Configura los `required_fields` de cada transición — es lo que evita que un defecto llegue a verificación sin número de build ni pasos de reproducción.
3. Crea las reglas de `automation_rules` con el motor de automatización de tu tracker.
4. Carga `sla-targets.json` en tu capa de reporting o alertas; empieza con estos números y ajústalos según tus tiempos de ciclo medidos.

## English

The [English version](README.md) describes the same files.
