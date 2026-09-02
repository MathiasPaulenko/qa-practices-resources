# Testing de Widgets en Flutter — Companion

Recurso companion para [Testing de Widgets en Flutter: 4 Capas con Ejemplos Dart](https://qapractices.com/es/documentation/flutter-widget-testing-guide).

## Contenido

- `lib/utils/validators.dart` — Validador de email usado en ejemplos de unit tests
- `lib/widgets/login_button.dart` — Widget LoginButton usado en widget y golden tests
- `test/utils/validators_test.dart` — Ejemplo de unit test (Capa 1)
- `test/widgets/login_button_test.dart` — Ejemplo de widget test (Capa 2)
- `test/golden/login_button_golden_test.dart` — Ejemplo de golden file test (Capa 4)
- `integration_test/login_flow_test.dart` — Ejemplo de integration test (Capa 3)
- `test/helpers/mock_api_service.dart` — Helper de generación de mocks con Mockito
- `pubspec.yaml` — Dependencias con versiones pineadas

## Requisitos

- Flutter SDK 3.24.0+
- Dart 3.5.0+

## Uso

```bash
# Instalar dependencias
flutter pub get

# Correr unit y widget tests
flutter test

# Generar mocks
dart run build_runner build

# Correr integration tests (requiere emulador o dispositivo)
flutter test integration_test/

# Actualizar golden baselines
flutter test --update-goldens
```

## Versiones

- Flutter: 3.24.0
- Mockito: 5.4.4
- build_runner: 2.4.15
