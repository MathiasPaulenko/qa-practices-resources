# Checklist de Onboarding QA — Companion Ejecutable

Artefactos pequeños usados durante la primera semana de la [Plantilla de Onboarding QA: Checklist 30-60-90](https://qapractices.com/es/templates/qa-onboarding-checklist-template/) en QAPractices.

## Contenido

| Archivo | Propósito |
|---|---|
| `env-check.sh` | Verifica que la máquina de la nueva incorporación tiene Node, Git, Python, Docker y los navegadores de Playwright. Falla en la primera herramienta rota (`set -e`) para que los problemas salgan antes del primer standup. |
| `first-ticket.yml` | Plantilla de issue form de GitHub para la primera tarea independiente de la incorporación. |

## Uso

```bash
bash env-check.sh
```

La salida esperada es similar a:

```text
== QA onboarding environment check ==
Node v20.11.0
Git 2.43.0
Python 3.11.x
Hello from Docker!
All checks passed.
```

Copia `first-ticket.yml` en `.github/ISSUE_TEMPLATE/` de tu repo para tener el formulario de tarea de onboarding listo.

Recurso origen: https://qapractices.com/es/templates/qa-onboarding-checklist-template/
