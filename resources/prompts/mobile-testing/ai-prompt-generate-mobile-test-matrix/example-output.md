# Example output fragment — Ledgerly mobile test matrix

```text
Assumptions
- No analytics supplied; device picks anchored to US/MX/BR market
  share (Samsung + Motorola dominant in MX/BR, iPhone in US).
- "P0 must run before every release" interpreted as ≤ 12 combos.

Axes included: device tier (flagship/mid/low RAM), OS version,
screen size + density, network (5G/4G/3G/offline), orientation,
locale (en/es/pt). Axes excluded: tablets (not supported), Android
Go (below min RAM profile of the app), rooted devices.

P0 — release blockers (10 combos)
1. Pixel 8, Android 15, 6.2" 420dpi, 4G — top US share, flagship ref
2. Galaxy S23, Android 14, 6.1" 480dpi, 5G — flagship Samsung camera
   path differs from Pixel; receipt capture must pass on both
3. Moto G84, Android 13, 6.5" 405dpi, 4G — dominant MX/BR mid-range
4. iPhone 15, iOS 18, 6.1", 4G — current-gen iOS reference
5. iPhone 12, iOS 16, 6.1", 3G — oldest supported form factor at scale
6. Low-RAM Android 10 device (Galaxy A12 class), 4G — floor of
   supported OS; offline sync pressure
7-10. P0 network variants: offline capture + sync recovery on combos
1 and 4; deep-link cold start on 2 and 5.

P1 — weekly regression (~14 combos)
Emulator/simulator variants of P0 plus: Android 11/12 steps, iOS 17,
es-MX and pt-BR locales, landscape orientation.

P2 — spot check / cloud-only (~10 combos)
Foldable inner display, Android 15 beta, iOS 18 beta, 2G-edge
network, max font scaling accessibility pass.

Execution map: P0 on the 6 physical devices (~1.5 QA days), P1 on
Firebase Test Lab + iOS simulator matrix (overnight), P2 monthly on
cloud farm.

Gaps accepted: tablets, Android Go, rooted devices, pre-Android-10 —
out of support scope or <1% of target-market share.
Maintenance triggers: Android 16 / iOS 19 release, device share shift
>2 points in analytics, new camera or payment feature.
```
