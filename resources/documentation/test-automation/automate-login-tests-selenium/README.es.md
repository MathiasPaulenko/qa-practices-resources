# Automatizar pruebas de login con Selenium

Suite de tests de login ejecutable de la guía de QAPractices [Cómo Automatizar Pruebas de Login con Selenium](https://qapractices.com/es/documentation/automate-login-tests-selenium/).

La carpeta `login-tests/` contiene una suite Maven/TestNG con Page Object Model y un equivalente en pytest con casos negativos parametrizados — las versiones corregidas y ejecutables de los fragmentos de la guía.

## Estructura del proyecto

```text
login-tests/
├── pom.xml                          # selenium-java 4.21.0 + testng 7.10.2 + surefire
├── src/test/java/
│   ├── LoginPage.java               # Page Object: locators + métodos login/error/dashboard con WebDriverWait
│   └── LoginTestPOM.java            # test de camino feliz + casos negativos via @DataProvider
└── python/
    ├── requirements.txt             # selenium 4.21.0 + pytest 8.2.0
    └── test_login.py                # suite pytest: hooks xUnit + casos negativos con @parametrize
```

## Qué demuestra

- `LoginPage.java` encapsula los locators en `PageFactory` y espera las dos cosas que realmente rompen los tests de login: `urlContains("/dashboard")` tras el submit y `visibilityOf(errorMessage)` antes de leer su texto.
- `LoginTestPOM.java` colapsa cuatro casos negativos en un solo test con `@DataProvider` — los casos nuevos son filas, no métodos.
- `test_login.py` muestra las firmas correctas de los hooks xUnit de pytest (`setup_method(self, method)`) y la misma estrategia de waits con `expected_conditions`.

## Uso

Requiere Java 17+ / Python 3.10+ y Chrome instalado. Selenium Manager (incluido en Selenium 4.6+) descarga el driver correspondiente automáticamente — no hace falta configurar `chromedriver`.

```bash
# Java — primero apunta driver.get(...) a la página de login de tu app
cd login-tests && mvn test

# Python
cd login-tests/python && pip install -r requirements.txt && pytest -v
```

Los tests apuntan a locators de ejemplo (`#email`, `#password`, `#login-button`, `.error-message`, `#dashboard`). Ajústalos a tu aplicación antes de esperar resultados en verde.
