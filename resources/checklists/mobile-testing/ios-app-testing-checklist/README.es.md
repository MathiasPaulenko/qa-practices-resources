# Checklist de Testing de iOS — Companion

> Recurso companion de [Checklist de Testing de iOS](https://qapractices.com/es/checklists/ios-app-testing-checklist) en QAPractices.com.

Test de login con XCUITest y capabilities de Appium para iOS para la Checklist de Testing de iOS.

## Requisitos

- Xcode 15+ con XCTest y XCUITest
- Appium 2.x con el driver XCUITest
- Python 3.10+ (para scripts de Appium)
- iOS Simulator o un dispositivo físico iOS

## Setup

```bash
# XCUITest (Swift)
# 1. Abrir el .xcodeproj en Xcode
# 2. Seleccionar un simulator o dispositivo conectado
# 3. Correr el target LoginTests con Cmd+U

# Appium (Python)
pip install Appium-Python-Client
appium driver install xcuitest
appium --use-plugins=images
python appium/ios_login_test.py
```

## Archivos

| Archivo | Propósito |
| ------- | --------- |
| `tests/LoginTests.swift` | Test de login con XCUITest con credenciales válidas e inválidas |
| `appium/ios_login_test.py` | Test de login con Appium iOS usando driver XCUITest |
| `appium/capabilities.py` | Capabilities reutilizables de Appium para iOS |

## Licencia

MIT — libre de usar, modificar y distribuir. Nunca guardes credenciales de producción en config de test; siempre usá variables de entorno o cuentas sandbox.
