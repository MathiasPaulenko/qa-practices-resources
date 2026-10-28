#!/usr/bin/env bash
# Mobile smoke runner — usage: ./run-smoke-tests.sh [android|ios]
# Env vars: ANDROID_TEST_CLASS (default smoke), IOS_SCHEME, IOS_TEST_CLASS, IOS_DEVICE
set -euo pipefail

PLATFORM="${1:?usage: run-smoke-tests.sh [android|ios]}"
ANDROID_TEST_CLASS="${ANDROID_TEST_CLASS:-com.app.LoginSmokeTest}"
IOS_SCHEME="${IOS_SCHEME:-App-UITests}"
IOS_TEST_CLASS="${IOS_TEST_CLASS:-LoginSmokeTest}"
IOS_DEVICE="${IOS_DEVICE:-iPhone 15}"

case "$PLATFORM" in
  android)
    ./gradlew connectedDebugAndroidTest \
      "-Pandroid.testInstrumentationRunnerArguments.class=${ANDROID_TEST_CLASS}"
    ;;
  ios)
    xcodebuild test \
      -scheme "${IOS_SCHEME}" \
      -destination "platform=iOS Simulator,name=${IOS_DEVICE}" \
      -only-testing:"${IOS_SCHEME}/${IOS_TEST_CLASS}"
    ;;
  *)
    echo "unknown platform: $PLATFORM" >&2
    exit 2
    ;;
esac
