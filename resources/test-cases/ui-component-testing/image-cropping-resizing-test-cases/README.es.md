# Casos de Prueba de Recorte y Redimensionamiento de Imágenes — Laboratorio Companion

Companion del recurso [Casos de Prueba de Recorte y Redimensionamiento de Imágenes](https://qapractices.com/es/test-cases/image-cropping-resizing-test-cases/) en QAPractices.com.

`image_pipeline.py` es un modelo en Pillow del pipeline de crop/resize: sniffing de formato, normalización de orientación EXIF, clamping de bounds/tamaño mínimo/proporción, mapeo de coordenadas de previsualización a fuente bajo zoom, export con manejo de alpha, recorte de todos los frames de un GIF y resize en batch. Codifica las *reglas* para que los puntos de fallo del recurso se puedan assertar sin navegador — los checks a nivel UI usan Playwright, como se ve en `crop-preset.spec.ts` y en el propio recurso.

## Qué cubre el modelo

- **Etapa de selección (TC-01 a TC-12, TC-30):** drift de crop, bloqueos de ratio 1:1 y 16:9, free crop, tamaño mínimo, clamping a bounds, mapeo de coordenadas con zoom.
- **Etapa de carga (TC-13, TC-14 + tabla de borde):** formatos no soportados, archivos corruptos, sniffing por magic bytes, orientación EXIF aplicada al decodificar.
- **Etapa de transformación (TC-09, TC-15, TC-16, TC-17):** resize a dimensiones exactas, salida 1×1, tope de bitmap sobredimensionado, fotos verticales que siguen derechas.
- **Etapa de export (TC-10, TC-23, TC-24, TC-26, TC-27):** conversión a JPEG, preservación de alpha en PNG, recorte de todos los frames del GIF, monotonía calidad-tamaño, resize batch con resultados por archivo.

## Ejecutar

```bash
pip install -r requirements.txt
pytest -v
```

Esperado: `20 passed` en menos de un segundo. Los tests generan sus propios fixtures (un JPEG vertical con `Orientation=6`, un PNG RGBA, un GIF de 12 frames, un JPEG truncado, un BMP), así que no hace falta nada externo.

## Archivos

- `image_pipeline.py` — `load_image`, `clamp_crop_box`, `preview_to_source`, `crop_image`, `resize_image`, `export_image`, `crop_animation`, `batch_resize`.
- `tests/test_image_pipeline.py` — 20 tests agrupados por etapa del pipeline, nombrados según los ids TC del recurso.
- `crop-preset.spec.ts` — spec de Playwright para el flujo de crop con preset en el navegador (requiere tu UI de crop corriendo).
- `crop.feature` — feature Gherkin que cubre el flujo de crop de punta a punta.
- `requirements.txt`, `pytest.ini` — Pillow 11.2.1 + pytest 8.3.4 fijados.
