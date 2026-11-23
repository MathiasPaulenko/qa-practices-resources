# Pruebas de Seguridad Móvil — Kit companion

Scripts companion de la guía [Pruebas de Seguridad Móvil con OWASP MASVS](https://qapractices.com/es/documentation/mobile-security-testing/) en QAPractices.com. Todo esto asume que pruebas una app propia o que tienes autorización para probar.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `scripts/mobsf-scan.sh` | Arranca MobSF 4.x en Docker en el puerto 8000 para subir un APK o IPA al análisis estático. |
| `scripts/decompile-apk.sh` | Decompila un APK con apktool 2.9+ y lista el manifest y `network_security_config` para revisión. |
| `scripts/storage-audit.sh` | Recorre `shared_prefs`, `files` y `databases` de un build depurable vía `adb shell run-as` y marca archivos que pueden contener tokens o datos personales. |
| `scripts/logcat-watch.sh` | Muestra `adb logcat` filtrando líneas con patrones típicos de filtrado (tokens, contraseñas, headers Bearer). |
| `objection/session.txt` | Secuencia ordenada de comandos de objection 1.11.x para una sesión en tiempo de ejecución: bypass de pinning, bypass de detección de root, enumeración de almacenamiento. |
| `android/network_security_config.xml` | Configuración solo para debug que confía en CAs instaladas por el usuario para que mitmproxy/ZAP pueda interceptar el tráfico. Nunca la publiques en builds de release. |

## Requisitos

- Android SDK Platform-Tools (`adb`), un emulador rooteado o un build depurable para `run-as` y objection
- Docker para `mobsf-scan.sh`; apktool 2.9+ para `decompile-apk.sh`
- mitmproxy 11.x u OWASP ZAP para la intercepción de tráfico; objection 1.11.x para `objection/session.txt`

## Uso

```bash
# 1. Escaneo estático — luego abre http://localhost:8000 y sube el APK
./scripts/mobsf-scan.sh

# 2. Decompilación e inspección del manifest + network security config
./scripts/decompile-apk.sh app-release.apk

# 3. Auditoría de almacenamiento local en un build depurable
./scripts/storage-audit.sh com.acme.banking

# 4. Vigilar logcat en busca de tokens o credenciales mientras recorres login y pagos
./scripts/logcat-watch.sh com.acme.banking

# 5. Sesión en tiempo de ejecución — ejecuta los comandos de objection/session.txt dentro de `explore`
objection -g com.acme.banking explore
```

Sustituye `com.acme.banking` por el nombre de tu paquete. Usa esto solo en builds y dispositivos que tengas autorización para probar.
