# Configuración de pipeline CI/CD para automatización de pruebas

Configs de CI ejecutables de la guía de QAPractices [Cómo Configurar un Pipeline CI/CD para Automatización](https://qapractices.com/es/documentation/cicd-pipeline-test-automation-setup/).

La carpeta `pipeline-setup/` contiene las tres configuraciones de plataforma que la guía recorre, más una variante de E2E con shards y reportes de Playwright combinados.

## Estructura del proyecto

```text
pipeline-setup/
├── .github/
│   └── workflows/
│       ├── test-pipeline.yml   # unit → integration (servicio postgres) → E2E + publicación JUnit
│       └── e2e-sharded.yml     # sharding de Playwright en 4 runners + job de merge-reports
├── Jenkinsfile                 # pipeline declarativo: lint → unit → E2E, gate de cobertura, email en fallo
└── .gitlab-ci.yml              # stages lint/test/e2e/deploy con reportes JUnit + cobertura
```

## Qué demuestra

- `test-pipeline.yml` ordena los stages del más barato al más caro: unit tests con cobertura, luego tests de integración contra un contenedor de servicio `postgres:16`, y al final E2E de Playwright bloqueado detrás de `needs:`. Un job final con `dorny/test-reporter@v1` publica los resultados JUnit en el PR.
- `e2e-sharded.yml` corre `npx playwright test --shard=N/4` en cuatro runners y combina los reportes por shard con `npx playwright merge-reports`.
- `Jenkinsfile` es el equivalente declarativo: tool `nodejs 'Node20'`, post-acciones `junit` + `publishHTML`, artifacts de Playwright archivados y notificación por `emailext` vía `${env.QA_TEAM_EMAIL}`.
- `.gitlab-ci.yml` usa `artifacts:reports:junit` y `coverage_report` para que fallos y cobertura se vean en el widget del merge request; el job de E2E corre dentro de la imagen pinneada `mcr.microsoft.com/playwright:v1.45.0-jammy`.

## Uso

Copiá el archivo de tu plataforma al repo:

- GitHub: `.github/workflows/test-pipeline.yml` (y `e2e-sharded.yml` cuando la suite E2E pase de ~10 minutos)
- Jenkins: `Jenkinsfile` en la raíz del repo — requiere los plugins NodeJS, JUnit, HTML Publisher y Email Extension
- GitLab: `.gitlab-ci.yml` en la raíz del repo

Ajustá `npm test`, `npm run test:integration` y `npm run lint` a los scripts de tu proyecto. Todas las versiones están pinneadas — mantenelas así.

## Recurso relacionado

- EN: https://qapractices.com/documentation/cicd-pipeline-test-automation-setup/
- ES: https://qapractices.com/es/documentation/cicd-pipeline-test-automation-setup/
