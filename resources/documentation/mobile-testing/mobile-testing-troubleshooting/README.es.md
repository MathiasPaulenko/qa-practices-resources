# Troubleshooting de Mobile Testing — Repo Companion

> Repositorio companion de la [Guía de Troubleshooting de Mobile Testing](https://qapractices.com/es/documentation/mobile-testing-troubleshooting) en QAPractices.com.

## Qué incluye

- **`check-emulator-acceleration.sh`** — verificación del estado de HAXM en Windows y de la aceleración por hardware del emulador Android (Problema 1).
- **`locator-strategies.js`** — XPath frágil vs accessibility ID estable, más un patrón `waitUntil` para elementos de renderizado lento (Problema 2).
- **`os-version-permissions.js`** — bifurcación por capabilities para los permisos granulares de Android 13+ frente al flujo de permisos legacy (Problema 3).
- **`network-throttling.js`** — perfiles de red de BrowserStack (`2g`/`3g`/`4g`/`offline`/`intermittent`) aplicados antes de disparar acciones de sincronización (Problema 4).
- **`browserstack.yml`** — ejemplo de matriz de dispositivos en la nube: dispositivo real vs emulador con APKs por arquitectura (Problema 5).

## Stack

| Herramienta | Versión |
| --- | --- |
| Appium Server | 2.x |
| WebdriverIO | 8.x |
| Node.js | 20 LTS |
| BrowserStack App Automate | cualquier plan actual |

## Uso

Los snippets `.js` asumen una sesión de Appium 2.x activa creada con WebdriverIO (remota o local). Son código de referencia extraído de la guía — intégralos en tus specs y ajusta los selectores a los accessibility IDs de tu app.
