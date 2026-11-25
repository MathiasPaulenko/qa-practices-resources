# Page Object Model en Automatización de Pruebas — Companion Ejecutable

Código companion de la guía [Page Object Model en Automatización de Pruebas](https://qapractices.com/es/documentation/page-object-model-test-automation/) en QAPractices.com.

## Archivos

| Archivo | Lenguaje | Qué contiene |
| --- | --- | --- |
| `java/BasePage.java` | Java | Página base abstracta con helpers compartidos de wait/click/type (Selenium 4.x). |
| `java/LoginPage.java` | Java | Page object de la página de login con `@FindBy` + `PageFactory`. |
| `java/DashboardPage.java` | Java | Page object post-login; `logout()` devuelve una `LoginPage`. |
| `java/HeaderComponent.java` | Java | Component object para un header compartido (búsqueda, carrito). |
| `java/ProductPage.java` | Java | Página que compone el `HeaderComponent`. |
| `java/LoginTest.java` | Java | Test TestNG 7.x que solo usa page objects — sin locators en el test. |
| `python/login_page.py` | Python | La misma `LoginPage` con locators como tuplas (`selenium` 4.x). |

## Requisitos

- Java 17+, Selenium Java 4.x, TestNG 7.x, ChromeDriver
- O Python 3.10+, `selenium` 4.x, ChromeDriver

## Uso

Apunta `navigateTo()` / `navigate_to()` a tu propia página de login de staging (la URL `staging.qapractices.com` es un placeholder) y asegúrate de que los locators `email`, `password`, `login-button` y `.error-message` coincidan con tu markup — o reemplázalos por atributos `data-testid` si controlas el front end.

```bash
# Java (con TestNG en el classpath)
mvn test -Dtest=LoginTest

# Python
python -c "from login_page import LoginPage; ..."
```

La guía: <https://qapractices.com/es/documentation/page-object-model-test-automation/>
