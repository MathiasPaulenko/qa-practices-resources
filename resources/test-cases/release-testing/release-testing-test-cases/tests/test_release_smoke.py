"""Runnable cut of the release-testing suite from the QAPractices guide.

Covers RT-SM-03/04, RT-ENV-01/04 and the release-specific edge cases:
wrong-environment guard, flag parity, checksum mismatch, expired
rollback window. Uses Flask's test client — no server needed.
"""

import importlib
import os
import time

import pytest

import app as app_module


def make_client(**env):
    for key, value in env.items():
        os.environ[key] = str(value)
    importlib.reload(app_module)
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


@pytest.fixture()
def client():
    return make_client(APP_ENV="production", CACHE_UP="1")


# --- RT-ENV-01 + edge: the suite must refuse a non-production target --------


def test_environment_reports_production(client):
    env = client.get("/meta/environment").get_json()["env"]
    assert env == "production", (
        f"refusing to smoke-test a {env} deployment as a release target"
    )


def test_environment_guard_flags_staging():
    staging_client = make_client(APP_ENV="staging")
    env = staging_client.get("/meta/environment").get_json()["env"]
    assert env == "staging"  # a real gate would abort here, before any check


# --- RT-SM-03 / RT-SM-04: health and dependencies ----------------------------


def test_health_endpoint_200_and_fast(client):
    start = time.monotonic()
    response = client.get("/health")
    elapsed = time.monotonic() - start
    assert response.status_code == 200
    assert elapsed < 0.5  # RT-SM-03 timing gate
    deps = response.get_json()["dependencies"]
    assert deps and all(v == "up" for v in deps.values())


def test_health_degrades_when_a_dependency_is_down():
    broken = make_client(APP_ENV="production", CACHE_UP="0")
    response = broken.get("/health")
    assert response.status_code == 503
    assert response.get_json()["dependencies"]["cache"] == "down"


# --- RT-ENV-04 + edges: migrations, checksum, flags --------------------------


def test_no_pending_migrations(client):
    meta = client.get("/meta/environment").get_json()
    assert meta["pending_migrations"] == 0


def test_pending_migrations_are_detected():
    dirty = make_client(APP_ENV="production", PENDING_MIGRATIONS="2")
    meta = dirty.get("/meta/environment").get_json()
    assert meta["pending_migrations"] == 2  # release must be blocked/flagged


def test_artifact_checksum_matches_build(client):
    meta = client.get("/meta/artifact").get_json()
    assert meta["deployed_sha"] == meta["expected_sha"]


def test_checksum_mismatch_is_detected():
    tampered = make_client(APP_ENV="production", ARTIFACT_SHA="deadbee")
    meta = tampered.get("/meta/artifact").get_json()
    assert meta["deployed_sha"] != meta["expected_sha"]  # deploy must halt


# --- RT-DEP-01 edge: rollback window -----------------------------------------


def test_rollback_allowed_inside_window(client):
    response = client.post("/deploy/rollback")
    assert response.status_code == 200
    assert response.get_json()["status"] == "rolled back"


def test_rollback_rejected_past_window():
    old = make_client(
        APP_ENV="production", DEPLOY_STARTED_AT=str(time.time() - 3600)
    )
    response = old.post("/deploy/rollback")
    assert response.status_code == 409
    assert response.get_json()["incident_required"] is True
