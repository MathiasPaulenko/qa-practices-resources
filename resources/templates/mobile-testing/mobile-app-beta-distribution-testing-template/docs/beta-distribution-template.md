# Beta Distribution Testing Document

Fill this document per beta cycle. See the full guide at https://qapractices.com/templates/mobile-app-beta-distribution-testing-template

### 1. Beta Details

| Field | Details |
|---|---|
| **App name** | [App name] |
| **Version / build** | [X.Y.Z (build N)] |
| **Platform(s)** | [iOS / Android / Both] |
| **iOS distribution** | [TestFlight Internal / External] |
| **Android distribution** | [Play Console Internal / Closed / Open] |
| **Beta testers** | [N internal / N external] |
| **Beta duration** | [X days] |
| **Test lead** | [Name / Role, e.g. Ali Rahman / QA Lead] |
| **Test dates** | [YYYY-MM-DD to YYYY-MM-DD] |

### 2. Beta Track Configuration

| Platform | Track | Tester Group | Build Available | Install Works | Status | Notes |
|---|---|---|---|---|---|---|
| **iOS** | TestFlight Internal | [Internal team] | [ ] | [ ] | [ ] | [Build expires in 90 days] |
| **iOS** | TestFlight External | [External beta group] | [ ] | [ ] | [ ] | [Requires Beta App Review] |
| **Android** | Play Console Internal | [Internal testers] | [ ] | [ ] | [ ] | [Up to 100 testers] |
| **Android** | Play Console Closed | [Closed beta list] | [ ] | [ ] | [ ] | [Email list or Google Group] |
| **Android** | Play Console Open | [Open beta] | [ ] | [ ] | [ ] | [Public via Play Store] |

#### Beta Track Checklist

- [ ] Build uploaded to the correct track (internal and closed tracks are not interchangeable)
- [ ] Build processed and installable on a real device, not just listed as available
- [ ] Tester email list or Google Group current and accurate
- [ ] Public beta link generated and smoke-tested in a browser without a Google account
- [ ] Beta build expiration date communicated to testers
- [ ] Beta testing guidelines and known issues sent with the invite
- [ ] Feedback channel established (email / form / in-app)

### 3. Device Coverage Matrix

| Device | OS Version | Screen Size | Beta Tested? | Install OK? | Launch OK? | Core Flows OK? | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| [Flagship iOS, e.g. iPhone 17 Pro] | [iOS 26.1] | [6.3"] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| [Small iOS, e.g. iPhone 16e] | [iOS 26.0] | [6.1"] | [ ] | [ ] | [ ] | [ ] | [ ] | [Notch layout] |
| [Min iOS device, e.g. iPhone 13] | [iOS 17.x] | [6.1"] | [ ] | [ ] | [ ] | [ ] | [ ] | [Min supported] |
| [Flagship Android, e.g. Pixel 10 Pro] | [Android 16] | [6.3"] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| [Mid-range Android, e.g. Galaxy A56] | [Android 15] | [6.7"] | [ ] | [ ] | [ ] | [ ] | [ ] | |
| [Min Android device, e.g. Pixel 7a] | [Android 13] | [6.1"] | [ ] | [ ] | [ ] | [ ] | [ ] | [Min supported] |
| [Tablet, e.g. iPad Air M3] | [iPadOS 26] | [11.0"] | [ ] | [ ] | [ ] | [ ] | [ ] | [Tablet] |

#### Device Coverage Checklist

- [ ] Latest flagship devices tested (iOS + Android)
- [ ] Mid-range devices tested (where most of the install base usually is)
- [ ] Minimum supported OS version tested on real hardware
- [ ] Small screen devices tested
- [ ] Tablet / large screen tested if the app supports them
- [ ] Notch / Dynamic Island layouts verified
- [ ] Landscape and portrait orientations tested

### 4. OS Version Compatibility

| OS Version | Platform | App Installs? | App Launches? | No Crashes? | New Features Work? | Status | Notes |
|---|---|---|---|---|---|---|---|
| [Latest + beta, e.g. iOS 26.x] | iOS | [ ] | [ ] | [ ] | [ ] | [ ] | [Current + beta OS] |
| [Min supported, e.g. iOS 17.0] | iOS | [ ] | [ ] | [ ] | [ ] | [ ] | [Min iOS] |
| [Latest, e.g. Android 16] | Android | [ ] | [ ] | [ ] | [ ] | [ ] | [Current + beta OS] |
| [Previous, e.g. Android 15] | Android | [ ] | [ ] | [ ] | [ ] | [ ] | |
| [Min supported, e.g. Android 13] | Android | [ ] | [ ] | [ ] | [ ] | [ ] | [Min Android] |

### 5. Beta Feedback Collection

| Feedback ID | Tester | Device | OS | Category | Description | Severity | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| FB-001 | [Tester name] | [Device] | [OS] | [UI / Crash / Performance / Feature] | [What they reported] | [Low-Med-High-Crit] | [ ] | |
| FB-002 | | | | | | | [ ] | |
| FB-003 | | | | | | | [ ] | |

#### Feedback Collection Checklist

- [ ] In-app feedback mechanism available (shake-to-report or settings entry point)
- [ ] External feedback channel established (form, email alias or board)
- [ ] Feedback categorized by type (UI, crash, performance, feature, other)
- [ ] Every item triaged with severity and owner within an agreed SLA
- [ ] Critical items resolved or explicitly deferred before production
- [ ] Reporters acknowledged — testers who feel ignored stop reporting

### 6. Crash Monitoring

| Platform | Tool | Crash-Free Sessions | Crash-Free Users | Top Crash | Affected Users | Status | Notes |
|---|---|---|---|---|---|---|---|
| **iOS** | [Crashlytics / Sentry] | [X%] | [X%] | [Crash signature] | [N] | [ ] | |
| **Android** | [Crashlytics / Sentry] | [X%] | [X%] | [Crash signature] | [N] | [ ] | [Include ANRs] |
| **Combined** | [Tool] | [X%] | [X%] | [Crash signature] | [N] | [ ] | |

#### Crash Monitoring Checklist

- [ ] Crash reporting SDK integrated and reporting from the beta build
- [ ] Crash-free session rate above the agreed threshold (99.5%+ is a sane default)
- [ ] No new critical crashes introduced by this build
- [ ] Top crashes investigated and resolved or explicitly deferred
- [ ] ANR rate monitored on Android, not just hard crashes
- [ ] Symbol files / dSYMs uploaded for crash deobfuscation
- [ ] Crash alerts wired to someone who will actually read them

### 7. Staged Rollout Plan

| Stage | Platform | Percentage | Duration | Criteria to Proceed | Status | Notes |
|---|---|---|---|---|---|---|
| **Stage 1** | Android | [5%] | [24 hrs] | [No critical crashes, crash-free > 99.5%] | [ ] | |
| **Stage 2** | Android | [20%] | [48 hrs] | [No new critical issues, feedback stable] | [ ] | |
| **Stage 3** | Android | [50%] | [48 hrs] | [Stable, no regression] | [ ] | |
| **Stage 4** | Android | [100%] | [Ongoing] | [All clear] | [ ] | [Full release] |
| **Phased release** | iOS | [7-day phased] | [7 days] | [Apple automatic phased rollout] | [ ] | [Cannot pause mid-phase — halt the release instead] |
| **Production** | Both | [100%] | [Ongoing] | [All gates passed] | [ ] | |

#### Rollout Checklist

- [ ] Rollout percentage configurable per stage in Play Console
- [ ] iOS phased release toggled on in App Store Connect before submission
- [ ] Rollback or halt plan documented (Play Console can halt a rollout; App Store can pause a phased release — know which lever you have)
- [ ] Monitoring dashboards open during each stage, not checked afterwards
- [ ] Named owner who can pause the rollout outside business hours
- [ ] Production release confirmed only after the full rollout completes

### 8. Beta to Production Release Gates

| Gate | Criteria | Met? | Status | Notes |
|---|---|---|---|---|
| **Crash-free rate** | [> 99.5% sessions] | [ ] | [ ] | |
| **No critical bugs** | [0 open critical bugs] | [ ] | [ ] | |
| **Device coverage** | [All priority devices tested] | [ ] | [ ] | |
| **OS compatibility** | [Min to latest OS tested] | [ ] | [ ] | |
| **Beta feedback** | [All high-severity addressed] | [ ] | [ ] | |
| **Performance** | [No regression vs previous build] | [ ] | [ ] | |
| **Store assets** | [Screenshots and listing current] | [ ] | [ ] | |
| **Release notes** | [Written and reviewed] | [ ] | [ ] | |
| **Rollback plan** | [Documented and verified] | [ ] | [ ] | |

### 9. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | [Name] | [YYYY-MM-DD] | [Approved for production] |
| **Mobile Lead** | [Name] | [YYYY-MM-DD] | [Build verified] |
| **Product Manager** | [Name] | [YYYY-MM-DD] | [Release approved] |
| **DevOps / Release Lead** | [Name] | [YYYY-MM-DD] | [Rollout plan confirmed] |

### Negative Scenarios and Boundary Examples

Beta-specific edge cases the team should walk through before shipping:

| Negative Scenario | Input / Boundary | Expected Result | Automation Note |
|---|---|---|---|
| Expired TestFlight build | Tester installs after the 90-day expiry | App warns or fails cleanly; team notified to push a new build | Manual check of expiry date |
| Broken public link | Open beta link shared before track is active | Landing shows "beta not available", not a dead page | Manual smoke test |
| Build pushed to wrong track | Internal build uploaded to Open beta | Upload rejected or caught in review before exposure | fastlane lane per track |
| Permission denied mid-flow | Camera / location denied during core flow | Feature degrades with rationale, no crash | Appium |
| Rotation during transaction | Portrait to landscape mid-checkout | State preserved; no data loss | Appium |
| Upgrade with stale data | Beta installed over previous beta with cached data | Migration runs; no crash on first launch | Appium + seeded device |
| Airplane mode on launch | Network disabled at first open | Offline state or cached content shown gracefully | Appium |
