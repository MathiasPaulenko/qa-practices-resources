# Mobile App Beta Distribution Testing Template — Companion

Copyable artifacts for the [Mobile App Beta Distribution Testing Template](https://qapractices.com/templates/mobile-app-beta-distribution-testing-template) on QAPractices.

## What's inside

| Path | What it is |
|---|---|
| `docs/beta-distribution-template.md` | The blank beta distribution document: tracks, device matrix, OS compat, feedback, crash metrics, rollout stages, release gates and sign-off. |
| `docs/cartwell-beta-sample.md` | The same document filled in for CartWell Shopper v4.2.0 — a two-week external beta on both platforms. |
| `fastlane/Fastfile` | One lane per distribution track (`ios_beta_internal`, `ios_beta_external`, `android_beta_internal`, `android_beta_closed`) plus `android_rollout` for staged rollout percentages. |
| `.env.example` | The env vars the lanes read: App Store Connect API key, Play Console service account path, beta metadata and the crash-free threshold. |

## Usage

1. Copy `docs/beta-distribution-template.md` into your repo per beta cycle.
2. Copy `fastlane/Fastfile` and `.env.example` into your project and adjust scheme, groups and tracks.
3. Run a lane per track — `fastlane ios ios_beta_external`, `fastlane android android_beta_closed` — so the track table and the tooling can never disagree silently.
4. For staged rollout: `fastlane android android_rollout percent:0.20` per stage, gated on the crash-free threshold in `.env.example`.

## Notes

- Requires fastlane 2.220+, an App Store Connect API key and a Play Console service account JSON key. Keys never get committed — the paths in `.env.example` point to a `keys/` directory you gitignore.
- iOS phased release is toggled in App Store Connect, not fastlane; Play Console rollout percentages are the `rollout:` parameter on the production track.
