"""Tests for the ingredient class.

This module contains unit tests for the Ingredient class in the
recipe_converter.ingredients module.
"""

import pytest
from recipe_converter.models import Ingredient


class TestIngredient:
    """Test suite for the Ingredient class."""

    def test_init_with_defaults(self):
        """Test that Ingredient initializes correctly with default values."""
        flour = Ingredient("Flour", 120)
        assert flour.name == "flour"
        assert flour.density == 120
        assert flour.aliases == []

    def test_init_with_aliases(self):
        """Test that Ingredient initializes correctly with provided aliases."""
        flour = Ingredient("All-Purpose Flour", 120, ["flour", "AP Flour"])
        assert flour.name == "all-purpose flour"
        assert flour.density == 120
        assert len(flour.aliases) == 2
        assert "flour" in flour.aliases
        assert "ap flour" in flour.aliases

    def test_special_characters_in_name(self):
        """Test that special characters in names are handled correctly."""
        sugar = Ingredient("CAFÉ Sugar", 200)
        assert sugar.name == "café sugar"  # casefold handles special

    def test_convert_volume_to_weight_cup(self):
        """Test converting from cup to weight."""
        sugar = Ingredient("Sugar", 200)
        # 1 cup of sugar (200g per cup)
        assert sugar.convert_volume_to_weight(1, "cup") == 200

    def test_convert_volume_to_weight_tablespoon(self):
        """Test converting from tablespoon to weight."""
        sugar = Ingredient("Sugar", 200)
        # 1 tbsp is 1/16 of a cup, so 200g/16 = 12.5g
        assert sugar.convert_volume_to_weight(1, "tbsp") == pytest.approx(
            12.5, 0.1
        )

    def test_convert_volume_to_weight_multiple_units(self):
        """Test converting from various volume units to weight."""
        flour = Ingredient("Flour", 120)
        # Test with different volume units
        assert flour.convert_volume_to_weight(0.5, "cup") == 60
        assert flour.convert_volume_to_weight(2, "tbsp") == pytest.approx(
            15, 0.1
        )
        assert flour.convert_volume_to_weight(1, "fl_oz") == pytest.approx(
            15, 0.1
        )
        assert flour.convert_volume_to_weight(240, "ml") == pytest.approx(
            120, 0.1
        )

    def test_convert_weight_to_volume_cup(self):
        """Test converting from weight to cups."""
        flour = Ingredient("Flour", 120)
        # 120g flour = 1 cup
        assert flour.convert_weight_to_volume(120, "cup") == 1

    def test_convert_weight_to_volume_multiple_units(self):
        """Test converting from weight to various volume units."""
        sugar = Ingredient("Sugar", 200)
        # 100g sugar
        assert sugar.convert_weight_to_volume(100, "cup") == 0.5
        assert sugar.convert_weight_to_volume(100, "tbsp") == pytest.approx(
            8, 0.1
        )
        assert sugar.convert_weight_to_volume(100, "ml") == pytest.approx(
            118.3, 0.1
        )

    def test_convert_weight_to_volume_zero_density(self):
        """Test that zero density raises a ZeroDivisionError."""
        invalid = Ingredient("Invalid", 0)
        with pytest.raises(ZeroDivisionError):
            invalid.convert_weight_to_volume(100, "cup")

    def test_convert_with_invalid_unit(self):
        """Test that invalid units raise a ValueError."""
        flour = Ingredient("Flour", 120)
        with pytest.raises(ValueError):
            flour.convert_volume_to_weight(1, "invalid_unit")
        with pytest.raises(ValueError):
            flour.convert_weight_to_volume(100, "invalid_unit")
