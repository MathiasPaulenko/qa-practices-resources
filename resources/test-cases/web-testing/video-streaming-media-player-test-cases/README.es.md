# Casos de Prueba de Video Streaming — Archivos Complementarios

Assets ejecutables para [Casos de Prueba Video Streaming y Media Player: Playback](https://qapractices.com/es/test-cases/video-streaming-media-player-test-cases/).

## Contenido

| Archivo | Propósito |
|---|---|
| `src/abr-throttling.spec.ts` | Spec de Playwright 1.48 que ejecuta TC-VS-002: inicia el playback, limita la red vía CDP `Network.emulateNetworkConditions` y verifica el cambio de rendition sin stall. |
| `src/mock-hls-playlist.m3u8` | Playlist maestra HLS mínima con cuatro renditions (240p–1080p) para tests de player en local sin CDN. |

## Uso

```bash
npm install -D @playwright/test
npx playwright install chromium
npx playwright test src/abr-throttling.spec.ts
```

Apuntá `PLAYER_URL` en el spec a tu player de staging. Serví `mock-hls-playlist.m3u8` junto con las playlists de cada rendition desde cualquier servidor estático para testear ABR en local.
