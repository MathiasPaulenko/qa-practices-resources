"""Mini-app simulating a deployed service for release-testing smoke checks.

Environment knobs let you replay the edge cases from the guide:
  APP_ENV              staging | production   (default: production)
  CACHE_UP             0 | 1                   (dependency failure)
  PENDING_MIGRATIONS   int                     (default: 0)
  ARTIFACT_SHA / EXPECTED_SHA                  (checksum mismatch)
  FF_PAYMENTS          0 | 1                   (flag parity)
  DEPLOY_STARTED_AT    unix ts                 (rollback window edge)
"""

import os
import time

from flask import Flask, jsonify

app = Flask(__name__)

ROLLBACK_WINDOW_SECONDS = 30 * 60

APP_ENV = os.environ.get("APP_ENV", "production")
CACHE_UP = os.environ.get("CACHE_UP", "1") == "1"
PENDING_MIGRATIONS = int(os.environ.get("PENDING_MIGRATIONS", "0"))
ARTIFACT_SHA = os.environ.get("ARTIFACT_SHA", "a1b2c3")
EXPECTED_SHA = os.environ.get("EXPECTED_SHA", "a1b2c3")
FF_PAYMENTS = os.environ.get("FF_PAYMENTS", "1") == "1"
DEPLOY_STARTED = float(os.environ.get("DEPLOY_STARTED_AT", time.time()))


@app.get("/health")
def health():
    deps = {
        "database": "up",
        "cache": "up" if CACHE_UP else "down",
    }
    healthy = all(v == "up" for v in deps.values())
    body = {"status": "ok" if healthy else "degraded", "dependencies": deps}
    return jsonify(body), (200 if healthy else 503)


@app.get("/meta/environment")
def environment():
    return jsonify(env=APP_ENV, pending_migrations=PENDING_MIGRATIONS)


@app.get("/meta/artifact")
def artifact():
    return jsonify(deployed_sha=ARTIFACT_SHA, expected_sha=EXPECTED_SHA)


@app.get("/meta/flags")
def flags():
    return jsonify(payments=FF_PAYMENTS)


@app.post("/deploy/rollback")
def rollback():
    if time.time() - DEPLOY_STARTED > ROLLBACK_WINDOW_SECONDS:
        return jsonify(error="rollback window expired", incident_required=True), 409
    return jsonify(status="rolled back")


if __name__ == "__main__":
    app.run(port=5000)
