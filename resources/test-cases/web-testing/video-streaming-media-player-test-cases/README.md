# Video Streaming Test Cases — Companion Files

Executable assets for [Video Streaming and Media Player Test Cases: Playback](https://qapractices.com/test-cases/video-streaming-media-player-test-cases/).

## Contents

| File | Purpose |
|---|---|
| `src/abr-throttling.spec.ts` | Playwright 1.48 spec that drives TC-VS-002: starts playback, throttles via CDP `Network.emulateNetworkConditions`, and asserts rendition downshift/upshift without a stall. |
| `src/mock-hls-playlist.m3u8` | Minimal HLS master playlist with four renditions (240p–1080p) for local player tests without a CDN. |

## Usage

```bash
npm install -D @playwright/test
npx playwright install chromium
npx playwright test src/abr-throttling.spec.ts
```

Point `PLAYER_URL` in the spec at your staging player. Serve `mock-hls-playlist.m3u8` plus matching variant playlists from any static server to test ABR locally.
