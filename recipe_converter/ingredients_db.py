"""Ingredient database with density values for common ingredients."""

from recipe_converter.models import Ingredient


class IngredientDatabase:
    """
    Database of ingredient densities and properties.

    This database provides density information for different ingredients, which is
    crucial for accurate volume-to-weight-conversions.
    """

    def __init__(self) -> None:
        """Initialize the ingredient database with default values."""
        self.ingredients: dict[str, Ingredient] = {}
        self._load_default_ingredients()

    def get_ingredient(self, name: str) -> Ingredient | None:
        """Look up an ingredient by its name or alias.

        Args:
            name (str): The name to look up.

        Returns:
            Ingredient | None: Matching Ingredient object when found. Else None.
        """
        lookup_name = name.casefold()

        # Direct lookup
        if lookup_name in self.ingredients:
            return self.ingredients[lookup_name]

        # If not found, try normalizing name
        normalized = lookup_name.replace("-", " ").replace("_", " ")
        if normalized in self.ingredients:
            return self.ingredients[normalized]

        return None

    def add_ingredient(
        self, name: str, density: float, aliases: list[str] = None
    ) -> None:
        """Add an ingredient to the database.

        Args:
            name (str): The canonical name of the ingredient.
            density (float): The density in grams per cup.
            aliases (list[str], optional): alternative names for this ingredient.
            Defaults to None.
        """
        if aliases is None:
            aliases = []

        ingredient = Ingredient(name, density, aliases)

        # Add by canonical name
        self.ingredients[ingredient.name] = ingredient

        # Add by each alias
        for alias in ingredient.aliases:
            self.ingredients[alias] = ingredient

    def _load_default_ingredients(self) -> None:
        """Load the default ingredient data."""
        # Basic baking ingredients
        self.add_ingredient(
            "all-purpose flour",
            120,
            ["all purpose flour", "flour", "plain flour", "white flour"],
        )
        self.add_ingredient("bread flour", 127, ["strong flour"])
        self.add_ingredient("cake flour", 100, ["pastry flour"])
        self.add_ingredient("whole wheat flour", 130, ["wholemeal flour"])
        self.add_ingredient("granulated sugar", 200, ["sugar", "white sugar"])
        self.add_ingredient(
            "brown sugar", 220, ["light brown sugar", "dark brown sugar"]
        )
        self.add_ingredient(
            "powdered sugar", 120, ["confectioners sugar", "icing sugar"]
        )
        self.add_ingredient(
            "butter", 227, ["unsalted butter", "salted butter"]
        )
        self.add_ingredient(
            "vegetable oil", 218, ["canola oil", "sunflower oil"]
        )
        self.add_ingredient(
            "olive oil", 216, ["extra virgin olive oil", "evoo"]
        )
        self.add_ingredient(
            "milk", 240, ["whole milk", "skim milk", "semi-skimmed milk"]
        )
        self.add_ingredient(
            "heavy cream", 238, ["double cream", "whipping cream"]
        )
        self.add_ingredient("water", 237, [])
        self.add_ingredient(
            "salt", 288, ["sea salt", "kosher salt", "table salt"]
        )
        self.add_ingredient("baking powder", 192, [])
        self.add_ingredient(
            "baking soda", 220, ["bicarbonate of soda", "sodium bicarbonate"]
        )
        self.add_ingredient("cocoa powder", 100, ["unsweetened cocoa powder"])
        self.add_ingredient("rice", 185, ["white rice", "long grain rice"])


# Create a singleton instance for easy import
ingredient_db = IngredientDatabase()
