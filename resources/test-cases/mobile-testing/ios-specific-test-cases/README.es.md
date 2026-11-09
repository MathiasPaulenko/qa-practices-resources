# Casos de Prueba Específicos de iOS — Archivos Companion

Assets para [Casos de Prueba Específicos de iOS: 30 Escenarios](https://qapractices.com/es/test-cases/ios-specific-test-cases/).

## Contenido

| Archivo | Propósito |
|---|---|
| `src/appium-ios-caps.py` | Capacidades `XCUITestOptions` de Appium 2.x para corridas en Simulador y dispositivo real, con una verificación de estado entre segundo y primer plano (TC-001). |
| `src/LifecycleTests.swift` | Specs de XCUITest para casos de ciclo de vida y permisos: preservación de estado (TC-001), interruption monitor para alertas de permiso (TC-005/006) y arranque por Universal Link (TC-026). |
| `src/apns-payloads.json` | Fixtures de payloads APNs para los casos de notificaciones: push con alerta, push silencioso (TC-004), decremento de badge (TC-011) y nivel de interrupción urgente (TC-012). |

## Uso

```bash
pip install "Appium-Python-Client>=4.0"
# Inicia el servidor Appium 2.x con el driver XCUITest instalado y luego:
python src/appium-ios-caps.py
```

Actualiza `BUNDLE_ID` y `UDID` para tu app y dispositivo antes de ejecutar. Para las specs de Swift, copia `LifecycleTests.swift` al target de UI tests de tu app en Xcode 15+.

Envía los fixtures de APNs a un dispositivo con `xcrun simctl push <device> <bundleId> <payload>.json` (Simulador) o vía una herramienta de push-testing como la CLI `pushtry` para dispositivos reales.
