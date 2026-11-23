# Mobile Security Testing — Companion Kit

Companion scripts for the [Mobile Security Testing with OWASP MASVS](https://qapractices.com/documentation/mobile-security-testing/) guide on QAPractices.com. Everything here assumes you are testing an app you own or are authorized to test.

## Files

| File | What it does |
| --- | --- |
| `scripts/mobsf-scan.sh` | Starts MobSF 4.x in Docker on port 8000 so you can upload an APK or IPA for static analysis. |
| `scripts/decompile-apk.sh` | Decompiles an APK with apktool 2.9+ and lists the manifest and `network_security_config` for review. |
| `scripts/storage-audit.sh` | Walks `shared_prefs`, `files` and `databases` of a debuggable app via `adb shell run-as` and flags files that may hold tokens or PII. |
| `scripts/logcat-watch.sh` | Tails `adb logcat` and filters lines matching common leak patterns (tokens, passwords, Bearer headers). |
| `objection/session.txt` | Ordered objection 1.11.x command sequence for a runtime session: pinning bypass, root-detection bypass, storage enumeration. |
| `android/network_security_config.xml` | Debug-only config that trusts user-installed CAs so mitmproxy/ZAP can intercept traffic. Never ship it to release builds. |

## Requirements

- Android SDK Platform-Tools (`adb`), a rooted emulator or a debuggable build for `run-as` and objection
- Docker for `mobsf-scan.sh`; apktool 2.9+ for `decompile-apk.sh`
- mitmproxy 11.x or OWASP ZAP for traffic interception; objection 1.11.x for `objection/session.txt`

## Usage

```bash
# 1. Static scan — then open http://localhost:8000 and upload the APK
./scripts/mobsf-scan.sh

# 2. Decompile and inspect manifest + network security config
./scripts/decompile-apk.sh app-release.apk

# 3. Audit local storage on a debuggable build
./scripts/storage-audit.sh com.acme.banking

# 4. Watch logcat for token or credential leaks while you exercise login and payment flows
./scripts/logcat-watch.sh com.acme.banking

# 5. Runtime session — run the commands in objection/session.txt inside `explore`
objection -g com.acme.banking explore
```

Replace `com.acme.banking` with your package name. Only use these on builds and devices you are authorized to test.
