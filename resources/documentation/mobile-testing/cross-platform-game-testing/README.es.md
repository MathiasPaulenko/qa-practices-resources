# Companion de Testing de Juegos Multiplataforma

Companion ejecutable de la [guía de Testing de Juegos Multiplataforma](https://qapractices.com/es/documentation/cross-platform-game-testing/) — utilidades pequeñas para las secciones de performance y certificación de la guía: un analizador de frame times, una captura de ejemplo, un checklist de pre-certificación en YAML y un script de monitoreo térmico con adb.

## Ejecutar

```bash
python frame_time_report.py frame_times_sample.csv
```

Requiere Python 3.12+; solo stdlib. Salida esperada contra la captura incluida:

```text
frames: 360 | avg fps: 55.7 | 1% low: 22.1 | stutters: 19
```

El logger térmico necesita un dispositivo Android conectado:

```bash
./thermal_log.sh 1800 thermal_log.csv   # sesión sostenida de 30 minutos
adb shell dumpsys gfxinfo <package> framestats  # para cruzar con frame times
```

## Qué cubre

| Archivo | Sección de la guía | Qué demuestra |
|---|---|---|
| `frame_time_report.py` | Testing de Performance | FPS promedio, 1% low y frames con stutter (>33 ms) desde una captura cruda |
| `frame_times_sample.csv` | Testing de Performance | Captura de 360 frames: stream a ~60 fps con spikes realistas de pacing |
| `cert-checklist.yaml` | Certificación y Compliance | Checks de pre-submission: suspend/resume, input, almacenamiento, errores, tienda, achievements |
| `thermal_log.sh` | Thermal throttling | Temperatura máxima de zonas térmicas muestreada cada 5 s durante una sesión |
