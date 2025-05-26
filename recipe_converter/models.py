"""Recipe unit conversion module.

Recipe unit conversion module providing object-oriented interfaces for
converting between US and metric measurements in recipes.
"""

from dataclasses import dataclass, field

from recipe_converter.converter import convert_volume


@dataclass
class Ingredient:
    """
    Represents a recipe ingredient with its density information.

    Attributes:
    name: The canonical name of the ingredient
    density: The density in grams per cup
    aliases: Alternative names for this ingredient
    """

    name: str  # Base name for lookup
    density: float  # grams per cup
    aliases: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Process the name and aliases after initialization."""
        self.name = self.name.casefold()  # lower name incl. special characters
        self.aliases = [alias.casefold() for alias in self.aliases]

    def convert_volume_to_weight(self, amount: float, unit: str) -> float:
        """
        Convert a volume measurement to weight.

        Args:
            amount: the amount in the specified unit.
            unit: the unit of volume (cup, tbsp, etc.)

        Returns:
            Weight in grams for a cup of this ingredient.
        """
        cups = convert_volume(amount, unit, "cup")
        return cups * self.density

    def convert_weight_to_volume(self, grams: float, unit: str) -> float:
        """
        Convert a weight measurement to volume.

        Args:
        grams: The weight in grams.
        unit: The desired volume unit.

        Returns:
        Volume in the requested unit
        """
        cups = grams / self.density
        return convert_volume(cups, "cup", unit)


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
