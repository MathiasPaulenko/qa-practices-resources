# Casos de Prueba de Carga de Archivos — Companion

Materiales ejecutables del recurso [Casos de Prueba de Carga de Archivos: UX y Drag & Drop](https://qapractices.com/es/test-cases/file-upload-test-cases/) de QAPractices.

## Contenido

| Archivo | Qué es |
|---|---|
| `upload-demo/index.html` | Widget DocDrop 2.3: zona de drop con input de archivo oculto, lista blanca `accept` y límite de 10 MB. |
| `upload-demo/upload.js` | Lógica de la cola: comprobaciones de tipo/tamaño/vacío en el cliente antes de cualquier petición, progreso por archivo vía `xhr.upload`, controles de cancelar/reintentar/eliminar, estados de error con motivo. |
| `file-upload-ui.spec.ts` | Spec de Playwright 1.48 con 4 tests: camino feliz, rechazo de `.exe` en el cliente (afirma cero POSTs), estado reintentable tras un 500 del servidor y eliminación de la cola. Simula `/api/upload` con `page.route`. |
| `package.json` | Dependencia `@playwright/test` y el script `test`. |

## Inicio rápido

```bash
npm install
npx playwright install chromium
npm test
```

Para toquetear el widget a mano, sirve `upload-demo/` con cualquier servidor estático (p. ej. `npx http-server upload-demo -p 8080`) y abre `http://localhost:8080` — las cargas fallarán sin un `/api/upload` real, lo cual ya es una buena prueba manual de los estados de error.

## Notas

- `setInputFiles` funciona sobre el input oculto — es la ruta rápida. La ruta del drop necesita un `DataTransfer` sintetizado y es la única que detecta un manejador `dragover`/`drop` roto.
- Las comprobaciones del cliente (extensión, vacío, tamaño) se ejecutan **antes** de `xhr.open`, así que un rechazo debería producir cero peticiones de red — la spec afirma exactamente eso.
- La validación del lado servidor (magic bytes, antivirus, traversal) queda fuera del alcance a propósito; la suite a nivel API vive en `file-upload-download-test-cases`.
