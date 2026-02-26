"""Unit conversion tools for magnetic quantities."""

# Conversion factors
CONVERSIONS = {
    "T_to_Gauss": 10000,
    "Gauss_to_T": 1 / 10000,
    "Wb_to_Maxwell": 1e8,
    "Maxwell_to_Wb": 1e-8,
    "A_per_m_to_Oersted": 1 / 79.577,
    "Oersted_to_A_per_m": 79.577,
    "H_to_mH": 1000,
    "mH_to_H": 1 / 1000,
    "H_to_uH": 1e6,
    "uH_to_H": 1e-6,
    "mH_to_uH": 1000,
    "uH_to_mH": 1 / 1000,
}


def convert_unit(value: float, from_unit: str, to_unit: str) -> dict:
    """
    Convert between magnetic units.

    Args:
        value: The numerical value to convert
        from_unit: The unit to convert from (e.g., 'T', 'Gauss', 'A/m')
        to_unit: The unit to convert to (e.g., 'Gauss', 'T', 'Oersted')

    Returns:
        Dictionary with converted value or error message
    """
    # Normalize unit names
    from_unit = from_unit.strip()
    to_unit = to_unit.strip()

    if from_unit == to_unit:
        return {
            "original_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "converted_value": value,
            "message": "Input and output units are the same"
        }

    # Normalize units for key lookup (replace "/" with "_per_")
    from_unit_normalized = from_unit.replace("/", "_per_")
    to_unit_normalized = to_unit.replace("/", "_per_")

    # Try to find conversion key
    conversion_key = f"{from_unit_normalized}_to_{to_unit_normalized}"
    reverse_key = f"{to_unit_normalized}_to_{from_unit_normalized}"

    if conversion_key in CONVERSIONS:
        converted = value * CONVERSIONS[conversion_key]
        return {
            "original_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "converted_value": converted
        }
    elif reverse_key in CONVERSIONS:
        converted = value / CONVERSIONS[reverse_key]
        return {
            "original_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "converted_value": converted
        }
    else:
        supported = ", ".join(sorted(set(
            k.split("_to_")[0].replace("_per_", "/") for k in CONVERSIONS.keys()
        )))
        return {
            "error": f"Conversion from '{from_unit}' to '{to_unit}' not supported",
            "supported_units": supported
        }
