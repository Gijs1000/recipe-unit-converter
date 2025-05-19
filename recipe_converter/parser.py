"""Recipe text parsing module.

This module provides functionality for parsing recipes and extracting
ingredients with their measurements.
"""

import re
from dataclasses import dataclass
from fractions import Fraction


@dataclass
class ParsedIngredient:
    """Represents a parsed ingredient from a recipe text.

    Attributes:
        amount: The numerical quantity.
        unit: The unit of measurement (cup, tbsp, etc.)
        name: The name of the ingredient.
        original_text: The original text this was parsed from.
    """

    amount: float
    unit: str
    name: str
    original_text: str


class RecipeParser:
    """Parser for extracting ingredients from recipe text."""

    # Regex patterns
    FRACTION_PATTERN = r"(\d+\s+)?\d+/\d+"
    DECIMAL_PATTERN = r"\d+\.\d+"
    INTEGER_PATTERN = r"\d+"

    # Combined pattern for any number format
    NUMBER_PATTERN = (
        f"({FRACTION_PATTERN}|{DECIMAL_PATTERN}|{INTEGER_PATTERN})"
    )

    # Common US volume units with variations
    VOLUME_UNITS = {
        "cup": ["cup", "cups", "c", "c."],
        "tablespoon": [
            "tablespoon",
            "tablespoons",
            "tbsp",
            "tbsp.",
            "tbs",
            "tbs.",
            "T",
        ],
        "teaspoon": ["teaspoon", "teaspoons", "tsp", "tsp.", "t"],
        "fluid ounce": [
            "fluid ounce",
            "fluid ounces",
            "fl oz",
            "fl. oz.",
            "oz.",
            "oz",
        ],
        "pint": ["pint", "pints", "pt", "pt."],
        "quart": ["quart", "quarts", "qt", "qt."],
        "gallon": ["gallon", "gallons", "gal", "gal."],
    }

    # Common US weight units
    WEIGHT_UNITS = {
        "pound": ["pound", "pounds", "lb", "lb.", "lbs", "lbs."],
        "ounce": ["ounce", "ounces", "oz", "oz."],
    }

    # Temperature units
    TEMPERATURE_UNITS = {
        "f": ["f", "fahrenheit", "degrees f", "degrees fahrenheit", "°f", "℉"],
    }

    # All units combined
    ALL_UNITS = {**VOLUME_UNITS, **WEIGHT_UNITS, **TEMPERATURE_UNITS}

    # Flatten the unit variations into a single list for regex
    UNIT_VARIATIONS = [
        var for variations in ALL_UNITS.values() for var in variations
    ]

    # Ingredient line pattern - matches lines that likely contain ingredients
    # This regex pattern is designed to match typical ingredient lines
    INGREDIENT_PATTERN = re.compile(
        rf'^\s*({NUMBER_PATTERN})?\s*({"|".join(UNIT_VARIATIONS)})?\s*(.+?)$',
        re.IGNORECASE,
    )

    def __init__(self):
        """Intialize the recipe parser."""
        # Build a map from unit variations to canonical unit names
        self.unit_map = {}
        for canonical, variations in self.ALL_UNITS.items():
            for var in variations:
                self.unit_map[var.lower()] = canonical

    def parse_recipe(self, text: str) -> list[ParsedIngredient]:
        """Parse a recipe text and extract ingredients.

        Args:
            text (str): Recipe text to parse.

        Returns:
            list[ParsedIngredient]: List of parsed ingredients.
        """
        lines = text.split("\n")
        ingredients = []

        for line in lines:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue

            # Try to parse as an ingredient
            ingredient = self._parse_ingredient_line(line)
            if ingredient:
                ingredients.append(ingredient)
        return ingredients

    def _parse_ingredient_line(self, line: str) -> ParsedIngredient | None:
        """Parse a single line as an ingredient.

        Args:
            line (str): the line to parse an ingredient from

        Returns:
            ParsedIngredient | None: ParsedIngredient if found. Else None.
        """
        # Match the line against the ingredient pattern
        match = self.INGREDIENT_PATTERN.match(line)
        if not match:
            return None

        amount_str, unit_str, name = match.groups()

        # If no amount or unit, this might not be an ingredient
        if not amount_str and not unit_str:
            return None

        # Parse the amount
        amount = 1.0
        if amount_str:
            try:
                # Handle mixed numbers and fractions
                amount_str = amount.str.strip()
                amount = float(sum(Fraction(s) for s in amount_str.split()))
            except ValueError:
                # If parsing fails, this might not be an ingredient.
                return None

        # Clean and normalize the unit
        unit = ""
        if unit_str:
            unit = self._normalize_unit(unit_str.strip().casefold())

        # Clean up the ingredient name
        name = name.strip()
        if name.startswith("of "):
            name = name[3:]
        name = name.strip(",")

        return ParsedIngredient(amount, unit, name, line)

    def _normalize_unit(self, unit_str: str) -> str:
        """Normalize a unit string to its canonical form.

        Args:
            unit_str (str): Unit string to normalize.

        Returns:
            str: Canonical unit name.
        """
        unit_str = unit_str.casefold().strip(".")

        # Return canonical unit name or un-normalized if not found.
        return self.unit_map.get(unit_str, unit_str)
