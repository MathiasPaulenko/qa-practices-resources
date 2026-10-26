"""Decide whether a desktop app should fetch an update.

Mirrors the semver comparison logic from the Desktop App Auto-Update
Testing Checklist. Requires: pip install packaging
"""

from packaging import version


def should_update(current: str, available: str, minimum: str) -> str:
    """Return 'force', 'available', or 'none' for an update decision."""
    if version.parse(current) < version.parse(minimum):
        return "force"
    if version.parse(available) > version.parse(current):
        return "available"
    return "none"


if __name__ == "__main__":
    assert should_update("2.3.0", "2.4.1", "2.2.0") == "available"
    assert should_update("2.1.0", "2.4.1", "2.3.0") == "force"
    assert should_update("2.4.1", "2.4.1", "2.3.0") == "none"
    print("All version-check assertions passed")
