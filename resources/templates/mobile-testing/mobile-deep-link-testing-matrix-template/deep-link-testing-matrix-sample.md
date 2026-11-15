# Mobile Deep Link Testing Matrix — Completed Sample

Filled excerpt for a fictional e-commerce app: Shoply (`shop.example.io`), iOS 16+ and Android 12+, Branch for deferred deep links.

## Deep Link Details

| Field | Details |
|---|---|
| **App name** | Shoply |
| **Platforms** | Both (iOS 16+, Android 12+) |
| **Link types** | Universal Links, App Links, Deferred (Branch) |
| **Deep link provider** | Branch |
| **Domain(s)** | shop.example.io, go.shop.example.io |
| **Test lead** | Dana Whitfield / QA Lead |
| **Test dates** | 2026-11-02 to 2026-11-06 |

## Universal Links (iOS) Tests

| Link | App Installed | App in Background | App Not Installed | Correct Screen? | Fallback Works? | Status | Notes |
|---|---|---|---|---|---|---|---|
| `https://shop.example.io/product/123` | Pass | Pass | Safari → web PDP | Yes | Yes | Done | |
| `https://shop.example.io/cart` | Pass | Pass | Safari → cart | Yes | Yes | Done | |
| `https://shop.example.io/search?q=shoes` | Pass | Resumes on home | Safari → search | No | Yes | Failed | Logged as DL-001 |

## App Links (Android) Tests

| Link | App Installed | App in Background | App Not Installed | Correct Screen? | Fallback Works? | Status | Notes |
|---|---|---|---|---|---|---|---|
| `https://shop.example.io/product/123` | Pass | Pass | Browser → web PDP | Yes | Yes | Done | Verified via `pm get-app-links` |
| `https://shop.example.io/cart` | Pass | Pass | Browser → cart | Yes | Yes | Done | |

## Custom URI Scheme Tests

| URI Scheme | App Installed | App Not Installed | Correct Screen? | Error Handling? | Status | Notes |
|---|---|---|---|---|---|---|
| `shoply://product/123` | Pass | Browser error page | Yes | Yes | Done | |
| `shoply://deeplink/invalid` | Pass | Browser error page | Friendly error | Yes | Done | |

## Deferred Deep Link Tests

| Scenario | Link | App Installed at Click? | After Install: Correct Screen? | Data Passed? | Status | Notes |
|---|---|---|---|---|---|---|
| First install via link | `https://go.shop.example.io/product/123` | No | Yes | Yes | Done | Branch payload intact |
| Attribution data | `https://go.shop.example.io/?campaign=black-friday` | No | Yes | Yes | Done | Campaign params reached analytics |

## Fallback Behavior Tests

| Scenario | Link | App State | Expected Fallback | Actual Behavior | Status | Notes |
|---|---|---|---|---|---|---|
| App not installed (iOS) | Universal link | Not installed | Safari opens web page | Safari → web PDP | Done | Install CTA present |
| App not installed (Android) | App link | Not installed | Browser opens web page | Browser → web PDP | Done | |

## Cross-Platform Routing Tests

| Link | iOS Behavior | Android Behavior | Web Behavior | Consistent? | Status | Notes |
|---|---|---|---|---|---|---|
| `https://shop.example.io/product/123` | Product screen | Product screen | Web PDP | Yes | Done | |
| `shoply://product/123` | Product screen | Product screen | N/A | Yes | Done | |

## Deep Link Analytics Tests

| Event | Platform | Trigger | Event Logged? | Data Correct? | Status | Notes |
|---|---|---|---|---|---|---|
| Deep link open | iOS | Universal link click | Yes | Yes | Done | `deep_link_opened` in Firebase |
| Deferred deep link | Both | First launch after install | Yes | Yes | Done | Attribution source = Branch |

## Defect Tracking

| Defect ID | Category | Severity | Platform | Description | Status | Notes |
|---|---|---|---|---|---|---|
| DL-001 | Universal Links | High | iOS | Backgrounded app ignores the `/search` route and resumes on home | Open | Repro on iOS 18.1, AASA v12 deployed |

## Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | Dana Whitfield | 2026-11-06 | Approved with DL-001 open |
| **Mobile Lead** | Kenji Sato | 2026-11-06 | Deep links verified |
| **Product Manager** | Priya Nair | 2026-11-06 | Routing validated |
