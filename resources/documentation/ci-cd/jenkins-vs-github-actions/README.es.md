# Jenkins vs GitHub Actions: el mismo pipeline en ambas herramientas

Complemento de la guía de QAPractices [Jenkins vs GitHub Actions: Comparación CI/CD](https://qapractices.com/es/documentation/jenkins-vs-github-actions/).

La carpeta `same-pipeline/` implementa un único pipeline CI de Node.js dos veces — una como `Jenkinsfile` declarativo y otra como workflow de GitHub Actions — para comparar ambos DSL línea por línea.

## Estructura del proyecto

```text
same-pipeline/
├── Jenkinsfile
└── .github/
    └── workflows/
        └── ci.yml
```

## Mapeo de conceptos

| Jenkins | GitHub Actions | Notas |
|---------|----------------|-------|
| `pipeline { stages { stage } }` | `jobs.<id>.steps` | Jenkins agrupa en stages; Actions agrupa en jobs |
| `agent any` | `runs-on: ubuntu-latest` | Jenkins elige cualquier agent online; Actions elige un runner hosted o self-hosted |
| `environment { CI = 'true' }` | implícito (Actions exporta `CI=true`) | Los runners hosted ya exportan `CI=true` |
| `post { always { junit ... } }` | `if: always()` + `dorny/test-reporter` | Publicar resultados es un plugin en Jenkins, una action en Actions |
| `post { failure { archiveArtifacts } }` | `if: failure()` + `actions/upload-artifact` | Misma semántica, mecanismo distinto |
| `options { timestamps(); buildDiscarder }` | integrado en la UI de Actions | La retención se configura a nivel repo/org |
| credential store de Jenkins | `secrets.*` + environments / OIDC | OIDC elimina por completo las credenciales cloud de larga duración |

## Requisitos

- Un proyecto Node.js con scripts `npm run test:unit` y `npm run test:e2e`, Jest con el reporter `jest-junit` y una suite E2E (Playwright o equivalente) que escriba `playwright-report/`.
- Para el Jenkinsfile: un controller de Jenkins con un agent con Node.js 20 (o un agent `docker { image 'node:20-bookworm' }`) y el plugin JUnit.
- Para el workflow: nada extra — el runner hosted `ubuntu-latest` lo cubre.

## Uso

Copia el archivo de la herramienta que estés evaluando a un repo real y corre unos PRs contra él. La comparación se siente, no se lee: observa la espera en cola de los agents de Jenkins frente al spin-up de los runners de Actions antes de decidir.
