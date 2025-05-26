"""Recipe text parsing module.

This module provides functionality for parsing recipes and extracting
ingredients with their measurements.
"""

import re
from fractions import Fraction
from recipe_converter.models import ParsedIngredient


class RecipeParser:
    """Parser for extracting ingredients from recipe text."""

    # Regex patterns
    FRACTION_PATTERN = r"(?:\d+\s+)?(?:\d+/\d+)"
    DECIMAL_PATTERN = r"\d+\.\d+"
    INTEGER_PATTERN = r"\d+"

    # Combined pattern for any number format
    NUMBER_PATTERN = f"(?:{FRACTION_PATTERN}|{DECIMAL_PATTERN}|{INTEGER_PATTERN})"  # noqa: E231, E501

    # Common US volume units with variations
    VOLUME_UNITS = {
        "cup": ["cup", "cups", "c.", "c"],
        "tablespoon": [
            "tablespoon",
            "tablespoons",
            "tbsp",
            "tbsp.",
            "tbs",
            "tbs.",
        ],
        "teaspoon": ["teaspoon", "teaspoons", "tsp", "tsp."],
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

    # Flatten the unit variations into a single list for regex. Sory by longest word
    # first so the regex later on will find "cups" instead of stopping at "cup" since
    # that is matched.
    UNIT_VARIATIONS = sorted(
        [var for variations in ALL_UNITS.values() for var in variations],
        key=len,
        reverse=True,
    )

    # Ingredient line pattern - matches lines that likely contain ingredients
    # This regex pattern is designed to match typical ingredient lines.
    # It maches a number, followed by a unit, followed by either "of" (as in 0.5 liters
    # of milk) or by the ingredient (as in 5 teaspoons milk).
    INGREDIENT_PATTERN = re.compile(
        rf'^\s*({NUMBER_PATTERN})?\s*(?:\b({"|".join(UNIT_VARIATIONS)})\b)?\s*(.+?)$',  # noqa: E231, E501
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

        groups = match.groups()
        amount_str, unit_str, name = groups

        # If there's no amount but there is a unit, assume amount is 1
        if not amount_str and unit_str:
            amount_str = "1"

        # If there's no amount and no unit, it's probably not an ingredient
        if not amount_str and not unit_str:
            return None

        # Parse amount
        if amount_str:
            try:
                amount_str = amount_str.strip()  # Not amount.str
                amount = float(sum(Fraction(s) for s in amount_str.split()))
            except ValueError:
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
        unit_str = unit_str.casefold()

        # Return canonical unit name or un-normalized if not found.
        return self.unit_map.get(unit_str, unit_str)


# Create a singleton instance for easy import
recipe_parser = RecipeParser()
