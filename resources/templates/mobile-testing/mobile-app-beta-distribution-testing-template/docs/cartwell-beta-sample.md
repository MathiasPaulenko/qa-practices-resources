# CartWell Shopper 4.2.0 — Beta Distribution (completed sample)

Filled example for a two-week external beta, both platforms.

### 1. Beta Details

| Field | Details |
|---|---|
| **App name** | CartWell Shopper |
| **Version / build** | 4.2.0 (build 240) |
| **Platform(s)** | Both |
| **iOS distribution** | TestFlight Internal + External |
| **Android distribution** | Play Console Internal + Closed |
| **Beta testers** | 40 internal / 320 external |
| **Beta duration** | 14 days |
| **Test lead** | Elena Vargas, QA Lead |
| **Test dates** | 2026-11-02 to 2026-11-16 |

### 2. Beta Track Configuration

| Platform | Track | Tester Group | Build Available | Install Works | Status | Notes |
|---|---|---|---|---|---|---|
| **iOS** | TestFlight Internal | Engineering + QA | [x] | [x] | Done | Same-day feedback loop |
| **iOS** | TestFlight External | Beta cohort opt-ins | [x] | [x] | Done | Passed Beta App Review in 26h |
| **Android** | Play Console Internal | Engineering + QA | [x] | [x] | Done | |
| **Android** | Play Console Closed | Beta Google Group | [x] | [x] | Done | 3 stale emails removed |
| **Android** | Play Console Open | — | [ ] | [ ] | Skipped | Open beta deferred to v4.3 |

### 3. Device Coverage Matrix

| Device | OS Version | Screen Size | Beta Tested? | Install OK? | Launch OK? | Core Flows OK? | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| **iPhone 17 Pro** | iOS 26.1 | 6.3" | [x] | [x] | [x] | [x] | Pass | |
| **iPhone 16e** | iOS 26.0 | 6.1" | [x] | [x] | [x] | [x] | Pass | Button overlap fixed in 241 |
| **iPhone 13** | iOS 17.7 | 6.1" | [x] | [x] | [x] | [x] | Pass | Min supported iOS |
| **Pixel 10 Pro** | Android 16 | 6.3" | [x] | [x] | [x] | [x] | Pass | |
| **Galaxy A56** | Android 15 | 6.7" | [x] | [x] | [x] | [x] | Pass | Scroll lag on list view (FB-003) |
| **Pixel 7a** | Android 13 | 6.1" | [x] | [x] | [x] | [x] | Pass | Min supported Android |
| **iPad Air M3** | iPadOS 26.1 | 11.0" | [x] | [x] | [x] | [x] | Pass | |

### 4. OS Version Compatibility

| OS Version | Platform | App Installs? | App Launches? | No Crashes? | New Features Work? | Status | Notes |
|---|---|---|---|---|---|---|---|
| **iOS 26.1** | iOS | [x] | [x] | [x] | [x] | Pass | |
| **iOS 17.7** | iOS | [x] | [x] | [x] | [x] | Pass | Min supported |
| **Android 16** | Android | [x] | [x] | [x] | [x] | Pass | |
| **Android 13** | Android | [x] | [x] | [x] | [x] | Pass | Min supported |

### 5. Beta Feedback Collection

| Feedback ID | Tester | Device | OS | Category | Description | Severity | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| FB-001 | Sarah Johnson | iPhone 16e | iOS 26.0 | UI | Address button overlapped on small screen | Medium | Fixed | Shipped in build 241 |
| FB-002 | Elena Vargas | Pixel 10 Pro | Android 16 | Crash | Crash on profile after upgrade from 4.1.3 | Critical | Fixed | Stale cached session; migration added |
| FB-003 | Ravi Iyer | Galaxy A56 | Android 15 | Performance | Scroll lag on address list | Medium | Deferred | Acceptable; tracked for v4.3 |
| FB-004 | Ana Gómez | iPhone 13 | iOS 17.7 | UI | Truncated CTA text in Spanish locale | Low | Fixed | Shipped in build 241 |

### 6. Crash Monitoring

| Platform | Tool | Crash-Free Sessions | Crash-Free Users | Top Crash | Affected Users | Status | Notes |
|---|---|---|---|---|---|---|---|
| **iOS** | Firebase Crashlytics | 99.8% | 99.9% | CheckoutViewModel address parse | 3 | Pass | Resolved in build 241 |
| **Android** | Firebase Crashlytics | 99.6% | 99.7% | ProfileActivity stale session NPE | 9 | Pass | FB-002, resolved in 241 |
| **Combined** | Crashlytics | 99.7% | 99.8% | — | 12 | Pass | ANR rate 0.04%, under 0.1% bar |

### 7. Staged Rollout Plan

| Stage | Platform | Percentage | Duration | Criteria to Proceed | Status | Notes |
|---|---|---|---|---|---|---|
| **Stage 1** | Android | 5% | 24 hrs | No critical crashes, crash-free > 99.5% | Done | Held 36h after FB-002; resumed once fixed |
| **Stage 2** | Android | 20% | 48 hrs | No new critical issues, feedback stable | Done | |
| **Stage 3** | Android | 50% | 48 hrs | Stable, no regression | Done | |
| **Stage 4** | Android | 100% | Ongoing | All clear | Done | Full release 2026-11-18 |
| **Phased release** | iOS | 7-day phased | 7 days | Apple automatic phased rollout | Done | No halt needed |
| **Production** | Both | 100% | Ongoing | All gates passed | Done | |

### 8. Beta to Production Release Gates

| Gate | Criteria | Met? | Status | Notes |
|---|---|---|---|---|
| **Crash-free rate** | > 99.5% sessions | [x] | Pass | 99.7% combined |
| **No critical bugs** | 0 open critical bugs | [x] | Pass | FB-002 closed in build 241 |
| **Device coverage** | All priority devices tested | [x] | Pass | 10/10 devices |
| **OS compatibility** | Min to latest OS tested | [x] | Pass | |
| **Beta feedback** | All high-severity addressed | [x] | Pass | FB-003 deferred with PM sign-off |
| **Performance** | No regression vs 4.1.x | [x] | Pass | Cold start within 40ms of previous |
| **Store assets** | Screenshots and listing current | [x] | Pass | New checkout screenshots uploaded |
| **Release notes** | Written and reviewed | [x] | Pass | |
| **Rollback plan** | Documented and verified | [x] | Pass | Play Console halt tested; iOS would pause phased release |

### 9. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| **QA Lead** | Elena Vargas | 2026-11-16 | Approved for production |
| **Mobile Lead** | Dimitri Sokolov | 2026-11-16 | Build verified |
| **Product Manager** | Jin-ho Park | 2026-11-17 | Release approved |
| **DevOps / Release Lead** | Leila Haddad | 2026-11-17 | Rollout plan confirmed |
