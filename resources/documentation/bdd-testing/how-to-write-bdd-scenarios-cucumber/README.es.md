# Escritura de escenarios BDD con Cucumber — Ejemplos ejecutables

Recurso complementario de [Escenarios BDD con Cucumber: Ejemplos Gherkin](https://qapractices.com/es/documentation/how-to-write-bdd-scenarios-cucumber/).

Tres suites autocontenidas que cubren el mismo feature de login, para comparar el glue code:

- **Cucumber JVM 7.34.8** con JUnit Platform Suite
- **Behave 1.3.3** (Python)
- **@cucumber/cucumber 13.2.1** (JavaScript/Node)

Cada suite demuestra `Background`, `Scenario Outline` con `Examples`, un step con `Data Table`, filtrado por tags (`@smoke`, `@regression`, `@wip`) y hooks `@Before`/`@After`. Los step definitions delegan a un `LoginPage`/`AuthService` en memoria — sin navegador ni API externa: `mvn test` o `behave` funcionan directo.

## Escenario

Un usuario registrado inicia sesión con email y contraseña y llega al dashboard. El outline cubre credenciales válidas, contraseña incorrecta, usuario desconocido y email vacío.

## Estructura

```text
cucumber-jvm/    # Proyecto Maven, glue io.cucumber
behave/          # Proyecto Python, decorators de behave
js/              # Proyecto Node, @cucumber/cucumber
```

## Prerrequisitos

- Java 17+ y Maven (para cucumber-jvm)
- Python 3.10+ (para behave)
- Node 20+ (para js)

## Ejecutar Cucumber JVM

```bash
cd cucumber-jvm
mvn test
```

## Ejecutar Behave

```bash
cd behave
pip install -r requirements.txt
behave
behave --tags @smoke
```

## Ejecutar JavaScript

```bash
cd js
npm install
npx cucumber-js
npx cucumber-js --tags @smoke
```

## Reportes

- Java: `mvn test` genera `target/cucumber-reports.html`.
- JavaScript: `npx cucumber-js --format json:cucumber-report.json`, luego pásalo a `cucumber-html-reporter`.
- Behave: `behave -f json -o report.json` o `-f junit --junit-directory reports/` para CI.
