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
        # Flours and grains
        self.add_ingredient(
            "all-purpose flour",
            120,
            ["flour", "all purpose flour", "plain flour", "white flour"],
        )
        self.add_ingredient("bread flour", 127, ["strong flour"])
        self.add_ingredient("cake flour", 100, ["pastry flour"])
        self.add_ingredient("whole wheat flour", 130, ["wholemeal flour"])
        self.add_ingredient(
            "rye flour", 102, ["dark rye flour", "light rye flour"]
        )
        self.add_ingredient("cornmeal", 138, ["polenta", "corn meal"])
        self.add_ingredient("almond flour", 96, ["ground almonds"])
        self.add_ingredient("oat flour", 90, ["ground oats"])
        self.add_ingredient("rice flour", 158, ["white rice flour"])
        self.add_ingredient(
            "cornstarch", 128, ["corn starch", "cornflour", "corn flour"]
        )
        self.add_ingredient("rolled oats", 85, ["old-fashioned oats", "oats"])
        self.add_ingredient("quick oats", 90, ["instant oats"])
        self.add_ingredient("rice", 185, ["white rice", "long grain rice"])
        self.add_ingredient("brown rice", 175, ["whole grain rice"])

        # Sugars and sweeteners
        self.add_ingredient("granulated sugar", 200, ["sugar", "white sugar"])
        self.add_ingredient(
            "brown sugar",
            220,
            ["light brown sugar", "dark brown sugar", "packed brown sugar"],
        )
        self.add_ingredient(
            "powdered sugar", 120, ["confectioners sugar", "icing sugar"]
        )
        self.add_ingredient("honey", 340, ["pure honey"])
        self.add_ingredient("maple syrup", 315, ["pure maple syrup"])
        self.add_ingredient("corn syrup", 328, ["light corn syrup"])
        self.add_ingredient("molasses", 328, ["black treacle"])

        # Fats and oils
        # TODO: create modifier DB so we can mix and match ingredient modifiers
        self.add_ingredient(
            "butter",
            227,
            ["unsalted butter", "salted butter", "butter, softened"],
        )
        self.add_ingredient(
            "vegetable oil", 218, ["canola oil", "sunflower oil"]
        )
        self.add_ingredient(
            "olive oil", 216, ["extra virgin olive oil", "evoo"]
        )
        self.add_ingredient("coconut oil", 218, ["virgin coconut oil"])
        self.add_ingredient("shortening", 205, ["vegetable shortening"])

        # Dairy and alternatives
        self.add_ingredient(
            "milk", 240, ["whole milk", "skim milk", "semi-skimmed milk"]
        )
        self.add_ingredient(
            "heavy cream", 238, ["double cream", "whipping cream"]
        )
        self.add_ingredient("half and half", 242, ["half-and-half"])
        self.add_ingredient("buttermilk", 240, ["cultured buttermilk"])
        self.add_ingredient("yogurt", 245, ["plain yogurt", "greek yogurt"])
        self.add_ingredient("sour cream", 230, ["cultured sour cream"])
        self.add_ingredient("cream cheese", 250, ["full-fat cream cheese"])
        self.add_ingredient(
            "cottage cheese", 225, ["small curd cottage cheese"]
        )
        self.add_ingredient("ricotta cheese", 246, ["whole milk ricotta"])

        # Leavening agents and salts
        self.add_ingredient(
            "salt", 288, ["sea salt", "kosher salt", "table salt"]
        )
        self.add_ingredient("baking powder", 192, [])
        self.add_ingredient(
            "baking soda", 220, ["bicarbonate of soda", "sodium bicarbonate"]
        )
        self.add_ingredient("active dry yeast", 128, ["dried yeast"])
        self.add_ingredient(
            "instant yeast", 128, ["rapid-rise yeast", "bread machine yeast"]
        )

        # Nuts and seeds
        self.add_ingredient(
            "almonds", 142, ["whole almonds", "sliced almonds"]
        )
        self.add_ingredient("walnuts", 125, ["chopped walnuts"])
        self.add_ingredient("pecans", 110, ["pecan halves"])
        self.add_ingredient("peanuts", 146, ["roasted peanuts"])
        self.add_ingredient("sunflower seeds", 140, ["hulled sunflower seeds"])
        self.add_ingredient("flax seeds", 150, ["linseeds"])
        self.add_ingredient("chia seeds", 170, [])

        # Chocolate and cocoa
        self.add_ingredient("cocoa powder", 100, ["unsweetened cocoa powder"])
        self.add_ingredient(
            "chocolate chips", 170, ["semi-sweet chocolate chips"]
        )
        self.add_ingredient("chocolate chunks", 170, ["chocolate pieces"])
        self.add_ingredient("milk chocolate", 168, ["milk chocolate chips"])
        self.add_ingredient("dark chocolate", 170, ["bittersweet chocolate"])
        self.add_ingredient("white chocolate", 170, ["white chocolate chips"])

        # Fruits and vegetables
        self.add_ingredient("raisins", 165, ["seedless raisins"])
        self.add_ingredient("dried cranberries", 120, ["craisins"])
        self.add_ingredient(
            "carrots", 128, ["grated carrots", "shredded carrots"]
        )
        self.add_ingredient("zucchini", 130, ["grated zucchini", "courgette"])
        self.add_ingredient("apples", 130, ["chopped apples", "diced apples"])
        self.add_ingredient("bananas", 230, ["mashed bananas"])

        # Liquids
        self.add_ingredient("water", 237, [])
        self.add_ingredient("coffee", 237, ["brewed coffee"])
        self.add_ingredient("apple juice", 242, ["unsweetened apple juice"])
        self.add_ingredient("orange juice", 248, ["fresh orange juice"])

        # Extracts and flavorings
        self.add_ingredient("vanilla extract", 208, ["pure vanilla extract"])
        self.add_ingredient("almond extract", 208, ["pure almond extract"])
        self.add_ingredient("lemon juice", 245, ["fresh lemon juice"])
        self.add_ingredient("lime juice", 246, ["fresh lime juice"])

        # Spices and herbs
        self.add_ingredient("cinnamon", 132, ["ground cinnamon"])
        self.add_ingredient("nutmeg", 125, ["ground nutmeg"])
        self.add_ingredient("ginger", 120, ["ground ginger"])
        self.add_ingredient("cloves", 130, ["ground cloves"])
        self.add_ingredient("allspice", 114, ["ground allspice"])
        self.add_ingredient("cardamom", 108, ["ground cardamom"])


# Create a singleton instance for easy import
ingredient_db = IngredientDatabase()
