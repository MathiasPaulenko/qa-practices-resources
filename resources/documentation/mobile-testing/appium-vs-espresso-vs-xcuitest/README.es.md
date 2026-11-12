# Companion de Appium vs Espresso vs XCUITest

Recurso companion de [Appium vs Espresso vs XCUITest: iOS y Android Nativos](https://qapractices.com/es/documentation/appium-vs-espresso-vs-xcuitest). El mismo escenario de login implementado una vez por framework para comparar sintaxis, configuración y modelo de ejecución lado a lado.

## Archivos

| Archivo | Framework | Modelo de ejecución |
|---------|-----------|---------------------|
| `AppiumLoginTest.java` | Appium 2.x + UiAutomator2, `appium-java-client` 9.x | Fuera del proceso, HTTP/WebDriver |
| `LoginEspressoTest.kt` | Espresso 3.5+ (AndroidX Test 1.5+) | Dentro del proceso, source set `androidTest` |
| `LoginUITest.swift` | XCUITest, Xcode 15+ | Proceso runner separado, APIs de accesibilidad |

## Inicio Rápido

```bash
# Appium (servidor + driver uiautomator2 instalados, app en dispositivo/emulador)
appium &                    # Appium Server 2.x escucha en :4723
javac AppiumLoginTest.java  # necesita appium-java-client 9.x en el classpath

# Espresso (dentro del source set androidTest de la app)
./gradlew connectedAndroidTest

# XCUITest (requiere macOS + Xcode)
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16'
```

## Requisitos

- Appium Server 2.x con el driver `uiautomator2` (`appium driver install uiautomator2`)
- `appium-java-client` 9.x para el ejemplo en Java
- Android SDK + emulador o dispositivo para Espresso
- macOS + Xcode 15+ para XCUITest

## Notas

- Reemplaza `com.example.app`, los selectores `R.id.*` y las claves `accessibilityIdentifier` por los identificadores reales de tu app. Los IDs de accesibilidad sobreviven a la localización y a los cambios de layout mejor que el texto o XPath.
- El mismo flujo de login tarda unos 2-5 s bajo Appium (round-trips HTTP) frente a menos de un segundo en Espresso (dentro del proceso) — la diferencia de velocidad que explica el artículo.
- `qa@staging.acme.dev` es un placeholder: usa una cuenta de pruebas dedicada en tu entorno de staging.
