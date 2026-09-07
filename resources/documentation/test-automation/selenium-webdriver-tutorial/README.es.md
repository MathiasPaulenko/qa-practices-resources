# Tutorial de Selenium WebDriver: Código Companion

Código companion para el [Tutorial de Selenium WebDriver](https://qapractices.com/es/documentation/selenium-webdriver-tutorial).

## Requisitos

- Java 17+ o Node.js 18+ o Python 3.10+
- Chrome, Firefox o Edge instalado
- Selenium 4.48.0 (incluye Selenium Manager para descarga automática de drivers)

## Ejemplos

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

### Selenium Grid con Docker

```bash
cd scripts
docker-compose up -d
# Correr tests contra Grid en http://localhost:4444/wd/hub
docker-compose down
```

### CI/CD con GitHub Actions

El workflow en `.github/workflows/selenium-tests.yml` corre tests en Chrome y Firefox en paralelo en cada pull request.

## Recursos Relacionados

- [Tutorial de Selenium WebDriver](https://qapractices.com/es/documentation/selenium-webdriver-tutorial)
- [Guía Completa de Selenium WebDriver 4](https://qapractices.com/es/documentation/selenium-webdriver-4-complete-guide)
- [Mejores Prácticas de CI/CD Testing](https://qapractices.com/es/documentation/ci-cd-testing-best-practices)
- [Checklist de Selenium Grid](https://qapractices.com/es/checklists/selenium-grid-setup-checklist)
