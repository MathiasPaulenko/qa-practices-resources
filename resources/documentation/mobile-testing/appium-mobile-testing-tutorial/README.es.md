# Tutorial de Appium — Repo Companion

> Repositorio companion para el [Tutorial de Appium: iOS y Android](https://qapractices.com/es/documentation/appium-mobile-testing-tutorial) en QAPractices.com.

## Qué incluye

- **Ejemplos de tests en Java** para Appium 2 con iOS y Android
- **Archivos de capabilities** para emulador, dispositivo real y CI
- **Workflow de GitHub Actions** para CI/CD con emulador Android

## Stack

| Herramienta | Versión |
| --- | --- |
| Appium Server | 2.0.0 |
| Appium Java Client | 9.2.0 |
| Selenium Java | 4.21.0 |
| JUnit Jupiter | 5.10.2 |
| Java | 17+ |

## Estructura del proyecto

```text
appium-mobile-testing-tutorial/
├── pom.xml
├── .github/workflows/
│   └── appium-android-tests.yml
├── src/test/java/com/shop/qa/
│   ├── AndroidLoginTest.java
│   ├── GestureExamplesTest.java
│   ├── ExplicitWaitTest.java
│   └── IOSPredicateExampleTest.java
└── src/test/resources/capabilities/
    ├── android-emulator.json
    ├── android-real-device.json
    ├── ios-simulator.json
    └── ios-real-device.json
```

## Cómo correr los tests

### Requisitos previos

1. Instalar Appium Server 2: `npm install -g appium@2.0.0`
2. Instalar drivers: `appium driver install uiautomator2` y `appium driver install xcuitest`
3. Iniciar Appium: `appium`
4. Android Studio con un emulador corriendo (para tests Android)
5. Xcode con iOS Simulator (para tests iOS, solo macOS)

### Correr todos los tests

```bash
mvn test
```

### Correr una clase específica

```bash
mvn test -Dtest=AndroidLoginTest
mvn test -Dtest=GestureExamplesTest
mvn test -Dtest=ExplicitWaitTest
mvn test -Dtest=IOSPredicateExampleTest
```

## Archivos de capabilities

Los archivos están en `src/test/resources/capabilities/`. Reemplazá `/path/to/app.apk` y `/path/to/app.app` con los paths reales a tus builds.

| Archivo | Caso de uso |
| --- | --- |
| `android-emulator.json` | Emulador Android (Pixel 7, API 34) |
| `android-real-device.json` | Dispositivo Android físico (setear `udid`) |
| `ios-simulator.json` | iOS Simulator (iPhone 15, iOS 17.5) |
| `ios-real-device.json` | Dispositivo iOS físico (setear `udid` y signing) |

## CI/CD

El workflow de GitHub Actions en `.github/workflows/appium-android-tests.yml` corre tests Android en API levels 30 y 34 usando `reactivecircus/android-emulator-runner`.

## Recursos relacionados

- [Tutorial de Appium: iOS y Android](https://qapractices.com/es/documentation/appium-mobile-testing-tutorial)
- [Appium vs Espresso vs XCUITest](https://qapractices.com/es/documentation/appium-vs-espresso-vs-xcuitest)
- [Checklist de Mobile App Testing](https://qapractices.com/es/checklists/mobile-app-testing-checklist)
- [Plantilla de Script de Appium](https://qapractices.com/es/templates/appium-test-script-template)

## Licencia

MIT
