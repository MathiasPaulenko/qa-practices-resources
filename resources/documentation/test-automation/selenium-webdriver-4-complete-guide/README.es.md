# Selenium WebDriver 4 — Suite de tests ejecutable

Código companion de la guía [Selenium WebDriver 4: Novedades](https://qapractices.com/es/documentation/selenium-webdriver-4-complete-guide/).

Suite autocontenida que ejercita las técnicas centrales de la guía — Page Object Model, explicit waits, localizadores relativos, manejo de ventanas y alertas — contra un fixture HTML local (`app/login.html`). No necesita ningún sitio externo.

## Requisitos

- Python 3.10+ y Chrome instalado (Selenium Manager descarga ChromeDriver automáticamente)
- `pip install -r requirements.txt`

## Ejecutar

```bash
python -m pytest tests/ -v
```

El modo headless viene activado por defecto. Para ver el navegador correr:

```bash
SELENIUM_HEADLESS=false python -m pytest tests/ -v
```

## Qué cubre

| Archivo | Técnica |
|---|---|
| `tests/test_login_pom.py` | Page Object Model: página de login fluent, caminos de éxito y fallo |
| `tests/test_selenium4_features.py` | Localizador relativo (`above`), explicit wait sobre elemento diferido, invisibilidad del spinner, handle de pestaña nueva, aceptar alerta de confirmación |
