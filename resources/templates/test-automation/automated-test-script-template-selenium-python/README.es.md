# Plantilla de Script Automatizado (Selenium + Python) — Companion

Companion ejecutable de la [Plantilla de Script Automatizado (Selenium + Python)](https://qapractices.com/es/templates/automated-test-script-template-selenium-python/) en QAPractices.

Esqueleto completo de suite Selenium 4 + pytest: page object model, fixtures de `conftest.py` con capturas en fallo, datos de prueba en JSON/YAML, ejecución paralela con pytest-xdist y workflow de GitHub Actions. Las pruebas de login corren contra [the-internet.herokuapp.com](https://the-internet.herokuapp.com), un sitio público de práctica para Selenium, así que la suite smoke pasa sin tocar nada.

## Estructura

- `pages/` — `BasePage` (esperas explícitas, acciones comunes) más `LoginPage`, `DashboardPage`, `CheckoutPage`
- `tests/` — `test_login.py` (smoke + regresión) y `test_checkout.py` (regresión)
- `utils/` — `TestDataLoader` (JSON/YAML) y `ScreenshotUtils`
- `data/` — `test_data.json` (usuarios, productos, URLs) y `credentials.yaml` (contraseñas; cámbialo por secretos de CI)
- `config/` — `browsers.yaml` con URLs por entorno y timeouts
- `conftest.py` — fixture `driver` (navegador + headless por flags CLI) y hook de captura en fallo
- `requirements.txt` — versiones fijadas: selenium 4.27.0, pytest 8.4.2, pytest-xdist 3.8.1, allure-pytest 2.15.0

## Uso

```bash
pip install -r requirements.txt

# suite smoke contra the-internet.herokuapp.com (Chrome headless por defecto)
pytest -m smoke

# ver el navegador en lugar de headless
pytest -m smoke --headless=no

# Firefox
pytest -m smoke --browser=firefox

# regresión completa en 4 workers
pytest -m regression -n 4
```

Selenium Manager descarga el driver correcto automáticamente: no hace falta `webdriver-manager`. Los reportes caen en `reports/html/` y las capturas de fallos en `reports/screenshots/`.

## Adaptación

Apunta `base_url` en `data/test_data.json` a tu app, cambia los localizadores de `LoginPage` por los tuyos y deja las contraseñas en `credentials.yaml` (añádelo al .gitignore en proyectos reales) o en los secretos de CI.
