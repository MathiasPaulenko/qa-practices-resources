# Preguntas de Entrevista de Agile Testing — Companion

Artefactos ejecutables referenciados en la guía [Top 20 Preguntas de Entrevista de Agile Testing](https://qapractices.com/es/documentation/agile-testing-interview-questions/) de QAPractices.

## Archivos

| Archivo | Concepto que demuestra |
|---|---|
| `Jenkinsfile` | Pipeline de continuous testing: unit → integración → E2E smoke → staging → exploratorio (Q12) |
| `sprint_burndown.py` | Seguimiento de horas de QA contra tareas de dev dentro de un sprint (Q4) |
| `dod_check.yaml` | Gate de Definition of Done usable como chequeo de build (Q5) |
| `tdd_discount.py` | Ciclo red-green-refactor con un test estilo pytest ejecutable (Q7) |
| `login.feature` | Escenarios Gherkin en formato Given-When-Then (Q8) |

## Uso

- `python sprint_burndown.py` — imprime el progreso de QA del sprint.
- `python tdd_discount.py` — corre el ejemplo TDD completo.
- `Jenkinsfile` — úsalo en un job de pipeline de Jenkins; ajusta los npm scripts a tu proyecto.
- `login.feature` — corre con Behave 1.2+ (`behave login.feature`) cuando existan los step definitions.
- `dod_check.yaml` — parsea en CI y rompe el build ante cualquier entrada `false`.
