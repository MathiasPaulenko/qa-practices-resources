# Cheat Sheet de Comandos de Appium — Repo companion

> Repositorio companion del [Cheat Sheet de Comandos de Appium](https://qapractices.com/es/documentation/appium-commands-cheat-sheet) en QAPractices.com.

## Qué contiene

- **`AppiumCommandsExamples.java`** — una clase compilable que refleja cada sección de código del cheat sheet: configuración del driver, localizadores, gestos `mobile:`, W3C Actions, comandos de app/dispositivo y esperas.

## Stack

| Herramienta | Versión |
| --- | --- |
| Appium Server | 2.x |
| Appium Java Client | 9.2.0 |
| Selenium Java | 4.21.0 |
| Java | 17+ |

## Uso

La clase es una referencia, no una suite ejecutable — cada método corresponde a una sección del cheat sheet y asume una sesión activa contra un servidor Appium.

```bash
# Levantar el servidor (Appium 2.x escucha en "/", sin /wd/hub)
npm install -g appium
appium driver install uiautomator2
appium

# Compilar los ejemplos
mvn compile
```

Para ejecutar un snippet de verdad, apuntá las capabilities a tu app y emulador/dispositivo, y llamá al método que necesites desde un test JUnit.

## Notas sobre Appium 2.x

- La URL del servidor es `http://localhost:4723` — sin sufijo `/wd/hub`.
- `launchApp`, `closeApp`, `resetApp` se eliminaron en java-client 8+; usá `activateApp`/`terminateApp` y las capabilities `noReset`/`fullReset`.
- `swipeGesture` y `scrollGesture` de UiAutomator2 requieren el parámetro `direction`.
- El gesto de tap en coordenadas es `mobile: clickGesture` — `mobile: tap` no existe en UiAutomator2 (existe en XCUITest con otros parámetros).
