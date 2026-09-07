# Selenium WebDriver Tutorial: Companion Code

Companion code for the [Selenium WebDriver Tutorial](https://qapractices.com/documentation/selenium-webdriver-tutorial).

## Requirements

- Java 17+ or Node.js 18+ or Python 3.10+
- Chrome, Firefox or Edge installed
- Selenium 4.48.0 (includes Selenium Manager for automatic driver download)

## Examples

### Java

```bash
cd scripts/java
mvn test
mvn test -Dbrowser=firefox
```

### JavaScript

```bash
cd scripts/javascript
npm install selenium-webdriver
node login.test.js
BROWSER=firefox node login.test.js
```

### Python

```bash
cd scripts/python
pip install selenium pytest
pytest
BROWSER=firefox pytest
```

### Selenium Grid with Docker

```bash
cd scripts
docker-compose up -d
# Run tests against Grid at http://localhost:4444/wd/hub
docker-compose down
```

### CI/CD with GitHub Actions

The workflow in `.github/workflows/selenium-tests.yml` runs tests on Chrome and Firefox in parallel on every pull request.

## Related Resources

- [Selenium WebDriver Tutorial](https://qapractices.com/documentation/selenium-webdriver-tutorial)
- [Selenium WebDriver 4 Complete Guide](https://qapractices.com/documentation/selenium-webdriver-4-complete-guide)
- [CI/CD Testing Best Practices](https://qapractices.com/documentation/ci-cd-testing-best-practices)
- [Selenium Grid Setup Checklist](https://qapractices.com/checklists/selenium-grid-setup-checklist)
