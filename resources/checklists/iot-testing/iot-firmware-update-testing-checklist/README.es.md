# Companion del Checklist de Testing de Actualización de Firmware IoT

Recurso companion del [Checklist de Testing de Actualización de Firmware IoT](https://qapractices.com/es/checklists/iot-firmware-update-testing-checklist). Contiene un ejemplo de manifest de firmware OTA y un test estilo pytest de recuperación ante pérdida de energía que ejercita el rollback tras una actualización interrumpida.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `ota-manifest.json` | Manifest de actualización de ejemplo con version, minVersion, size, checksum SHA-256 y firma |
| `test_power_loss_recovery.py` | Test de recuperación ante pérdida de energía: actualizar, cortar energía, restaurar, verificar versión de rollback |

## Inicio Rápido

```bash
python -m pytest test_power_loss_recovery.py -v
```

El test espera un CLI `ota-client` más comandos `power-cut`/`power-restore` en el PATH — sustitúyelos por tu cliente OTA y tu herramienta de control de energía (relé de fuente de banco, API de switch PoE o un emulador de dispositivo).

## Requisitos

- Python 3.11+ con pytest 8.x
- Un CLI de cliente OTA (Mender, swupdate o propio) y un harness de control de energía

## Notas

- `minVersion` en el manifest es el piso anti-rollback: las imágenes por debajo deben rechazarse.
- El checksum usa SHA-256 — nunca MD5 ni SHA-1 para integridad de firmware.
- Extiende el test con un disparo de health check fallido para cubrir el camino de rollback por watchdog.
