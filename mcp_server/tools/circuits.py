"""Magnetic circuit analysis tools."""

import math

# Physical constant
MU_0 = 4 * math.pi * 1e-7  # H/m (permeability of free space)


def reluctance(length_m: float, area_m2: float, relative_permeability: float) -> dict:
    """
    Compute reluctance of a magnetic circuit path.

    Using R = l / (μ₀ · μᵣ · A)

    Args:
        length_m: Length of the magnetic path in meters
        area_m2: Cross-sectional area in square meters
        relative_permeability: Relative permeability of the material (dimensionless)

    Returns:
        Dictionary with reluctance in H⁻¹ (Ampere-turns per Weber)
    """
    if length_m <= 0:
        return {"error": "Length must be positive"}
    if area_m2 <= 0:
        return {"error": "Area must be positive"}
    if relative_permeability <= 0:
        return {"error": "Relative permeability must be positive"}

    mu = MU_0 * relative_permeability
    R = length_m / (mu * area_m2)

    return {
        "reluctance_H_inv": R,
        "reluctance_AT_per_Wb": R,  # Same units, different name
        "length_m": length_m,
        "area_m2": area_m2,
        "relative_permeability": relative_permeability,
        "permeability_H_per_m": mu,
        "equation": "R = l / (μ₀ · μᵣ · A)"
    }


def mmf_required(H_field: float, path_length_m: float) -> dict:
    """
    Compute magnetomotive force (MMF) needed for a magnetic path.

    Using MMF = H · l

    Args:
        H_field: Magnetic field strength in A/m
        path_length_m: Length of the magnetic path in meters

    Returns:
        Dictionary with MMF in Ampere-turns
    """
    if path_length_m < 0:
        return {"error": "Path length must be non-negative"}

    mmf = H_field * path_length_m

    return {
        "mmf_AT": mmf,
        "H_field_A_per_m": H_field,
        "path_length_m": path_length_m,
        "equation": "MMF = H · l"
    }
