# Companion de la Checklist de Pruebas de Permisos de Apps Móviles

Recurso complementario de la [Checklist de Pruebas de Permisos de Apps Móviles](https://qapractices.com/es/checklists/mobile-app-permission-testing-checklist). Contiene un script `adb` para conceder, revocar, resetear e inspeccionar permisos runtime de Android, más un esqueleto de tests con Appium/WebdriverIO para los flujos principales de permisos.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `permission_adb.sh` | Concede, revoca, resetea o inspecciona permisos runtime de un paquete en un dispositivo Android o emulador conectado |
| `appium_permissions.test.js` | Esqueleto de tests con Appium WebdriverIO: flujo de auto-concesión, denegación permanente con deep link a Ajustes, y manejo de la alerta one-shot de iOS |

## Inicio Rápido

```bash
# Conceder permiso de cámara al build instalado
./permission_adb.sh com.example.app grant android.permission.CAMERA

# Revocarlo y reabrir para probar el camino de denegación
./permission_adb.sh com.example.app revoke android.permission.CAMERA

# Restaurar todos los permisos runtime al estado de instalación
./permission_adb.sh com.example.app reset

# Inspeccionar el estado de concesión de cada permiso declarado
./permission_adb.sh com.example.app dump

# Ejecutar el esqueleto de Appium (edita las capabilities primero)
node appium_permissions.test.js
```

## Requisitos

- Android SDK platform-tools (`adb`) para el script de shell.
- Node.js 20+ con `webdriverio` y un servidor Appium 2.x con los drivers `uiautomator2` y `xcuitest`.
- Para tests de denegación en iOS sobre el simulador, `xcrun simctl privacy <device> reset <bundleId>` resetea todas las concesiones de privacidad entre ejecuciones.

## Notas

- `autoGrantPermissions` omite por completo el diálogo del sistema — úsalo solo en suites de camino feliz, nunca cuando lo que se prueba es el flujo de denegación.
- Los IDs del diálogo de permisos (`com.android.packageinstaller`) varían entre versiones de Android y capas de fabricante; verifica el deep link a Ajustes sobre la UI propia de la app.
- Android 11+ puede resetear automáticamente los permisos de apps sin uso. Simula la ruta de re-solicitud revocando con `pm revoke` y reabriendo, en lugar de esperar al job del sistema.
