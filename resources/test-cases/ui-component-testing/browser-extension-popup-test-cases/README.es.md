# Casos de Prueba de Popup de Extensión — Companion

Materiales ejecutables del recurso [Casos de Prueba de Popup de Extensión de Navegador](https://qapractices.com/es/test-cases/browser-extension-popup-test-cases/) de QAPractices.

## Contenido

| Archivo | Qué es |
|---|---|
| `extension/manifest.json` | Manifiesto Manifest V3 mínimo: permiso `storage`, `activeTab` como opcional, background con service worker, popup en la acción. |
| `extension/popup.html` | Popup estilo TabSaver: input de nota, botón Guardar, lista de páginas guardadas, toggle de vista compacta y estilos de modo oscuro. |
| `extension/popup.js` | Lógica del popup: carga el estado desde `chrome.storage.local` al abrir, pide `activeTab` al hacer clic, guarda entradas y muestra un error reintentable cuando el worker no responde. |
| `extension/background.js` | Service worker MV3 con manejador `chrome.runtime.onMessage` usando `sendResponse`. |
| `popup-persistence.spec.ts` | Spec de Playwright 1.48: lanza un contexto persistente con la extensión cargada, abre `chrome-extension://{id}/popup.html`, guarda una página y verifica que la lista se rehidrata desde storage tras reabrir. |
| `package.json` | Dependencia `@playwright/test` y el script `test`. |

## Inicio rápido

```bash
# Instala el runner de Playwright (Node 18+)
npm install
npx playwright install chromium

# Ejecuta la spec (con ventana — los contextos persistentes la necesitan)
npm test
```

Para probar el popup manualmente, carga `extension/` como extensión sin empaquetar en `chrome://extensions` con el modo desarrollador activado.

## Notas

- Las extensiones solo se cargan dentro de un **contexto persistente** (`chromium.launchPersistentContext`); un `browser.newContext()` normal no las reconoce. En CI usa `--headless=new` — el modo headless antiguo no ejecuta extensiones.
- El popup se destruye al perder el foco: cada apertura vuelve a ejecutar `loadState()` y rehidrata la UI desde `chrome.storage.local`. Ese comportamiento de arranque en frío es lo que verifica el TC-006.
- El service worker de background puede dormirse tras ~30 segundos inactivo; el primer `sendMessage` posterior ejercita la ruta de despertar cubierta por el TC-012.
