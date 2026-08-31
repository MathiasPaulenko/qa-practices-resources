"""pytest fixtures for HIL testing.

Provides the `rig` fixture that yields a (HilRig, DutInterface) pair
with automatic setup and teardown.
"""

import pytest

from hil_rig import HilRig
from dut_interface import DutInterface


@pytest.fixture
def rig():
    """Yield a (HilRig, DutInterface) pair with automatic cleanup."""
    hil = HilRig()
    dut = DutInterface()

    hil.connect()
    dut.connect()

    # Rig health check before every run
    if not hil.health_check():
        pytest.skip("HIL rig health check failed — skipping test")

    yield hil, dut

    hil.reset_faults()
    dut.clear_fault_state()
    dut.disconnect()
    hil.shutdown()
