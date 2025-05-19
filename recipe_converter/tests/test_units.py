"""Tests for the unit conversion functions."""

import pytest
from recipe_converter.units import (
    convert_volume,
    convert_weight,
    convert_temperature,
)


def test_convert_volume_cup_to_ml():
    """Test conversion from cups to milliliters."""
    # 1 cup should be 236.588ml
    assert round(convert_volume(1, "cup", "ml"), 3) == 236.588


def test_convert_volume_ml_to_cup():
    """Test conversion from milliliters to cups."""
    # 237 ml should be approximately 1 cup
    assert round(convert_volume(237, "ml", "cup"), 2) == 1.00


def test_convert_weight_oz_to_g():
    """Test conversion from ounces to grams."""
    # 1 oz should be 28.35g
    assert round(convert_weight(1, "oz", "g"), 2) == 28.35


def test_convert_weight_lb_to_kg():
    """Test conversion from pounds to kilograms."""
    # 1 lb should be approximately 0.454 kg
    assert round(convert_weight(1, "lb", "kg"), 3) == 0.454


def test_convert_temperature_f_to_c():
    """Test conversion from Fahrenheit to Celsius."""
    # 32°F should be 0°C
    assert convert_temperature(32, "f", "c") == 0
    # 212°F should be 100°C
    assert convert_temperature(212, "f", "c") == 100


def test_convert_temperature_c_to_f():
    """Test conversion from Celsius to Fahrenheit."""
    # 0°C should be 32°F
    assert convert_temperature(0, "c", "f") == 32
    # 100°C should be 212°F
    assert convert_temperature(100, "c", "f") == 212


def test_invalid_unit_conversion():
    """Test that invalid unit conversions raise ValueErrors."""
    with pytest.raises(ValueError):
        convert_volume(1, "cup", "invalid_unit")

    with pytest.raises(ValueError):
        convert_weight(1, "invalid_unit", "g")
