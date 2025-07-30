#!/usr/bin/env python3

"""
Tests for the LED strip controller.

Tests LED control functionality with mocked GPIO hardware.
"""

import pytest
from unittest.mock import Mock, patch
from led.ledlightstrip_controller import LEDLightstripController
from led.color import Color


class TestLEDLightstripController:
    """Test cases for LED strip controller."""
    
    def test_controller_creation(self, mock_gpio_service, test_pins):
        """Test controller can be created with dependencies."""
        controller = LEDLightstripController(test_pins, mock_gpio_service)
        
        assert controller._pins == test_pins
        assert controller._gpio_service == mock_gpio_service
        assert controller._interrupt is False
        assert controller._sequence is None
    
    def test_set_color(self, led_controller, mock_gpio_service):
        """Test setting LED color."""
        red_color = Color(255, 0, 0)
        led_controller.set_color(red_color)
        
        # Verify GPIO calls were made for each color channel
        expected_calls = [
            (18, 255),  # Red pin
            (19, 0),    # Green pin  
            (20, 0)     # Blue pin
        ]
        
        actual_calls = [call.args for call in mock_gpio_service.set_pin_pwm.call_args_list]
        assert actual_calls == expected_calls
    
    def test_switch_on(self, led_controller, mock_gpio_service):
        """Test switching LED strip on."""
        led_controller.switch_on()
        
        # Should set to white (255, 255, 255)
        expected_calls = [
            (18, 255),  # Red pin
            (19, 255),  # Green pin
            (20, 255)   # Blue pin
        ]
        
        actual_calls = [call.args for call in mock_gpio_service.set_pin_pwm.call_args_list]
        assert actual_calls == expected_calls
    
    def test_switch_off(self, led_controller, mock_gpio_service):
        """Test switching LED strip off."""
        led_controller.switch_off()
        
        # Should set to black (0, 0, 0) and manage interrupt state
        expected_calls = [
            (18, 0),    # Red pin
            (19, 0),    # Green pin
            (20, 0)     # Blue pin
        ]
        
        actual_calls = [call.args for call in mock_gpio_service.set_pin_pwm.call_args_list]
        assert actual_calls == expected_calls
    
    def test_interrupt_control(self, led_controller):
        """Test interrupt state management."""
        assert not led_controller.is_interrupted()
        
        led_controller.interrupt()
        assert led_controller.is_interrupted()
        
        led_controller.resume()
        assert not led_controller.is_interrupted()
    
    @patch('led.ledlightstrip_controller.Thread')
    def test_start_sequence(self, mock_thread_class, led_controller):
        """Test starting a sequence."""
        mock_thread = Mock()
        mock_thread_class.return_value = mock_thread
        
        def dummy_effect():
            pass
        
        led_controller.start_sequence(dummy_effect, "arg1", "arg2", kwarg1="value1")
        
        # Verify thread was created with correct arguments
        mock_thread_class.assert_called_once_with(
            target=dummy_effect, 
            args=("arg1", "arg2"), 
            kwargs={"kwarg1": "value1"}
        )
        mock_thread.start.assert_called_once()
        assert led_controller._sequence == mock_thread
        assert not led_controller.is_interrupted()
    
    def test_stop_sequence_no_sequence(self, led_controller):
        """Test stopping when no sequence is running."""
        # Should not raise an error when no sequence is running
        led_controller.stop_current_sequence()
        assert led_controller._sequence is None
    
    @patch('led.ledlightstrip_controller.Thread')
    def test_run_sequence(self, mock_thread_class, led_controller):
        """Test running a sequence (stop + start)."""
        mock_thread = Mock()
        mock_thread.name = "test_sequence"
        mock_thread_class.return_value = mock_thread
        
        def dummy_effect():
            pass
        
        led_controller.run_sequence(dummy_effect, "test_arg")
        
        mock_thread_class.assert_called_once_with(
            target=dummy_effect,
            args=("test_arg",),
            kwargs={}
        )
        mock_thread.start.assert_called_once()