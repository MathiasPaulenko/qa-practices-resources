"""HilRig — Abstraction for a HIL test rig (dSPACE, NI, OPAL-RT).

This is a reference implementation. In production, replace the stub
methods with calls to your vendor's API (dSPACE ConfigurationDesk,
NI VeriStand, OPAL-RT RT-LAB).
"""

import os
import logging

logger = logging.getLogger(__name__)


class HilRig:
    """Wraps the real-time simulator and signal conditioning hardware."""

    def __init__(self, simulator: str = None):
        self.simulator_url = simulator or os.environ.get(
            "HIL_SIMULATOR_URL", "dspace://hil-rig-01"
        )
        self._connected = False
        self._faults_active = set()

    def connect(self):
        """Connect to the HIL simulator."""
        logger.info("Connecting to HIL simulator: %s", self.simulator_url)
        self._connected = True

    def set_motor_current(self, current: float):
        """Set the simulated motor current in amps."""
        if not self._connected:
            raise RuntimeError("Rig not connected")
        logger.info("Setting motor current to %.1f A", current)

    def inject_fault(self, fault_name: str):
        """Inject a fault (e.g. 'phase_current_short_to_ground')."""
        if not self._connected:
            raise RuntimeError("Rig not connected")
        logger.info("Injecting fault: %s", fault_name)
        self._faults_active.add(fault_name)

    def clear_faults(self):
        """Clear all injected faults."""
        logger.info("Clearing faults: %s", self._faults_active)
        self._faults_active.clear()

    def reset_faults(self):
        """Reset all faults to known-good state."""
        self.clear_faults()

    def health_check(self) -> bool:
        """Verify the rig is ready for testing."""
        if not self._connected:
            return False
        logger.info("Rig health check passed")
        return True

    def shutdown(self):
        """Safely shut down the rig."""
        if self._faults_active:
            self.clear_faults()
        self._connected = False
        logger.info("HIL rig shut down")
