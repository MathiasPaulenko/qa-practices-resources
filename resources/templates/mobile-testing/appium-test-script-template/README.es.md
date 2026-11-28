# Plantilla de Script de Test con Appium — Companion

Archivos ejecutables de la [Plantilla de Script de Test con Appium](https://qapractices.com/es/templates/appium-test-script-template/) de QAPractices. Copia el esqueleto a tu proyecto, rellena los marcadores TODO y ejecútalo contra un servidor Appium 2.x local — sin copy-paste desde el navegador.

## Archivos

| Archivo | Qué es |
|---|---|
| `appium-test-template.js` | El esqueleto en blanco: config de entorno, capabilities W3C para UiAutomator2 (con la variante XCUITest comentada), setup de sesión, helper de wait explícito, flujo de test y teardown |
| `appium-login-sample.js` | El mismo esqueleto completado para un flujo de login en una app Android ficticia de e-commerce (`shopwave-2.4.1-debug.apk`, emulador `Pixel_8_API_34`) |

## Uso

1. Instala Appium 2.x y los drivers: `npm i -g appium`, después `appium driver install uiautomator2` (y `xcuitest` en macOS para iOS).
2. Añade WebdriverIO a tu proyecto (`npm i webdriverio`) o porta el archivo a tu test runner.
3. Rellena cada marcador TODO de `appium-test-template.js`: ruta de la app, nombre del dispositivo, accessibility IDs, texto esperado.
4. Arranca el servidor (`appium` escucha en `http://127.0.0.1:4723` por defecto) y ejecuta el script.

## Relacionados

- [Plantilla de Script de Test con Appium](https://qapractices.com/es/templates/appium-test-script-template/) — la plantilla completa con mejores prácticas, errores comunes y FAQ
- [Cheat Sheet de Comandos de Appium](https://qapractices.com/es/documentation/appium-commands-cheat-sheet/) — los comandos de driver usados dentro de los bloques de flujo
