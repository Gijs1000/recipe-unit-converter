"""Command line interface for the recipe converter."""

import argparse
import sys
from typing import TextIO

from recipe_converter.parser import recipe_parser
from recipe_converter.ingredients_db import ingredient_db
from recipe_converter.converter import convert_weight, convert_temperature
from recipe_converter.models import ParsedIngredient


def format_converted_ingredient(
    ingredient: ParsedIngredient, to_metric: bool = True
) -> str:
    """Format a converted ingredient with appropriate units.

    Args:
        ingredient (ParsedIngredient): parsed ingredient from the recipe
        to_metric (bool, optional): whether to convert to metric (True) or US (False).
                                    Defaults to True.

    Returns:
        str: a  formatted string with the converted ingredient.
    """
    # Skip ingredients without units
    if not ingredient.unit:
        return ingredient.original_text

    # Find the ingredient in the database
    ingredient_data = ingredient_db.get_ingredient(ingredient.name)
    if not ingredient_data:
        # TODO: we could still do weight-to-weight conversion, right?
        # If not found, we can't do volume-to-weight-conversion
        return ingredient.original_text

    try:
        # US volume to metric weight
        if to_metric and ingredient.unit in [
            "cup",
            "tablespoon",
            "teaspoon",
            "fluid ounce",
        ]:
            grams = ingredient_data.convert_volume_to_weight(
                ingredient.amount, ingredient.unit
            )
            # Format appropriately based on amount
            if grams < 1:
                return f"{grams * 1000:.0f} mg {ingredient.name}"
            elif grams < 1000:
                return f"{grams:.0f} g {ingredient.name}"
            else:
                return f"{grams / 1000:.2f} kg {ingredient.name}"

        # US weight to metric weight
        elif to_metric and ingredient.unit in ["pound", "ounce"]:
            grams = convert_weight(ingredient.amount, ingredient.unit, "g")
            if grams < 1000:
                return f"{grams:.0f} g {ingredient.name}"
            else:
                return f"{grams / 1000:.2f} kg {ingredient.name}"

        # Temperature conversion
        # XXX: this shouldn't be done this way. Temperature is not an ingredient.
        elif ingredient.unit in ["f", "c"]:
            if to_metric and ingredient.unit == "f":
                celsius = convert_temperature(ingredient.amount, "f", "c")
                return f"{celsius:.0f} °C {ingredient.name}"
            elif not to_metric and ingredient.unit == "c":
                fahrenheit = convert_temperature(ingredient.amount, "c", "f")
                return f"{fahrenheit:.0f}°F {ingredient.name}"

        # Default: return original text if no conversion applies
        else:
            return ingredient.original_text

    except ValueError:
        # If conversion fails for any reason, return the original text
        return ingredient.original_text


def convert_recipe(
    input_file: TextIO,
    output_file: TextIO,
    to_metric: bool = False,
    verbose: bool = False,
) -> int:
    """Convert a recipe from a file and write the converted version.

    Args:
        input_file: File-like object to read recipe from
        output_file: File-like object to write converted recipe to
        to_metric: Whether to convert to metric (True) or US (False)
        verbose: Whether to print verbose output

    Returns:
        Number of ingredients successfully converted
    """
    try:
        # Read the input text
        recipe_text = input_file.read()

        if verbose:
            print(f"Read {len(recipe_text)} characters from input")

        # Parse the recipe
        ingredients = recipe_parser.parse_recipe(recipe_text)

        if verbose:
            print(f"Found {len(ingredients)} ingredient lines.")

        # Convert ingredients
        original_lines = recipe_text.split("\n")
        converted_lines = []

        # Track which lines are ingredients to convert them
        ingredient_lines = {ing.original_text for ing in ingredients}

        # Count successful conversions
        conversion_count = 0

        for line in original_lines:
            if line.strip() in ingredient_lines:
                # Find the parsed ingredient for this line
                ingredient = next(
                    (
                        ing
                        for ing in ingredients
                        if ing.original_text == line.strip()
                    ),
                    None,
                )
                if ingredient:
                    original = ingredient.original_text
                    converted = format_converted_ingredient(
                        ingredient, to_metric
                    )

                    # Only count as converted if it actually changed
                    if converted != original:
                        conversion_count += 1
                        if verbose:
                            print(f"Converted: {original} → {converted}")
                    else:
                        if verbose:
                            print(f"No conversion needed for: {original}")

                    converted_lines.append(converted)
                else:
                    converted_lines.append(line)
            else:
                # Keep non-ingredient lines as-is
                converted_lines.append(line)

        # Write output
        output_file.write("\n".join(converted_lines))

        return conversion_count

    except Exception as e:
        print(f"Error converting recipe: {e}", file=sys.stderr)
        return 0


def main(args: list[str] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command-line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Convert recipes between US and metric measurements."
    )

    parser.add_argument(
        "input",
        nargs="?",
        type=str,
        default="-",
        help="Input recipe file (use '-' for stdin)",
    )

    parser.add_argument(
        "output",
        nargs="?",
        type=str,
        default="-",
        help="Output file for converted recipe (use '-' for stdout)",
    )

    parser.add_argument(
        "--to-us",
        action="store_true",
        help="Convert to US measurements (default is to metric)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )

    parsed_args = parser.parse_args(args)

    # Handle input file
    if parsed_args.input == "-":
        input_file = sys.stdin
        if parsed_args.verbose:
            print("Reading from stdin...")
    else:
        try:
            input_file = open(parsed_args.input, "r")
            if parsed_args.verbose:
                print(f"Reading from {parsed_args.input}...")
        except IOError as e:
            print(f"Error opening input file: {e}", file=sys.stderr)
            return 1

    # Handle output file
    if parsed_args.output == "-":
        output_file = sys.stdout
        if parsed_args.verbose:
            print("Writing to stdout...")
    else:
        try:
            output_file = open(parsed_args.output, "w")
            if parsed_args.verbose:
                print(f"Writing to {parsed_args.output}...")
        except IOError as e:
            print(f"Error opening output file: {e}", file=sys.stderr)
            if parsed_args.input != "-":
                input_file.close()
            return 1

    try:
        # Perform the conversion
        conversions = convert_recipe(
            input_file, output_file, not parsed_args.to_us, parsed_args.verbose
        )

        # Show summary if not writing to stdout
        if parsed_args.output != "-" and parsed_args.verbose:
            print(f"Successfully converted {conversions} ingredients")
            print(f"Converted recipe written to {parsed_args.output}")

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        # Close files if they're not stdin/stdout
        if parsed_args.input != "-":
            input_file.close()
        if parsed_args.output != "-":
            output_file.close()


if __name__ == "__main__":
    sys.exit(main())
