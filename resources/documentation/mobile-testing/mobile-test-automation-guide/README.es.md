# Companion de la Guía de Automatización de Pruebas Móviles

Recurso companion de [Automatización de Pruebas Móviles: Guía Práctica](https://qapractices.com/es/documentation/mobile-test-automation-guide). Contiene un flow de Maestro ejecutable y un test de Appium que cubren el mismo escenario de login.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `login-flow.yaml` | Flow de Maestro: lanzar, ingresar credenciales, iniciar sesión, verificar el saludo de home |
| `test_login_appium.py` | El mismo flow como test de Appium en Python usando selectores accessibility-id |

## Inicio Rápido

```bash
# Maestro (necesita un emulador corriendo o dispositivo conectado)
maestro test login-flow.yaml

# Appium (necesita appium server + driver configurado en conftest)
python -m pytest test_login_appium.py -v
```

## Requisitos

- Maestro CLI 1.39+ para el flow YAML
- Appium 2.x con el driver UiAutomator2 para el test de Python
- Un build debug/release de la app a testear instalado en emulador o dispositivo

## Notas

- Reemplazá `com.example.app` y los accessibility IDs con los identificadores reales de tu app. Los accessibility IDs sobreviven mejor a cambios de localización y layout que los selectores por texto o XPath.
- Corré los tests contra un **build de release** — los builds de debug traen Metro y menús de desarrollo que cambian el timing.
- Agregá `clearAppState` (Maestro) o un hook de reset de estado (`beforeEach` en Appium) entre escenarios para que los tests no filtren historial de navegación.
