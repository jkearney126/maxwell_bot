"""Magnetic field calculations."""

import math

# Physical constant
MU_0 = 4 * math.pi * 1e-7  # H/m (permeability of free space)


def solenoid_field(turns: int, length_m: float, current_A: float) -> dict:
    """
    Compute magnetic field at the center of a solenoid.

    Using B = μ₀ · n · I
    where n = N/L (turns per unit length)

    Args:
        turns: Number of turns in the solenoid
        length_m: Length of the solenoid in meters
        current_A: Current through the solenoid in amperes

    Returns:
        Dictionary with B field in Tesla
    """
    if length_m <= 0:
        return {"error": "Length must be positive"}
    if turns < 0:
        return {"error": "Turns cannot be negative"}

    n = turns / length_m  # turns per meter
    B = MU_0 * n * current_A

    return {
        "B_tesla": B,
        "turns": turns,
        "length_m": length_m,
        "current_A": current_A,
        "turns_per_meter": n,
        "equation": "B = μ₀ · n · I"
    }


def biot_savart_wire(current_A: float, distance_m: float) -> dict:
    """
    Compute magnetic field around an infinite straight current-carrying wire.

    Using B = μ₀ · I / (2π · r)

    Args:
        current_A: Current in the wire in amperes
        distance_m: Perpendicular distance from the wire in meters

    Returns:
        Dictionary with B field in Tesla
    """
    if distance_m <= 0:
        return {"error": "Distance must be positive"}

    B = (MU_0 * current_A) / (2 * math.pi * distance_m)

    return {
        "B_tesla": B,
        "current_A": current_A,
        "distance_m": distance_m,
        "equation": "B = μ₀ · I / (2π · r)"
    }


def magnetic_flux(B_tesla: float, area_m2: float, angle_deg: float = 0) -> dict:
    """
    Compute magnetic flux through a surface.

    Using Φ = B · A · cos(θ)

    Args:
        B_tesla: Magnetic flux density in Tesla
        area_m2: Area of the surface in square meters
        angle_deg: Angle between B and normal to surface in degrees (default 0)

    Returns:
        Dictionary with flux in Webers
    """
    if area_m2 < 0:
        return {"error": "Area must be non-negative"}

    angle_rad = math.radians(angle_deg)
    cos_theta = math.cos(angle_rad)
    flux = B_tesla * area_m2 * cos_theta

    return {
        "flux_Wb": flux,
        "B_tesla": B_tesla,
        "area_m2": area_m2,
        "angle_deg": angle_deg,
        "cos_theta": cos_theta,
        "equation": "Φ = B · A · cos(θ)"
    }


def energy_stored(B_tesla: float, volume_m3: float) -> dict:
    """
    Compute energy stored in a magnetic field.

    Using W = (B² / (2μ₀)) · Volume

    Args:
        B_tesla: Magnetic flux density in Tesla
        volume_m3: Volume of the field in cubic meters

    Returns:
        Dictionary with energy in Joules
    """
    if volume_m3 < 0:
        return {"error": "Volume must be non-negative"}

    W = (B_tesla ** 2 / (2 * MU_0)) * volume_m3

    return {
        "energy_J": W,
        "B_tesla": B_tesla,
        "volume_m3": volume_m3,
        "equation": "W = (B² / (2μ₀)) · Volume"
    }
