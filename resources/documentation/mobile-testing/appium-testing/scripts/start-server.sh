#!/usr/bin/env bash
# Start Appium 2.0 and verify it is listening on /wd/hub/status.
set -euo pipefail
appium --base-path /wd/hub &
sleep 4
curl -s http://127.0.0.1:4723/wd/hub/status | grep -q "ready" && echo "Appium server UP" || echo "Server failed to start"
