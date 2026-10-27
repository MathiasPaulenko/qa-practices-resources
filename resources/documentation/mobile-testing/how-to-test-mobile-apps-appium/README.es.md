# Apps Móviles con Appium — companion pytest

Companion de [Apps Móviles con Appium: Primeras Pruebas](https://qapractices.com/es/documentation/how-to-test-mobile-apps-appium/).

- `tests/conftest.py` — fixture de sesión UiAutomator2; salta hasta setear `CAPABILITIES["appium:app"]`.
- `tests/test_first_appium_test.py` — las tres estrategias de selectores del Paso 4 (accessibility id, resource-id, XPath) más el patrón de waits explícitos (sin `Thread.sleep`).
- `.github/workflows/appium-ci.yml` — el job del emulador del Paso 10.
- `requirements.txt` — `appium-python-client 4.2` + `pytest 8.3`.

## Ejecutar

```bash
pip install -r requirements.txt
# Editá CAPABILITIES["appium:app"] en tests/conftest.py, después:
appium --port 4723 &
pytest tests/ -v
```
