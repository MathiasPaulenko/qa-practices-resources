#!/usr/bin/env bash
# Install Appium 2.0 platform drivers and verify the environment.
set -euo pipefail
appium driver install xcuitest        # iOS
appium driver install uiautomator2    # Android
appium plugin install element-wait || true
appium doctor
echo "Drivers installed. Start the server with scripts/start-server.sh"
