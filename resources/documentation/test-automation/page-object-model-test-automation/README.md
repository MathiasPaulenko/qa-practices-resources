# Page Object Model in Test Automation — Runnable Companion

Companion code for the [Page Object Model in Test Automation](https://qapractices.com/documentation/page-object-model-test-automation/) guide on QAPractices.com.

## Files

| File | Language | What it contains |
| --- | --- | --- |
| `java/BasePage.java` | Java | Abstract base page with shared wait/click/type helpers (Selenium 4.x). |
| `java/LoginPage.java` | Java | Page object for the login page using `@FindBy` + `PageFactory`. |
| `java/DashboardPage.java` | Java | Post-login page object; `logout()` returns a `LoginPage`. |
| `java/HeaderComponent.java` | Java | Component object for a shared header (search, cart). |
| `java/ProductPage.java` | Java | Page that composes the `HeaderComponent`. |
| `java/LoginTest.java` | Java | TestNG 7.x test using only page objects — no locators in the test. |
| `python/login_page.py` | Python | The same `LoginPage` with tuple locators (`selenium` 4.x). |

## Requirements

- Java 17+, Selenium Java 4.x, TestNG 7.x, ChromeDriver
- Or Python 3.10+, `selenium` 4.x, ChromeDriver

## Usage

Point `navigateTo()` / `navigate_to()` at your own staging login page (the `staging.qapractices.com` URL is a placeholder) and make sure the `email`, `password`, `login-button` and `.error-message` locators match your markup — or replace them with `data-testid` attributes if you control the front end.

```bash
# Java (with TestNG on the classpath)
mvn test -Dtest=LoginTest

# Python
python -c "from login_page import LoginPage; ..."
```

The guide: <https://qapractices.com/documentation/page-object-model-test-automation/>
