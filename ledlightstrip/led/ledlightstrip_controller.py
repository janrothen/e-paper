#!/usr/bin/env python3


from threading import Thread
import logging
from typing import Any, Callable, Optional, Dict
from .color import Color
from .gpio_service import GPIOService

R: str = 'red'
G: str = 'green'
B: str = 'blue'


class LEDLightstripController(object):
    def __init__(self, pins: Dict[str, int], gpio_service: Optional[GPIOService] = None) -> None:
        self._gpio_service = gpio_service or GPIOService()
        self._pins = pins

        self._interrupt = False
        self._sequence = None

    def switch_on(self) -> None:
        self.set_color(Color.WHITE)

    def switch_off(self) -> None:
        self.interrupt()
        self.set_color(Color.BLACK)
        self.resume()

    def interrupt(self) -> None:
        self._interrupt = True

    def resume(self) -> None:
        self._interrupt = False

    def is_interrupted(self) -> bool:
        """Check if the current sequence should be interrupted."""
        return self._interrupt

    def set_color(self, color: Color = Color.WHITE) -> None:
        logging.info(f"Set RGB to: R={color.red:6.2f} G={color.green:6.2f} B={color.blue:6.2f}")
        self._set_red_value(color.red)
        self._set_green_value(color.green)
        self._set_blue_value(color.blue)

    #region Sequence control
    def run_sequence(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        self.stop_current_sequence()
        self.start_sequence(func, *args, **kwargs)

    def start_sequence(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        logging.info(f"Starting sequence: {func.__name__}")
        self._sequence = Thread(target=func, args=args, kwargs=kwargs)
        self.resume()
        self._sequence.start()

    def stop_current_sequence(self, timeout: int = 60) -> None:
        if self._sequence is None:
            logging.info("No sequence to stop.")
            return
        
        logging.info(f"Stopping sequence: {self._sequence.name}")
        self.interrupt()
        try:
            self._sequence._sequence_stop_signal = True
            self._sequence.join(timeout)
        except AttributeError:
            pass

        self._reset_sequence()
    #endregion

    #region Private basic
    def _set_red_value(self, value: int) -> None:
        self._gpio_service.set_pin_pwm(self._pins[R], value)

    def _set_green_value(self, value: int) -> None:
        self._gpio_service.set_pin_pwm(self._pins[G], value)

    def _set_blue_value(self, value: int) -> None:
        self._gpio_service.set_pin_pwm(self._pins[B], value)

    def _reset_sequence(self) -> None:
        self._sequence = None
    #endregion