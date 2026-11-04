# Companion del Checklist de Ubicación y GPS Móvil

Recurso companion del [Checklist de Ubicación y GPS Móvil](https://qapractices.com/es/checklists/mobile-location-gps-testing-checklist). Contiene scripts de ubicación simulada para el emulador de Android y dispositivos reales, más un esqueleto de test de flujo de permisos.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `mock_location.sh` | Envía un fix de GPS simulado a un emulador Android vía `geo fix`, o habilita mock location en un dispositivo real con `adb` |
| `test_location_permission_flow.py` | Test de flujo de permiso: dispara el diálogo del sistema, concede permiso, verifica que la feature funciona |

## Inicio Rápido

```bash
# Emulador (el primer emulador escucha en 5554)
./mock_location.sh emulator 37.4219983 -122.084

# Dispositivo real con opciones de desarrollador + app de mock-location configurada
./mock_location.sh device 37.4219983 -122.084

python -m pytest test_location_permission_flow.py -v
```

## Requisitos

- Android SDK platform-tools (`adb`, consola telnet del emulador)
- Python 3.11+ con pytest 8.x y un driver de UI test (Appium o similar) para el test de flujo
- Para iOS: usa la ubicación simulada de Xcode o un archivo `.gpx` — mock location no está disponible fuera del simulador

## Notas

- `geo fix` fija una coordenada estática; encadena una serie de fixes para simular una ruta, o usa el playback de rutas del emulador.
- Detecta proveedores mock en los tests con `Location.isFromMockProvider()` (API 31+) o `ALLOW_MOCK_LOCATION` en APIs antiguas.
- El test de permiso afirma sobre IDs de `com.android.packageinstaller` — ajústalos a tu versión de Android; los IDs del diálogo varían según la capa del fabricante.
