# Checklist Completo de Despliegue a Producción — Companion

Archivo companion del recurso [Checklist Completo de Despliegue a Producción](https://qapractices.com/es/checklists/production-deployment-testing-checklist).

Los 71 checks de despliegue vienen en un CSV importable para que un release manager los lleve a una planilla, una herramienta de gestión de tests o un ticket de runbook sin reescribir nada.

## Archivos

| Archivo | Contenido |
|---|---|
| `checklist-items.csv` | Los 71 ítems del checklist en 10 fases (Verificación Pre-Despliegue, Readiness de Infraestructura, Migraciones de Base de Datos, Gestión de Configuración, Health Checks, Rollback, Monitoring, Seguridad, Rendimiento, Smoke Tests) con nivel de riesgo por ítem |

## Uso

- Importa `checklist-items.csv` como tareas (Jira, TestRail, una planilla) y ordena por `area` — corre las fases en orden.
- Filtra por `risk` y trata cada `High` como gate duro: ningún ítem High sin marcar, ningún deploy.
- Escala la profundidad al radio de impacto: un release de solo configuración puede saltarse el load test, nunca la capacidad de rollback ni los smoke tests.

Recurso en el sitio: [qapractices.com/es/checklists/production-deployment-testing-checklist](https://qapractices.com/es/checklists/production-deployment-testing-checklist)
