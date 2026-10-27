# Casos de Prueba de Apps Móviles — Archivos Complementarios

Assets para [Casos de Prueba de Apps Móviles: QA Práctico](https://qapractices.com/es/test-cases/mobile-app-test-cases/).

## Contenido

| Archivo | Propósito |
|---|---|
| `src/desired-caps.py` | Sets de capabilities de Appium-Python-Client 4.x para Android (UiAutomator2) e iOS (XCUITest), con la API moderna de `AppiumOptions` — sin `find_element_by_accessibility_id` deprecado. |
| `src/device-coverage-matrix.csv` | Matriz de cobertura dispositivo × OS para la suite: qué grupo de casos corre en cada tier (dispositivo real, emulador, device farm). |

## Uso

```bash
pip install Appium-Python-Client>=4.0
# Levantá el servidor Appium 2.x local, después:
python src/desired-caps.py
```

Actualizá `APP_PACKAGE` / `BUNDLE_ID` y `UDID` para tu app y dispositivo antes de correr.
