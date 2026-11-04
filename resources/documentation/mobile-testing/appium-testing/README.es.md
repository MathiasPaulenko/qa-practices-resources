# Guía de Appium Testing — Companion

Este companion contiene archivos ejecutables para la guía [Appium: Automatización iOS y Android](https://qapractices.com/es/documentation/appium-testing).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `scripts/install-drivers.sh` | Instala los drivers XCUITest y UiAutomator2 de Appium 2.0 y corre `appium doctor` |
| `scripts/start-server.sh` | Inicia el servidor Appium y verifica `/wd/hub/status` |
| `tests/login-android.wdio.js` | Flujo de login en Android con WebdriverIO (localizadores accessibility-id) |
| `tests/login-android.py` | Flujo de login en Python con UiAutomator2Options |
| `tests/gestures.wdio.js` | Ejemplos de swipeGesture, pinchGesture, sendBiometricMatch y deepLink |

## Inicio rápido

```bash
# Requiere Node.js 18+, Android SDK (y Xcode en macOS para iOS)
npm install -g appium

bash scripts/install-drivers.sh
bash scripts/start-server.sh   # dejar corriendo y en otra terminal:

npx wdio run tests/login-android.wdio.js    # test de WebdriverIO
pip install Appium-Python-Client==4.2.0
python tests/login-android.py             # test de Python
```

## Integración CI

Ejecuta `install-drivers.sh` una vez por build de imagen de CI. Arranca el servidor en segundo plano antes del job de tests y corre el smoke de login en un emulador antes de despachar las suites del device farm.
