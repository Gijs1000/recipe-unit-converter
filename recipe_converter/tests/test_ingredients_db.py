"""Tests for the ingredient database module."""
from recipe_converter.ingredients_db import IngredientDatabase


class TestIngredientDatabase:
    """Test suite for the IngredientDatabase class."""

    def setup_method(self):
        """Create a fresh database instance before each test."""
        # Create a new instance for each test to ensure test isolation
        self.db = IngredientDatabase()

    def test_default_ingredients_loaded(self):
        """Test that default ingredients are loaded on initialization."""
        # Check that common ingredients exist in the database
        assert self.db.get_ingredient("flour") is not None
        assert self.db.get_ingredient("sugar") is not None
        assert self.db.get_ingredient("butter") is not None

        # Verify specific properties of one ingredient
        flour = self.db.get_ingredient("flour")
        assert flour.name == "all-purpose flour"
        assert flour.density == 120

    def test_get_ingredient_by_canonical_name(self):
        """Test retrieving an ingredient by its canonical name."""
        # Get ingredient by full canonical name
        sugar = self.db.get_ingredient("granulated sugar")
        assert sugar is not None
        assert sugar.name == "granulated sugar"
        assert sugar.density == 200

    def test_get_ingredient_by_alias(self):
        """Test retrieving an ingredient by one of its aliases."""
        # Get ingredients by various aliases
        flour = self.db.get_ingredient("plain flour")
        assert flour is not None
        assert (
            flour.name == "all-purpose flour"
        )  # Should return canonical name

        butter = self.db.get_ingredient("unsalted butter")
        assert butter is not None
        assert butter.name == "butter"

        oil = self.db.get_ingredient("evoo")
        assert oil is not None
        assert oil.name == "olive oil"

    def test_get_ingredient_case_insensitive(self):
        """Test that ingredient lookup is case-insensitive."""
        # Mix of upper and lower case
        flour = self.db.get_ingredient("ALL-PURPOSE Flour")
        assert flour is not None
        assert flour.name == "all-purpose flour"

    def test_get_ingredient_normalized(self):
        """Test retrieval with different formatting (spaces vs. hyphens)."""
        # With hyphen in the database but spaces in the query
        flour = self.db.get_ingredient("all purpose flour")
        assert flour is not None
        assert flour.name == "all-purpose flour"

        # With spaces in query but different format in database
        soda = self.db.get_ingredient("baking soda")
        assert soda is not None
        assert soda.density == 220

    def test_get_nonexistent_ingredient(self):
        """Test that looking up a nonexistent ingredient returns None."""
        result = self.db.get_ingredient("nonexistent ingredient")
        assert result is None

    def test_add_ingredient(self):
        """Test adding a new ingredient to the database."""
        # Add a new ingredient
        self.db.add_ingredient(
            "maple syrup", 315, ["pure maple syrup", "canadian maple syrup"]
        )

        # Verify it can be retrieved
        syrup = self.db.get_ingredient("maple syrup")
        assert syrup is not None
        assert syrup.name == "maple syrup"
        assert syrup.density == 315

        # Check retrieval by alias
        syrup_by_alias = self.db.get_ingredient("canadian maple syrup")
        assert syrup_by_alias is not None
        assert syrup_by_alias.name == "maple syrup"

    def test_add_ingredient_overrides_existing(self):
        """Test that adding an ingredient with an existing name overrides it."""
        # Get the original density
        original_flour = self.db.get_ingredient("flour")
        assert original_flour.density == 120

        # Add a new flour with different density
        self.db.add_ingredient("flour", 130, ["plain flour"])

        # Check that the density has been updated
        updated_flour = self.db.get_ingredient("flour")
        assert updated_flour.density == 130

        # Ensure the alias still works
        by_alias = self.db.get_ingredient("plain flour")
        assert by_alias is not None
        assert by_alias.density == 130

    def test_add_ingredient_with_no_aliases(self):
        """Test adding an ingredient without any aliases."""
        # Add ingredient with no aliases
        self.db.add_ingredient("honey", 340)

        # Verify it can be retrieved
        honey = self.db.get_ingredient("honey")
        assert honey is not None
        assert honey.name == "honey"
        assert honey.density == 340
        assert honey.aliases == []


class TestIngredientDatabaseSingleton:
    """Test the singleton behavior of the ingredient database."""

    def test_instance_is_singleton(self):
        """Test that importing ingredient_db multiple times gives the same instance."""
        # This test verifies that multiple imports result in the same object
        from recipe_converter.ingredients_db import ingredient_db as db1
        from recipe_converter.ingredients_db import ingredient_db as db2

        # Should be the exact same object (identity check)
        assert db1 is db2

        # Modifying one should affect the other
        initial_count = len(db1.ingredients)
        db1.add_ingredient("test ingredient", 100)

        # Both references should see the new ingredient
        assert len(db2.ingredients) == initial_count + 1
        assert db2.get_ingredient("test ingredient") is not None
