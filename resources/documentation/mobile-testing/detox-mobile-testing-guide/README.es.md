# Companion de Testing con Detox para React Native

Setup E2E gray-box ejecutable con Detox v20 para la [Guía de Detox Mobile Testing](https://qapractices.com/es/documentation/detox-mobile-testing-guide/).

## Requisitos

- Node.js 18+
- Un proyecto React Native con carpetas iOS y/o Android
- Xcode + CocoaPods (iOS) o Android Studio con una imagen de emulador (Android)
- `detox-cli` instalado globalmente: `npm install -g detox-cli`

## Archivos

| Archivo | Descripción |
| --- | --- |
| `.detoxrc.js` | Configuración de Detox v20 para simulador iOS y emulador Android |
| `e2e/jest.config.js` | Setup del runner Jest para el suite E2E |
| `e2e/config.json` | Config del runner referenciada por `.detoxrc.js` |
| `e2e/login.test.js` | Suite de login: credenciales válidas, inválidas, matchers, actions y assertions |
| `e2e/pages/LoginPage.js` | Versión Page Object Model del mismo flujo |
| `.github/workflows/detox.yml` | Workflow de GitHub Actions que buildea y testea en runners macOS |

## Inicio rápido

```bash
# dentro de tu proyecto React Native
npm install --save-dev detox@^20 jest
cp -r e2e .detoxrc.js /ruta/a/tu-app/

# ajustá las rutas de .detoxrc.js al nombre y scheme de tu app
detox build -c ios
detox test -c ios
```

Reemplazá `MyApp` en `.detoxrc.js` por el nombre de tu workspace/scheme, y `Pixel_5_API_33` por un AVD que exista en tu máquina (`emulator -list-avds`).

## Notas

- Detox sincroniza con la app automáticamente — no hacen falta sleeps manuales.
- Los atributos `testID` deben existir en tus componentes de React Native para que los matchers `by.id()` los encuentren.
- El workflow de GitHub Actions necesita runners macOS para los builds de iOS.
