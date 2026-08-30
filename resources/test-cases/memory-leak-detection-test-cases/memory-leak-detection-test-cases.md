
# Memory Leak Detection Test Cases

## Overview

I once spent two days chasing a leak in a Node.js service. The culprit was a single closure inside a `setInterval` that kept a reference to a 50 MB cache. Leaks don't crash an app outright; they eat memory bit by bit until the system slows, hangs or gets killed by the OS.

**What are these test cases?** I built them as a reusable, step-by-step suite I run before any release where memory could be a problem. They help detect, isolate and prove leaks in web frontends, backend services and mobile apps. The cases cover web frontends, backend services and mobile apps using Chrome DevTools, `process.memoryUsage()`, `heapdump`, Valgrind and Xcode Instruments. Each case includes preconditions, test data, steps, expected results and a priority.

![Memory leak detection workflow: establish baseline, apply workload, capture snapshot, compare and analyze, isolate root cause, fix and verify in CI](/assets/images/diagrams/memory-leak-detection-flow.svg)

For broader performance coverage, see the [Performance Testing Guide](/documentation/performance-testing-guide) and the [Load Testing with k6 Guide](/documentation/load-testing-with-k6).

## When to Use

- **Major releases:** I always run these cases when a new feature, dependency upgrade or framework change ships, because those are the changes most likely to introduce a leak.
- **After dependency updates:** a newer library version can retain objects longer than the one before. I once traced a leak to a patch bump in a logging library.
- **During endurance testing:** if a service runs for 24+ hours, I expect its memory graph to stay flat. A slow climb is the signature of a leak.
- **Post-incident validation:** after a memory-related outage, I rerun the exact case that reproduced it before declaring the fix done.
- **Regression prevention:** I keep automated memory checks in CI so a failing build stops a leak before it reaches production.
- **Mobile app releases:** iOS and Android terminate apps that cross system memory limits. A 10-minute real-device run has saved us more than once.

## Test Cases

### Edge Cases and Boundary Values

These are the boundary conditions I keep in a separate checklist because they are the ones that usually catch leaks that normal functional tests miss.

| Scenario | Input | Boundary / Edge Type | Expected Result | Automation Note | Priority |
|---|---|---|---|---|---|
| Force garbage collection before snapshot | `global.gc()` or `--expose-gc` flag | GC baseline boundary | Snapshot reflects retained objects, not transient garbage | Node.js / Chrome flag | High |
| Run workload with zero iterations | 0 repeated actions | Lower boundary | Baseline memory is captured with no growth | Manual or automated baseline | Medium |
| Run workload at declared max capacity | 1,000 iterations or peak VU count | Upper boundary | Memory growth stays below the threshold (e.g., < 10%) | k6 / Playwright | High |
| Snapshot after component mount/unmount cycles | 100 mount/unmount cycles | Lifecycle boundary | Listener and DOM counts return to baseline | Playwright + DevTools | High |
| Heap comparison across library versions | Old version vs new version | Version boundary | New version doesn't retain extra objects from the same workload | Manual diff | Medium |

### TC-001: Capture a Baseline Heap Snapshot

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-001 | Capture a baseline heap snapshot | Application freshly started; no active user sessions | N/A | 1. Start the app in production mode.<br>2. Open DevTools Memory tab or run `node --heapsnapshot-near-heap-limit=1`.<br>3. Force GC and capture a snapshot.<br>4. Record total heap size. | Heap size is within the documented baseline range for the environment. | Manual / Chrome DevTools | High |

### TC-002: Detect DOM Node Accumulation in an SPA

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-002 | Detect detached DOM node accumulation | SPA with route transitions; DevTools open | 50 route transitions between `/list` and `/detail` | 1. Take a baseline snapshot at `/list`.<br>2. Navigate to `/detail` and back 50 times.<br>3. Force GC and take a second snapshot.<br>4. Compare heap size and detached DOM nodes. | Heap size difference is < 10% of baseline. No detached DOM nodes retained. | Playwright + Chrome DevTools | High |

### TC-003: Validate Memory Stability Over a Long Session

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-003 | Validate 4-hour memory stability | User authenticated; background tasks running | Realistic session with actions every 5 minutes | 1. Log in and record initial heap size.<br>2. Perform user actions every 5 minutes for 4 hours.<br>3. Record final heap size and calculate growth rate. | Memory growth rate is < 5 MB/hour. No `OutOfMemory` errors in logs. | k6 / Manual endurance test | High |

### TC-004: Verify Event Listeners Are Removed on Unmount

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-004 | Verify event listener cleanup | Component with event listeners; DevTools open | 100 mount and unmount cycles | 1. Record active event listener count at baseline.<br>2. Mount and unmount the component 100 times.<br>3. Force GC and compare listener count. | Active event listener count returns to baseline after unmounting. | React DevTools / Playwright | High |

### TC-005: Detect Backend Heap Growth Under Sustained Load

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-005 | Detect backend heap growth | API service running; load generator available | 1,000 requests over 30 minutes | 1. Record baseline `heapUsed` via `process.memoryUsage()`.<br>2. Send sustained load for 30 minutes.<br>3. Force GC and record final `heapUsed`. | Heap growth is < 20% of baseline. No object category grows > 50%. | k6 + Node.js heap dump | High |

### TC-006: Validate Mobile App Memory Returns to Baseline

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-006 | Validate mobile app memory recovery | Physical iOS or Android device; app installed | 10 minutes of typical user flow | 1. Launch app and record baseline memory.<br>2. Complete a typical user flow.<br>3. Return to the home screen and wait 60 seconds.<br>4. Record final memory. | Memory returns to near baseline. OS doesn't terminate the app. | Xcode Instruments / Android Profiler | High |

### TC-007: Isolate a Leak to a Specific Library Version

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-007 | Isolate a library version leak | Two builds: old library version and new version | Identical workload for both versions | 1. Run the same workload on the old version for 1 hour.<br>2. Capture a heap dump.<br>3. Repeat on the new version.<br>4. Compare retention graphs. | New version doesn't retain extra library objects that the old version frees. | `heapdump` / Valgrind | Medium |

### TC-008: Fail CI Build on Memory Regression

| Test Case ID | Scenario | Preconditions | Test Data | Steps | Expected Result | Automation Notes | Priority |
|---|---|---|---|---|---|---|---|
| TC-008 | Fail CI build on memory regression | CI pipeline can run headless browser or API tests | Baseline from previous green build | 1. Run a standardized workload in CI.<br>2. Capture `process.memoryUsage().heapUsed` or `performance.measureUserAgentSpecificMemory()`.<br>3. Compare against the previous baseline.<br>4. Fail if growth exceeds 10%. | Build passes when memory is stable; fails with a descriptive message when it exceeds the threshold. | GitHub Actions / Playwright | High |

## Best Practices

1. Always force garbage collection before taking a heap snapshot. Otherwise you measure transient objects, not real leaks.
2. Profile production builds, not development builds with hot reload and source maps. Dev builds inflate memory and hide the real pattern.
3. Test with production-like data. Small datasets hide retention problems; I load at least 10,000 realistic records before I trust a snapshot.
4. Focus on detached DOM nodes in SPAs and closures in long-running services. Those two patterns account for most leaks I have found.
5. Monitor RSS, external and heap memory in Node.js. A buffer leak may not show in the heap, but it will show in RSS.
6. Keep a known-good baseline in version control and compare against it in CI. Without a baseline you are just guessing.
7. Use real devices or emulators with identical OS versions when testing mobile apps. Memory handling differs between Android versions and iOS releases.

## Common Mistakes

1. Confusing intentional cache growth with an unbounded leak. A cache that stops at its limit is fine; a cache that grows forever is not.
2. Profiling development builds instead of production builds. Hot reload and source maps change the memory profile completely.
3. Ignoring closures and retained function references inside timers or streams. My two-day `setInterval` chase was exactly this.
4. Profiling only the main process in a microservice architecture. Worker processes and background queues leak just as often.
5. Taking snapshots without forcing garbage collection first. You end up chasing objects that would have been cleaned up anyway.
6. Relying only on manual testing and missing slow regressions. Leaks that grow 1 MB per hour are invisible in a 5-minute manual test.

## Related Resources

- [Performance Testing Guide](/documentation/performance-testing-guide)
- [Performance Testing Checklist](/checklists/performance-testing-checklist)
- [Load Testing with k6](/documentation/load-testing-with-k6)
- [Performance and Load Testing Test Cases](/test-cases/performance-load-testing-test-cases)
- [Performance Testing Topic Hub](/topics/performance-testing)

## Frequently Asked Questions

### What is the difference between memory growth and a memory leak?

Growth is bounded and expected. A cache filling to its configured limit is growth. A leak is unbounded: it keeps growing after the work finishes and the garbage collector has no path to reclaim it.

### Should I profile on a developer machine or in CI?

Both. I use local profiling for root-cause analysis and CI profiling to catch regressions automatically on every build. Local is fast for debugging; CI is the only way to stop regressions before they ship.

### Which tools should I use for Node.js memory leaks?

My usual stack is `--expose-gc` to force collection, `heapdump` for snapshots, `clinic.js` for diagnostics and `0x` for flame graphs. For native leaks I switch to Valgrind or AddressSanitizer, depending on whether the suspect code is C++ or a native add-on.

### How long should a memory leak test run?

Long enough to match the production session you care about. For backend services, 30 minutes to 4 hours is common; I start with 30 minutes and extend only if I see drift. For mobile apps, 10â€“30 minutes of real usage is usually enough because the OS kills the app quickly when memory climbs.
