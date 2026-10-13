# Ejemplo de Pipeline de Testing en CI/CD

Snippets ejecutables de la guía de QAPractices [Pruebas en CI/CD: Mejores Prácticas y Gates](https://qapractices.com/es/documentation/ci-cd-testing-best-practices/).

La carpeta `pipeline-example/` conecta las seis etapas descritas en la guía en un solo workflow de GitHub Actions, más el quality gate de Jenkins, una factory de datos de prueba con faker y un gate de carga en k6.

## Estructura del proyecto

```text
pipeline-example/
├── .github/
│   └── workflows/
│       └── quality-gates.yml
├── Jenkinsfile
├── factories/
│   └── user.factory.ts
├── load-test.js
└── package.json
```

## Qué demuestra

- `.github/workflows/quality-gates.yml` corre las etapas de más barata a más cara: build+unitarios, luego integración (servicios postgres/redis con puertos mapeados) y seguridad (npm audit, Semgrep, trufflehog) en paralelo, después E2E, y una etapa de performance+contrato gateada a `main`.
- `Jenkinsfile` implementa el gate de cobertura bloqueante: parsea `coverage/lcov.info` y rompe el build por debajo de 80%.
- `factories/user.factory.ts` es la factory de `@faker-js/faker` v9 usada en la sección de datos de prueba.
- `load-test.js` es un script de k6 v0.52 cuyo bloque `thresholds` exige el mismo gate p95 < 500 ms que define la guía.
- `package.json` contiene el setup de pre-commit con `lint-staged` 15 + `husky` 9 y los scripts `test:*` que cada etapa invoca.

## Uso

Copiá las piezas que necesites a tu propio repo. El workflow asume que existen `npm run test:unit`, `test:integration`, `test:contract` y una suite de Cypress — ajustá los nombres de los scripts a tu proyecto.
