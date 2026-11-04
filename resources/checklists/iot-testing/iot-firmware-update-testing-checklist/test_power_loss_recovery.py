"""Power-loss recovery test for OTA firmware updates.

Exercises the rollback path: start an update, cut power mid-flash,
restore power, and verify the device boots the previous firmware.
Swap the ota-client / power-* commands for your own harness.
"""

import subprocess

import pytest

DEVICE = "dev-001"
PREVIOUS_VERSION = "3.0.0"
TARGET_VERSION = "3.1.4"


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def get_version(device: str = DEVICE) -> str:
    out = subprocess.check_output(["ota-client", "version", device])
    return out.decode().strip()


@pytest.mark.parametrize("cut_stage", ["download", "flash", "boot"])
def test_power_loss_recovery(cut_stage: str) -> None:
    """Power cut at any stage must end in previous version or a clean resume."""
    run("ota-client", "start", "--device", DEVICE, "--to", TARGET_VERSION)
    run("power-cut", DEVICE, "--at", cut_stage)
    run("power-restore", DEVICE)

    version = get_version()
    assert version in {PREVIOUS_VERSION, TARGET_VERSION}, (
        f"device left in inconsistent state after power cut at {cut_stage}: {version}"
    )


def test_power_loss_during_flash_rolls_back() -> None:
    """A power cut mid-flash with failed health check must roll back."""
    run("ota-client", "start", "--device", DEVICE, "--to", TARGET_VERSION)
    run("power-cut", DEVICE, "--at", "flash")
    run("power-restore", DEVICE)

    assert get_version() == PREVIOUS_VERSION
