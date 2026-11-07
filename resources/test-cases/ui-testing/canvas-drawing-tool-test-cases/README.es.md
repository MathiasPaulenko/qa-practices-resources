# Casos de Prueba de Dibujo Canvas — Companion Ejecutable

> Ejemplos ejecutables de [Casos de Prueba: Herramienta de Dibujo Canvas](https://qapractices.com/es/test-cases/canvas-drawing-tool-test-cases/).

El contenido canvas vive en un bitmap, no en el DOM — por eso estos ejemplos assertan contra datos de píxel (`toDataURL`, bytes PNG) en lugar de selectores.

## Archivos

- `canvas-drawing.spec.ts` — spec de Playwright 1.49 que cubre trazo con mouse (TC-001), restore de undo (TC-006), trazo touch (TC-019) y download del export PNG (TC-009).
- `fixture/canvas-draw.html` — app de dibujo mínima con manejo de `pointerdown`/`pointermove`/`pointerup`/`pointercancel`, stack de historial con image data, undo y export PNG vía `toDataURL`.
- `canvas_export_check.py` — chequeo con Pillow de que un PNG exportado tiene las dimensiones correctas y no salió completamente transparente.

## Cómo usar

```bash
npm install
npx playwright install chromium
npm test

# tras una corrida, verificá un export descargado
python canvas_export_check.py canvas.png 600 400
```

## Requisitos

- Node.js 20+, Playwright 1.49
- Python 3.11+ con Pillow para el chequeo del export

## Notas

- El fixture usa Pointer Events, así que los dispatches con `pointerType: 'touch'` funcionan sin dispositivo real. Los valores de presión reales igual necesitan hardware — ver TC-021 en el recurso fuente.
- Las comparaciones de `toDataURL` son exactas: cualquier diferencia de anti-aliasing entre entornos puede dar falsos positivos. Para matching más laxo, compará regiones con `getImageData`.
