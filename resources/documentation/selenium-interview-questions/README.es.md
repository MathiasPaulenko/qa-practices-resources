# Companion de Preguntas de Entrevista de Selenium 4 Cartify

Esta carpeta contiene un proyecto **Java/TestNG/Selenium 4** ejecutable que replica la migración del checkout de Cartify desde la guía de QAPractices [50 Preguntas de Entrevista de Selenium: Cartify Selenium 4](https://qapractices.com/es/documentation/selenium-interview-questions/).

Es un proyecto pequeño `cartify-checkout` con clases Page Object Model, un retry analyzer, test data JSON, y un workflow de GitHub Actions que ejecuta la suite en Selenium Grid 4 con nodos Chrome y Firefox.

## Estructura del proyecto

```text
cartify-checkout/
├── .github/
│   └── workflows/
│       └── test.yml
├── pom.xml
└── src/test/
    ├── java/com/cartify/
    │   ├── pages/
    │   │   ├── BasePage.java
    │   │   ├── LoginPage.java
    │   │   ├── CartPage.java
    │   │   ├── CheckoutPage.java
    │   │   └── PaymentPage.java
    │   ├── utils/
    │   │   └── RetryAnalyzer.java
    │   └── tests/
    │       ├── LoginTest.java
    │       └── CheckoutTest.java
    └── resources/
        ├── test-data.json
        └── log4j2.xml
```

## Qué demuestra

- `BasePage.java` provee `waitForPageLoad()`, helpers de explicit wait, y captura de screenshots en fallos.
- `LoginPage.java`, `CartPage.java`, `CheckoutPage.java` y `PaymentPage.java` implementan el Page Object Model con selectores CSS `[data-testid]`.
- `RetryAnalyzer.java` implementa `IRetryAnalyzer` de TestNG con un máximo de 2 retries para tests flaky.
- `LoginTest.java` y `CheckoutTest.java` son clases de test TestNG con `@DataProvider` que lee desde `test-data.json`.
- `pom.xml` fija Selenium 4.21.0, TestNG 7.10, Java 21, Allure 2.29 y ChromeDriver 124.
- `.github/workflows/test.yml` ejecuta la suite en Selenium Grid 4 con nodos Chrome y Firefox via Docker Compose.
- `log4j2.xml` configura el logging para debugging.

## Prerrequisitos

- Java 21 (JDK)
- Maven 3.9+
- Docker (para Selenium Grid 4)

## Ejecutar localmente

```bash
cd cartify-checkout
mvn clean test
```

Output esperado:

```text
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

## Ejecutar en Selenium Grid 4

Levanta un nodo Chrome standalone:

```bash
# Levanta un nodo Chrome standalone en el puerto 4444 con Selenium 4.21.0
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.21.0
```

Ejecuta los tests contra el Grid:

```bash
mvn clean test -Dgrid.url=http://localhost:4444
```

## Ejecutar en GitHub Actions

El workflow en `.github/workflows/test.yml` levanta Selenium Grid 4 via Docker Compose, ejecuta la suite TestNG, y sube los reportes de Allure como artifacts.

## Versiones

| Dependencia | Versión |
|---|---|
| Selenium | 4.21.0 |
| TestNG | 7.10 |
| Java | 21 |
| Maven | 3.9 |
| Allure | 2.29 |
| ChromeDriver | 124 |

## Guía relacionada

- [50 Preguntas de Entrevista de Selenium: Cartify Selenium 4](https://qapractices.com/es/documentation/selenium-interview-questions/)
