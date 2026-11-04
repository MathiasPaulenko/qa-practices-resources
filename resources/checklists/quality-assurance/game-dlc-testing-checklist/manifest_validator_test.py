"""DLC manifest validator — catches the config bugs that ship broken DLC.

Run: pytest manifest_validator_test.py -v
"""
import json
import re
from pathlib import Path

import pytest

KNOWN_PLATFORMS = {"PC", "PS5", "XSX", "Switch", "iOS", "Android", "Cloud"}
KNOWN_REGIONS = {"US", "EU", "JP", "KR", "BR", "AU", "GLOBAL"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

MANIFEST_PATH = Path(__file__).parent / "dlc-manifest.json"


@pytest.fixture
def manifest():
    return json.loads(MANIFEST_PATH.read_text())


def test_required_fields(manifest):
    for key in ("dlcId", "title", "requiredBaseVersion", "platforms", "regions", "dependencies"):
        assert key in manifest, f"missing field: {key}"


def test_version_format(manifest):
    assert SEMVER.match(manifest["requiredBaseVersion"]), \
        f"requiredBaseVersion '{manifest['requiredBaseVersion']}' is not semver"


def test_platforms_are_known(manifest):
    unknown = set(manifest["platforms"]) - KNOWN_PLATFORMS
    assert not unknown, f"unknown platforms: {unknown}"


def test_regions_are_known(manifest):
    unknown = set(manifest["regions"]) - KNOWN_REGIONS
    assert not unknown, f"unknown regions: {unknown}"


def test_no_self_dependency(manifest):
    assert manifest["dlcId"] not in manifest["dependencies"]


def test_exclusivity_disjoint(manifest):
    assert set(manifest["exclusiveWith"]).isdisjoint(manifest["platforms"])
    assert set(manifest["exclusiveWith"]).isdisjoint({manifest["dlcId"]})


def test_manifest_is_not_empty(manifest):
    assert manifest["platforms"], "a DLC must target at least one platform"
    assert manifest["regions"], "a DLC must target at least one region"
