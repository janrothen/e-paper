#!/usr/bin/env python3

import os
import logging

MIN_PWM_VALUE: int = 0
MAX_PWM_VALUE: int = 255


from typing import Any

class GPIOService:
    """
    Service for controlling GPIO pins on Raspberry Pi using pigpio daemon.
    
    This service provides an abstraction layer for hardware interactions,
    specifically for controlling LED brightness through PWM (Pulse Width Modulation).
    Uses the pigpio library via shell commands to set PWM values on GPIO pins.
    
    Typical usage:
        gpio = GPIOService()
        gpio.set_pin_pwm(17, 127)  # Set pin 17 to 50% brightness
    """
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def set_pin_pwm(self, pin: int, value: int) -> None:
        """Set pulse width modulation value for a specific GPIO pin using pigpio."""
        rounded = self._clamp_value(value)
        command = f'pigs p {pin} {rounded}'
        self.logger.debug(f"Executing GPIO command: {command}")
        os.system(command)

    def _clamp_value(self, value: Any, min_val: int = MIN_PWM_VALUE, max_val: int = MAX_PWM_VALUE) -> int:
        """Clamp value between min and max bounds."""
        rounded = int(round(value))
        if rounded < min_val:
            rounded = min_val
        if rounded > max_val:
            rounded = max_val
        return rounded