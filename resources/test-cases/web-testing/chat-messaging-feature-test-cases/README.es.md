# Casos de Prueba de Chat y Mensajería — Companion

Companion ejecutable para los [Casos de Prueba de Chat y Mensajería](https://qapractices.com/es/test-cases/chat-messaging-feature-test-cases/) de QAPractices.

Cubre las verificaciones en tiempo real que son difíciles de scriptar solo desde el checklist: ida y vuelta de mensaje WebSocket con chequeo de deduplicación (TC001/TC025), timeout del indicador de escritura (TC004) y los endpoints REST de la sección de comandos de ejemplo.

## Archivos

- `delivery-assertions.mjs` — script de Node 20 con `ws` (sin más dependencias): conecta dos clientes, verifica que el mensaje llega en ≤1s, que el indicador de escritura se limpia a los 5s de inactividad, y que no hay entrega duplicada tras una reconexión forzada. Apúntalo a un endpoint de staging: `node delivery-assertions.mjs --url wss://ws.staging.example.com/v1`.
- `send-message.sh` — ejemplos curl para las llamadas REST: enviar mensaje, obtener historial con paginación, marcar como leído.
- `package.json` — declara la dependencia `ws`.

## Ejecutar

```bash
npm install
WS_URL=wss://ws.staging.example.com/v1 TOKEN=$API_TOKEN node delivery-assertions.mjs
```

Requiere Node 20+ y un entorno de staging con usuarios sembrados — mira los casos de prueba para las precondiciones de cada verificación.
