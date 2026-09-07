# Guía de XCUITest para iOS UI Testing — Companion

Archivos companion para la [Guía de XCUITest para iOS UI Testing](https://qapractices.com/es/documentation/xcuitest-guide-ios-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `tests/LoginPage.swift` | Page Object Model para la pantalla de login con accessibility identifiers. |
| `tests/LoginTests.swift` | Tests de login exitoso y fallido usando el Page Object Model. |
| `tests/QueryExamples.swift` | Ejemplos de queries de elementos: por identifier, texto, índice, children, firstMatch. |
| `.github/workflows/xcuitest-ios.yml` | Workflow de GitHub Actions para correr XCUITest en runners macOS. |

## Requisitos

- macOS con Xcode 15.4+
- iOS Simulator (iPhone 15 o iPhone SE 3rd generation)
- Swift 5.9+
- Un proyecto de iOS con accessibility identifiers seteados en los elementos de UI

## Uso

1. Copiá el directorio `tests/` a tu carpeta `MyAppUITests/`.
2. Actualizá los valores de `accessibilityIdentifier` para que coincidan con tu app.
3. Copiá el workflow de GitHub Actions a `.github/workflows/`.
4. Actualizá el comando `xcodebuild` con el nombre de tu proyecto y scheme.
5. Ejecutá `xcodebuild test -project MyApp.xcodeproj -scheme MyApp -destination "platform=iOS Simulator,name=iPhone 15"`.

## Integración de CI

El workflow corre XCUITest en dos simuladores (iPhone 15 y iPhone SE 3rd generation) en paralelo. Ajustá la matriz según tus necesidades.
