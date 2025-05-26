"""Integration tests for the recipe converter CLI."""
import os
import tempfile
from recipe_converter.cli import convert_recipe

# Sample recipes for testing
US_RECIPE = """Chocolate Chip Cookies

2 1/4 cups all-purpose flour
1 tsp baking soda
1 tsp salt
1 cup butter, softened
3/4 cup granulated sugar
3/4 cup packed brown sugar
2 large eggs
2 tsp vanilla extract
2 cups chocolate chips

Preheat oven to 375°F.
Mix ingredients and bake for 9-11 minutes.
"""


class TestCLIIntegration:
    """Integration tests for the recipe converter CLI."""

    def test_convert_us_to_metric(self):
        """Test converting a US recipe to metric units."""
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False
        ) as input_file, tempfile.NamedTemporaryFile(
            mode="w+", delete=False
        ) as output_file:
            # Write the sample recipe to the input file
            input_file.write(US_RECIPE)
            input_file.flush()

            # Close the files so they can be reopened
            input_path = input_file.name
            output_path = output_file.name

        try:
            # Reopen the files for the converter
            with open(input_path, "r") as input_file, open(
                output_path, "w"
            ) as output_file:
                # Run the converter
                conversions = convert_recipe(
                    input_file, output_file, to_metric=True
                )

                # Check that conversions happened
                assert conversions > 0

            # Read the output file
            with open(output_path, "r") as output_file:
                converted = output_file.read()

            # Check that the conversion worked correctly
            assert "Chocolate Chip Cookies" in converted  # Title preserved
            assert "270 g all-purpose flour" in converted  # 2 1/4 cups → 270g
            assert "5 g baking soda" in converted  # 1 tsp → 5g
            assert "227 g butter" in converted  # 1 cup → 227g
            assert "150 g granulated sugar" in converted  # 3/4 cup → 150g
            assert "165 g packed brown sugar" in converted  # 3/4 cup → 165g
            assert "2 large eggs" in converted  # No unit, unchanged
            assert "10 ml vanilla extract" in converted  # 2 tsp → 10ml
            assert "191°C" in converted  # 375°F → 191°C

        finally:
            # Clean up temporary files
            os.unlink(input_path)
            os.unlink(output_path)

    def test_nonexistent_ingredient(self):
        """Test handling of ingredients not in the database."""
        recipe = "1 cup unicorn tears\n"

        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False
        ) as input_file, tempfile.NamedTemporaryFile(
            mode="w+", delete=False
        ) as output_file:
            input_file.write(recipe)
            input_file.flush()

            input_path = input_file.name
            output_path = output_file.name

        try:
            with open(input_path, "r") as input_file, open(
                output_path, "w"
            ) as output_file:
                convert_recipe(input_file, output_file)

            with open(output_path, "r") as output_file:
                result = output_file.read()

            # Should leave original text unchanged
            assert result.strip() == "1 cup unicorn tears"

        finally:
            os.unlink(input_path)
            os.unlink(output_path)
