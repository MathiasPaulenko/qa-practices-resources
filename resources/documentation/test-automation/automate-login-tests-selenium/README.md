# Automate Login Tests with Selenium

Runnable login test suite from the QAPractices guide [How to Automate Login Tests with Selenium](https://qapractices.com/documentation/automate-login-tests-selenium/).

The `login-tests/` folder contains a Maven/TestNG Page Object Model suite and a pytest equivalent with parametrized negative cases — the fixed, runnable versions of the snippets in the guide.

## Project structure

```text
login-tests/
├── pom.xml                          # selenium-java 4.21.0 + testng 7.10.2 + surefire
├── src/test/java/
│   ├── LoginPage.java               # Page Object: locators + login/error/dashboard methods with WebDriverWait
│   └── LoginTestPOM.java            # happy-path test + @DataProvider negative cases
└── python/
    ├── requirements.txt             # selenium 4.21.0 + pytest 8.2.0
    └── test_login.py                # pytest suite: xUnit hooks + @parametrize negative cases
```

## What it demonstrates

- `LoginPage.java` wraps locators in `PageFactory` and waits on the two things that actually break login tests: `urlContains("/dashboard")` after submit and `visibilityOf(errorMessage)` before reading its text.
- `LoginTestPOM.java` collapses four negative cases into one `@DataProvider` test — new cases are rows, not methods.
- `test_login.py` shows the correct pytest xUnit signatures (`setup_method(self, method)`) and the same wait strategy with `expected_conditions`.

## Usage

Requires Java 17+ / Python 3.10+ and Chrome installed. Selenium Manager (built into Selenium 4.6+) downloads the matching driver automatically — no `chromedriver` setup needed.

```bash
# Java — point driver.get(...) at your app's login page first
cd login-tests && mvn test

# Python
cd login-tests/python && pip install -r requirements.txt && pytest -v
```

The tests target placeholder locators (`#email`, `#password`, `#login-button`, `.error-message`, `#dashboard`). Adjust them to your application before expecting green results.
