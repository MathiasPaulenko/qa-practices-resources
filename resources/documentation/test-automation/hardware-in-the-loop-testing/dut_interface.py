"""DutInterface — CAN bus interface to the Device Under Test.

Uses python-can to communicate with the embedded controller.
Install: pip install python-can
"""

import os
import logging

logger = logging.getLogger(__name__)


class DutInterface:
    """Talks to the DUT over CAN bus."""

    def __init__(self, can_bus: str = None, node_id: int = None):
        self.can_bus = can_bus or os.environ.get("HIL_CAN_BUS", "vcan0")
        self.node_id = node_id or int(os.environ.get("HIL_DUT_NODE_ID", "0x12"), 0)
        self._motor_enabled = True
        self._fault_code = 0x00

    def connect(self):
        """Initialize the CAN bus interface."""
        logger.info("Connecting to CAN bus %s, node ID 0x%02X", self.can_bus, self.node_id)

    @property
    def motor_enabled(self) -> bool:
        """Read the motor enable state from the DUT."""
        return self._motor_enabled

    @property
    def fault_code(self) -> int:
        """Read the current fault code from the DUT."""
        return self._fault_code

    def set_fault_state(self, fault_code: int):
        """Simulate a fault code received from the DUT."""
        self._fault_code = fault_code
        if fault_code != 0x00:
            self._motor_enabled = False

    def clear_fault_state(self):
        """Clear the fault state on the DUT."""
        self._fault_code = 0x00
        self._motor_enabled = True

    def disconnect(self):
        """Close the CAN bus interface."""
        logger.info("Disconnecting from CAN bus %s", self.can_bus)
