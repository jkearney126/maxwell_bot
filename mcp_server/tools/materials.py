"""Magnetic material property lookup."""

MATERIALS = {
    "air": {
        "relative_permeability": 1.0,
        "saturation_flux_density_T": None,
        "coercivity_A_per_m": 0.0,
        "description": "Vacuum/air"
    },
    "iron": {
        "relative_permeability": 5000.0,
        "saturation_flux_density_T": 2.15,
        "coercivity_A_per_m": 800.0,
        "description": "Pure iron (soft magnetic)"
    },
    "silicon_steel": {
        "relative_permeability": 4000.0,
        "saturation_flux_density_T": 2.0,
        "coercivity_A_per_m": 400.0,
        "description": "Silicon steel (transformer core)"
    },
    "ferrite": {
        "relative_permeability": 2000.0,
        "saturation_flux_density_T": 0.4,
        "coercivity_A_per_m": 250000.0,
        "description": "Ferrite (hard magnetic)"
    },
    "neodymium": {
        "relative_permeability": 1.05,
        "saturation_flux_density_T": 1.4,
        "coercivity_A_per_m": 955000.0,
        "description": "Neodymium magnet (NdFeB, hard magnetic)"
    },
    "mu_metal": {
        "relative_permeability": 80000.0,
        "saturation_flux_density_T": 0.8,
        "coercivity_A_per_m": 8.0,
        "description": "Mu-metal (high permeability shielding)"
    }
}


def lookup_material(material_name: str) -> dict:
    """
    Look up properties of a named magnetic material.

    Args:
        material_name: Name of the material (case-insensitive)

    Returns:
        Dictionary with material properties or error message
    """
    material_lower = material_name.lower().strip()

    if material_lower not in MATERIALS:
        available = ", ".join(MATERIALS.keys())
        return {
            "error": f"Material '{material_name}' not found",
            "available_materials": available
        }

    return MATERIALS[material_lower]
