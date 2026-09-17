# Mejores Prácticas de Appium — Companion

Companion ejecutable de la [guía de Mejores Prácticas de Appium](https://qapractices.com/es/documentation/appium-best-practices). Incluye una factoría de driver funcional, un ejemplo de page object, presets de capabilities y un job de GitHub Actions que corre los tests en un emulador Android.

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `capabilities/android-emulator.json` | Preset UiAutomator2 para un emulador Pixel 7 API 34 |
| `capabilities/ios-simulator.json` | Preset XCUITest para un simulador iPhone 15 |
| `pages/login_screen.py` | Page object: localizadores y métodos de intención en un solo lugar |
| `tests/conftest.py` | Factoría de driver + captura de screenshot/page-source en fallos |
| `tests/test_login_flow.py` | Dos tests de ejemplo usando el page object |
| `requirements.txt` | `Appium-Python-Client` 4.x, pytest 8.x, Selenium 4.x |
| `.github/workflows/appium-android.yml` | Job de CI: Appium 2 + UiAutomator2 + emulador Android |

## Requisitos

- Node.js 20+ y `appium@2` (`npm install -g appium@2`)
- Drivers de Appium: `appium driver install uiautomator2 xcuitest`
- Python 3.11+ con `pip install -r requirements.txt`
- Un emulador Android o simulador iOS con la app bajo prueba instalada,
  o un endpoint de device farm (BrowserStack, Sauce Labs) en `APPIUM_URL`

## Uso

```bash
# Levantar el servidor Appium
appium -p 4723

# Correr los tests de ejemplo contra un emulador Android
CAPS_FILE=capabilities/android-emulator.json pytest tests/ -v

# Simulador iOS
CAPS_FILE=capabilities/ios-simulator.json pytest tests/ -v
```

Ante un fallo, `tests/conftest.py` escribe `artifacts/{test}.png` y `artifacts/{test}-page.xml` para que cada test en rojo traiga su propia evidencia.
