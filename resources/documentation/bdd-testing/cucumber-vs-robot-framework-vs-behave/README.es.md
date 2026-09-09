# Cucumber vs Robot Framework vs Behave — Ejemplo de Login

Recurso companion para [Cucumber vs Robot Framework vs Behave: comparación BDD 2026](https://qapractices.com/es/documentation/cucumber-vs-robot-framework-vs-behave/).

Tres suites BDD probando el mismo escenario de login por API:

- **Cucumber JVM 7.34.3** con REST Assured 5.5.0
- **Robot Framework 7.4.2** con RequestsLibrary 0.9.7
- **Behave 1.3.3** con requests 2.32.3

## Escenario

Un usuario con email `qa@qapractices.com` y password `ValidPass!2026` inicia sesión a través de una API local en `http://127.0.0.1:8080`, recibe un token y alcanza un dashboard que dice `Welcome to QA Practices`.

## Estructura

```text
cucumber-jvm/        # Proyecto Maven con Cucumber + REST Assured
robot-framework/     # Robot Framework con RequestsLibrary
behave/              # Behave con requests
.github/workflows/   # Workflow de CI que corre las tres suites
```

## Prerrequisitos

- Java 17+ (para Cucumber JVM)
- Python 3.12+ (para Robot Framework y Behave)
- Una API corriendo en `http://127.0.0.1:8080` con endpoints:
  - `POST /api/v1/test-users` — crear usuario de prueba
  - `POST /api/v1/auth/login` — login, devuelve token
  - `GET /api/v1/dashboard` — dashboard protegido

## Ejecutar Cucumber JVM

```bash
cd cucumber-jvm
mvn test -Dtest=RunCucumberTest
```

## Ejecutar Robot Framework

```bash
cd robot-framework
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
robot --variable BASE_URL:http://127.0.0.1:8080 tests/login.robot
```

## Ejecutar Behave

```bash
cd behave
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
behave features/login.feature
```

## CI

El workflow en `.github/workflows/bdd-comparison.yml` corre las tres suites en GitHub Actions.

## Versiones

| Herramienta | Versión |
| --- | --- |
| Cucumber JVM | 7.34.3 |
| REST Assured | 5.5.0 |
| JUnit Platform | 1.14.2 |
| Robot Framework | 7.4.2 |
| robotframework-requests | 0.9.7 |
| Behave | 1.3.3 |
| requests | 2.32.3 |
