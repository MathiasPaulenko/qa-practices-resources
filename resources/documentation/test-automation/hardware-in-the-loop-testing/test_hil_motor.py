"""HIL test: overcurrent protection with fault injection.

This is the test from the HIL Testing Guide. It verifies that the
motor controller disables the motor and sets the correct fault code
when a phase-current short-to-ground fault is injected.

Requirements:
- A running HIL rig (dSPACE, NI PXI or OPAL-RT)
- A DUT (motor controller) flashed with the firmware under test
- CAN bus connectivity between the test runner and the DUT
"""

import pytest
import time

from conftest import rig  # noqa: F401 — pytest fixture


def test_overcurrent_protection(rig):
    """Motor must disable and set fault code 0x05 on short-to-ground."""
    hil, dut = rig

    # Start with normal current — motor should be enabled
    hil.set_motor_current(10.0)
    assert dut.motor_enabled is True

    # Inject short-to-ground fault and push current above threshold
    hil.inject_fault("phase_current_short_to_ground")
    hil.set_motor_current(55.0)
    time.sleep(0.05)  # 50ms — long enough for the diagnostic to react

    # Motor must be disabled and fault code must be 0x05
    assert dut.motor_enabled is False, "Motor should be disabled after overcurrent fault"
    assert dut.fault_code == 0x05, f"Expected fault code 0x05, got 0x{dut.fault_code:02X}"

    # Clear faults — motor should re-enable
    hil.clear_faults()
    dut.clear_fault_state()
    assert dut.motor_enabled is True, "Motor should re-enable after clearing faults"


def test_normal_operation_no_fault(rig):
    """Motor stays enabled under normal current with no faults."""
    hil, dut = rig

    hil.set_motor_current(8.0)
    assert dut.motor_enabled is True
    assert dut.fault_code == 0x00


def test_sensor_drift_does_not_trigger_overcurrent(rig):
    """A 5% sensor drift must not false-trigger the overcurrent protection."""
    hil, dut = rig

    hil.set_motor_current(10.0)
    assert dut.motor_enabled is True

    # Simulate 5% drift — within tolerance, should not trip
    hil.set_motor_current(10.5)
    time.sleep(0.1)
    assert dut.motor_enabled is True, "5% drift should not trigger overcurrent"
    assert dut.fault_code == 0x00
