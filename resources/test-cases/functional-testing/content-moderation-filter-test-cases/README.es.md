# Filtro de Moderación de Contenido — Companion

Suite pytest ejecutable para el recurso [Casos de Prueba de Filtro de Moderación de Contenido](https://qapractices.com/es/test-cases/content-moderation-filter-test-cases/) en QAPractices.

`conftest.py` incluye una implementación de referencia `moderate()` basada en reglas: normalización NFKC, mapeo de homoglifos, conversión de leet speak, eliminación de emojis/puntuación y matching por límite de palabra contra una blocklist. La suite ejercita los casos donde los filtros reales fallan — falsos positivos por substring, intentos de bypass, determinismo del umbral, entrada vacía y sobredimensionada.

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/ -v          # 24 tests
```

## Cubre

- Positivos: detección de blasfemias, paso de contenido limpio, spam de links repetidos, scores de toxicidad alta/baja
- Falsos positivos: términos de diccionario del problema Scunthorpe, discusión académica sensible
- Bypass: leet speak, homoglifos cirílicos, espaciado/puntuación, inserción de emojis, equivalencia NFC/NFD
- Límites: score exactamente en el umbral, entrada solo-espacios, contenido de 80k caracteres, borde de conteo de links
