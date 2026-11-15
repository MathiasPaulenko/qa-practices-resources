# Mobile Deep Link Testing Matrix

## Deep Link Details

| Field | Details |
|---|---|
| **App name** | [App name] |
| **Platforms** | [iOS / Android / Both] |
| **Link types** | [Universal Links / App Links / Custom URI / Deferred] |
| **Deep link provider** | [Branch / Firebase / AppsFlyer / Custom] |
| **Domain(s)** | [example.com, app.example.com] |
| **Test lead** | [Name / Role] |
| **Test dates** | [YYYY-MM-DD to YYYY-MM-DD] |

## Universal Links (iOS) Tests

| Link | App Installed | App in Background | App Not Installed | Correct Screen? | Fallback Works? | Status | Notes |
|---|---|---|---|---|---|---|---|
| `https://example.com/product/123` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/profile` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/cart` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/search?q=shoes` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Query params |
| `https://example.com/category/electronics` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |

### Universal Links Checklist

- [ ] `apple-app-site-association` file served over HTTPS
- [ ] AASA file valid JSON with correct app IDs
- [ ] AASA file at root domain or `/.well-known/`
- [ ] App registered associated domains in entitlements
- [ ] Links open app directly (no Safari interstitial)
- [ ] Correct screen/route displayed for each link
- [ ] Fallback to Safari when app not installed

## App Links (Android) Tests

| Link | App Installed | App in Background | App Not Installed | Correct Screen? | Fallback Works? | Status | Notes |
|---|---|---|---|---|---|---|---|
| `https://example.com/product/123` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/profile` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/cart` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/search?q=shoes` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | Query params |
| `https://example.com/category/electronics` | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | |

### App Links Checklist

- [ ] `assetlinks.json` file served over HTTPS
- [ ] Assetlinks file at `/.well-known/assetlinks.json`
- [ ] Assetlinks file contains correct package name and fingerprint
- [ ] Intent filters configured in AndroidManifest.xml
- [ ] `autoVerify="true"` set on intent filter
- [ ] Links open app directly (no disambiguation dialog)
- [ ] Correct screen/route displayed for each link
- [ ] Fallback to browser when app not installed

## Custom URI Scheme Tests

| URI Scheme | App Installed | App Not Installed | Correct Screen? | Error Handling? | Status | Notes |
|---|---|---|---|---|---|---|
| `myapp://product/123` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `myapp://profile` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `myapp://cart` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `myapp://search?q=shoes` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `myapp://deeplink/invalid` | [ ] | [ ] | [ ] | [ ] | [ ] | Invalid route |

### Custom URI Checklist

- [ ] URI scheme registered in app config (Info.plist / AndroidManifest)
- [ ] Correct screen displayed for each URI
- [ ] Invalid URIs handled gracefully (error page, home, or message)
- [ ] App not installed: browser shows error or redirect to store
- [ ] Query parameters parsed correctly
- [ ] No crash on malformed URIs

## Deferred Deep Link Tests

| Scenario | Link | App Installed at Click? | After Install: Correct Screen? | Data Passed? | Status | Notes |
|---|---|---|---|---|---|---|
| First install via link | `https://example.com/product/123` | No | [ ] | [ ] | [ ] | |
| Re-install via link | `https://example.com/profile` | No | [ ] | [ ] | [ ] | |
| Already installed click | `https://example.com/cart` | Yes | [ ] | [ ] | [ ] | Direct link |
| Attribution data | `https://example.com/?campaign=spring` | No | [ ] | [ ] | [ ] | Campaign tracking |
| Cross-device | `https://example.com/product/123` | No (different device) | [ ] | [ ] | [ ] | |

### Deferred Deep Link Checklist

- [ ] Deep link provider SDK integrated (Branch / Firebase / AppsFlyer)
- [ ] Deferred deep link retrieved after first app launch
- [ ] Correct screen displayed after install from link
- [ ] Attribution and campaign data passed correctly
- [ ] Deep link data available in analytics
- [ ] No deep link data lost on app reinstall
- [ ] Cross-device deep linking works (if supported)

## Fallback Behavior Tests

| Scenario | Link | App State | Expected Fallback | Actual Behavior | Status | Notes |
|---|---|---|---|---|---|---|
| App not installed (iOS) | Universal link | Not installed | Safari opens web page | [ ] | [ ] | |
| App not installed (Android) | App link | Not installed | Browser opens web page | [ ] | [ ] | |
| App not installed (both) | Custom URI | Not installed | Error or store redirect | [ ] | [ ] | |
| App disabled (Android) | App link | Disabled | Browser opens | [ ] | [ ] | |
| AASA file missing (iOS) | Universal link | Installed | Safari opens (no app) | [ ] | [ ] | |
| Assetlinks missing (Android) | App link | Installed | Disambiguation dialog | [ ] | [ ] | |

### Fallback Checklist

- [ ] Web fallback page displays correct content
- [ ] Store redirect works when app not installed
- [ ] No broken page or error when app not installed
- [ ] Fallback page includes app install CTA
- [ ] Fallback page preserves deep link destination
- [ ] Graceful handling of missing association files

## Cross-Platform Routing Tests

| Link | iOS Behavior | Android Behavior | Web Behavior | Consistent? | Status | Notes |
|---|---|---|---|---|---|---|
| `https://example.com/product/123` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/profile` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/cart` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `https://example.com/search?q=test` | [ ] | [ ] | [ ] | [ ] | [ ] | |
| `myapp://product/123` | [ ] | [ ] | N/A | [ ] | [ ] | |

### Cross-Platform Checklist

- [ ] Same link routes to equivalent screen on iOS and Android
- [ ] Web fallback shows equivalent content
- [ ] No platform-specific broken routes
- [ ] Query parameters handled consistently
- [ ] Route parameters extracted correctly on both platforms

## Deep Link Analytics Tests

| Event | Platform | Trigger | Event Logged? | Data Correct? | Status | Notes |
|---|---|---|---|---|---|---|
| Deep link open | iOS | Universal link click | [ ] | [ ] | [ ] | |
| Deep link open | Android | App link click | [ ] | [ ] | [ ] | |
| Deferred deep link | Both | First launch after install | [ ] | [ ] | [ ] | |
| Deep link fallback | Both | App not installed | [ ] | [ ] | [ ] | |
| Campaign attribution | Both | Campaign link click | [ ] | [ ] | [ ] | |

## Defect Tracking

| Defect ID | Category | Severity | Platform | Description | Status | Notes |
|---|---|---|---|---|---|---|
| DL-001 | Universal Links | High | iOS | AASA file not found at /.well-known/ | [ ] | |
| DL-002 | App Links | High | Android | Disambiguation dialog appears | [ ] | |
| DL-003 | Custom URI | Medium | Both | App crashes on malformed URI | [ ] | |
| DL-004 | Deferred | High | Both | Deferred deep link lost after install | [ ] | |
| DL-005 | Fallback | Medium | iOS | Web fallback page shows 404 | [ ] | |

## Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | [Name] | [Date] | [Decision] |
| **Mobile Lead** | [Name] | [Date] | [Decision] |
| **Product Manager** | [Name] | [Date] | [Decision] |
