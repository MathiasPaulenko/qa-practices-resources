#!/usr/bin/env bash
# Deep link verification commands for the Mobile Deep Link Testing Matrix.
# Replace the domain, package and URI scheme with your app's real values.

PACKAGE="com.shoply.app"
URL="https://shop.example.io/product/123"

# Fire a VIEW intent — lands in the app if the domain is verified,
# in the browser or a chooser dialog if it is not.
adb shell am start -a android.intent.action.VIEW -d "$URL" "$PACKAGE"

# Check the domain verification state granted by autoVerify.
# "always" = verified app link; anything else = chooser dialog.
adb shell pm get-app-links "$PACKAGE"

# Dump the system-level preferred-apps table when verification
# keeps failing and you suspect a stale decision.
adb shell dumpsys package domain-preferred-apps

# Open a universal link in the iOS Simulator.
# If it lands in Safari instead of the app, the AASA file or
# the associated-domain entitlement is the culprit.
xcrun simctl openurl booted "$URL"

# Verify the AASA file is served correctly (must be application/json,
# at the domain root or under /.well-known/).
curl -I "https://shop.example.io/.well-known/apple-app-site-association"

# Verify assetlinks.json is reachable where Android expects it.
curl -I "https://shop.example.io/.well-known/assetlinks.json"
