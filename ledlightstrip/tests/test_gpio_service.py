#!/usr/bin/env python3

"""
Tests for the GPIO service.

Tests GPIO pin control functionality with mocked system calls.
"""

import pytest
from unittest.mock import patch, Mock
from led.gpio_service import GPIOService


class TestGPIOService:
    """Test cases for GPIO service functionality."""
    
    def test_gpio_service_creation(self):
        """Test GPIO service can be created."""
        service = GPIOService()
        assert service is not None
    
    @patch('led.gpio_service.os.system')
    def test_set_pin_pwm(self, mock_system):
        """Test setting PWM value on a pin."""
        service = GPIOService()
        service.set_pin_pwm(18, 128)
        
        mock_system.assert_called_once_with('pigs p 18 128')
    
    @patch('led.gpio_service.os.system')
    def test_set_pin_pwm_clamping(self, mock_system):
        """Test PWM value clamping."""
        service = GPIOService()
        
        # Test upper bound clamping
        service.set_pin_pwm(18, 300)
        mock_system.assert_called_with('pigs p 18 255')
        
        # Test lower bound clamping
        service.set_pin_pwm(18, -10)
        mock_system.assert_called_with('pigs p 18 0')
    
    @patch('led.gpio_service.os.system')
    def test_set_pin_pwm_rounding(self, mock_system):
        """Test PWM value rounding."""
        service = GPIOService()
        service.set_pin_pwm(18, 127.8)
        
        mock_system.assert_called_once_with('pigs p 18 128')
    
    def test_clamp_value_method(self):
        """Test internal value clamping method."""
        service = GPIOService()
        
        assert service._clamp_value(127.5) == 128
        assert service._clamp_value(300) == 255
        assert service._clamp_value(-10) == 0
        assert service._clamp_value(100) == 100