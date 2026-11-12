# Companion de Testing de Localización para Juegos

Recurso companion de [Testing de Localización para Juegos](https://qapractices.com/es/documentation/localization-testing-for-games). Scripts ejecutables para las tres puertas mecánicas de l10n de la guía: pseudo-localización, presupuestos de expansión y detección de strings hardcodeados.

## Archivos

| Archivo | Qué hace | Stack |
|---------|----------|-------|
| `pseudolocalize.py` | Acentúa, expande y envuelve strings para builds pseudo-localizadas | Python 3.9+ stdlib |
| `check_expansion.py` | Marca traducciones que exceden su presupuesto de expansión por área | Python 3.9+ stdlib, entrada CSV |
| `find_hardcoded_strings.py` | Escanea fuentes buscando literales de UI que saltan la tabla de strings | Python 3.9+ stdlib |

## Inicio Rápido

```bash
# Generar una tabla de strings pseudo-localizada
python pseudolocalize.py < strings_en.txt > strings_pseudo.txt

# Verificar una exportación en alemán contra los presupuestos (sale 1 si hay violaciones)
python check_expansion.py strings_de.csv

# Encontrar strings de UI hardcodeados en el código del juego
python find_hardcoded_strings.py src/ --ext .cs .gd .cpp
```

Los tres corren solo con la stdlib — sin dependencias. `check_expansion.py` devuelve código de salida distinto de cero cuando encuentra violaciones, así que entra directo en una puerta de CI.

## Requisitos

- Python 3.9+
- Un CSV de tabla de strings para `check_expansion.py` con columnas `key`, `en`, `target` y opcionalmente `ui_area` (`button`, `hud`, `paragraph`; por defecto `default`)
