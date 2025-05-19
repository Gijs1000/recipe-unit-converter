"""Unit conversion functions for recipe ingredients."""


# Volume conversions
def convert_volume(amount: float, from_unit: str, to_unit: str) -> float:
    """
    Convert volume between different units.

    Args:
        amount (float): The amount to convert
        from_unit (str): Source unit (cup, tbsp, tsp, fl_oz, ml, l)
        to_unit (str): Target unit (cup, tbsp, tsp, fl_oz, ml, l)

    Returns:
        float: Converted amount in
    """
    # Conversion to milliliters (ml) as base unit
    ml_conversions = {
        "cup": 236.588,
        "tbsp": 14.787,
        "tsp": 4.929,
        "fl_oz": 29.574,
        "ml": 1,
        "l": 1000,
    }

    # Check if units are valid
    _validate_unit(to_unit, ml_conversions)
    _validate_unit(from_unit, ml_conversions)

    # Convert to base unit (ml)
    base_amount = amount * ml_conversions.get(from_unit)

    # Convert from base unit to target unit
    if base_amount is not None and to_unit in ml_conversions:
        return base_amount / ml_conversions.get(to_unit)
    else:
        raise ValueError(
            f"Unsupported unit conversion: {from_unit} to {to_unit}"
        )


# Weight conversions
def convert_weight(amount: float, from_unit: str, to_unit: str) -> float:
    """
    Convert weight between different units.

    Args:
        amount (float): The amount to convert
        from_unit (str): Source unit (g, kg, oz, lb)
        to_unit (str): Target unit (g, kg, oz, lb)

    Returns:
        float: Converted amount
    """
    # Conversion to grams (g) as a base unit
    g_conversions = {"g": 1, "kg": 1000, "oz": 28.35, "lb": 453.592}

    # Check if units are valid
    _validate_unit(to_unit, g_conversions)
    _validate_unit(from_unit, g_conversions)

    # Convert to base unit (g)
    base_amount = amount * g_conversions.get(from_unit)

    # Convert from base unit to target unit
    if base_amount is not None and to_unit in g_conversions:
        return base_amount / g_conversions.get(to_unit)
    else:
        raise ValueError(
            f"Unsupported unit conversion: {from_unit} to {to_unit}"
        )


# Temparature conversions
def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
    """
    Convert temperature between different units.

    Args:
        temp (float): The temperature to convert
        from_unit (str): Source unit (f, c)
        to_unit (str): Target unit (f, c)

    Returns:
        float: Converted temperature
    """
    if from_unit == "f" and to_unit == "c":
        return (temp - 32) * 5 / 9
    elif from_unit == "c" and to_unit == "f":
        return (temp * 9 / 5) + 32
    elif from_unit == to_unit:
        return temp
    else:
        raise ValueError(
            f"Unsupported temperature conversion: {from_unit} to {to_unit}"
        )


def _validate_unit(unit: str, valid_units: dict) -> None:
    """
    Validate that a unit exists in the dictionary of valid units.

    Args:
        unit (str): The unit to validate
        valid_units (dict): Dictionary of valid units and their conversion factors
        unit_type (str): Type of unit for the error message (e.g., "volume", "weight")

    Raises:
        ValueError: If the unit is not in the dictionary of valid units
    """
    if unit not in valid_units:
        valid_unit_list = ", ".join(valid_units.keys())
        raise ValueError(
            f"Unsupported unit: '{unit}'. Valid units are: {valid_unit_list}"
        )
